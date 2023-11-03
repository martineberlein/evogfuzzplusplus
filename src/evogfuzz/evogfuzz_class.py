import logging
from typing import Callable, List, Union, Set, Tuple, Sequence
from pathlib import Path
from random import choice
import numpy as np
from copy import deepcopy

from isla.parser import EarleyParser
from isla.derivation_tree import DerivationTree

from debugging_framework.grammar import is_valid_probabilistic_grammar
from debugging_framework.types import Grammar
from debugging_framework.oracle import OracleResult
from debugging_framework.probalistic_grammar_fuzzer import ProbabilisticGrammarFuzzer
from debugging_framework.report import MultipleFailureReport, SingleFailureReport
from debugging_framework.execution_handler import SingleExecutionHandler, BatchExecutionHandler


from evogfuzz.tournament_selection import Tournament
from evogfuzz.fitness_functions import fitness_function_failure

from evogfuzz.input import Input
from evogfuzz.types import GrammarType, Scenario
from evogfuzz.grammar_transformation import (
    get_transformed_grammar,
    get_transformed_grammar_from_strings,
)
from evogfuzz.probabilistic_fuzzer import ProbabilisticGrammarMinerExtended
from evogfuzz.report import MultipleFailureReport, SingleFailureReport
from evogfuzz.execution_handler import SingleExecutionHandler, BatchExecutionHandler
from evogfuzz.timeout_manager import ManageTimeout


class EvoGFrame:
    scenario: Scenario = Scenario.FUZZING

    def __init__(
        self,
        grammar: Grammar,
        oracle: Callable[[Union[Input, str]], Union[OracleResult, Sequence]],
        inputs: List[str],
        fitness_function: Callable[[Input], float] = fitness_function_failure,
        iterations: int = 10,
        use_multi_failure_report: bool = True,
        use_batch_execution: bool = False,
        transform_grammar: bool = False,
        working_dir: Path = None,
        logging: bool = False
    ):
        self.grammar = grammar
        self._oracle: Callable[[Input], Union[OracleResult, Sequence]] = oracle
        self.working_dir = working_dir
        self._probabilistic_grammars: List[Tuple[Grammar, GrammarType, float]] = []
        self._iteration: int = 0
        self._max_iterations: int = iterations
        self._number_individuals: int = 100
        self._parameter_lambda: float = 2
        self._elitism_rate: int = 5
        self._tournament_size: int = 4
        self._tournament_number: int = 25
        self._all_inputs = set()
        self._avg_prev_data = 0
        self.fitness_function: Callable[
            [Input],
            float,
        ] = fitness_function
        self.logging = logging

        # Fuzzing
        self.found_exceptions = set()  # TODO Remove

        self.report = (
            MultipleFailureReport()
            if use_multi_failure_report
            else SingleFailureReport()
        )

        self.execution_handler = (
            BatchExecutionHandler(self._oracle)
            if use_batch_execution
            else SingleExecutionHandler(self._oracle)
        )

        if transform_grammar:
            self.grammar = get_transformed_grammar_from_strings(
                inputs, self.grammar, recursive=False
            )

        self._probabilistic_grammar_miner = ProbabilisticGrammarMinerExtended(
            EarleyParser(self.grammar)
        )

        self.inputs = set()
        for inp in inputs:
            self.inputs.add(
                Input(
                    DerivationTree.from_parse_tree(
                        next(EarleyParser(grammar).parse(inp))
                    )
                )
            )

    def _setup(self):
        self.execution_handler.label(self.inputs, self.report)

        probabilistic_grammar = self._learn_probabilistic_grammar(self.inputs)
        self._probabilistic_grammars.append(
            (deepcopy(probabilistic_grammar), GrammarType.LEARNED, -1)
        )
        initial_population = self._generate_input_files(probabilistic_grammar)

        return initial_population

    def _loop(self, test_inputs: Set[Input]):
        # obtain labels, execute samples (Initial Step, Activity 5)
        self.execution_handler.label(test_inputs, self.report)

        test_inputs = set([inp for inp in test_inputs if inp.oracle != OracleResult.UNDEFINED])

        # determine fitness of individuals
        for inp in test_inputs:
            inp.fitness = self.fitness_function(inp)

        for inp in test_inputs:
            self._all_inputs.add(inp)

        # select fittest individuals
        fittest_individuals: Set[Input] = self._select_fittest_individuals(test_inputs)

        # learn new probabilistic grammar
        probabilistic_grammar = self._learn_probabilistic_grammar(fittest_individuals)
        self._probabilistic_grammars.append(
            (deepcopy(probabilistic_grammar), GrammarType.LEARNED, -1)
        )

        # mutate grammar
        mutated_grammar = self._mutate_grammar(probabilistic_grammar)
        self._probabilistic_grammars.append((mutated_grammar, GrammarType.MUTATED, -1))

        try:
            with ManageTimeout(2):
                # generate new population
                new_inputs = self._generate_input_files(mutated_grammar)
        except TimeoutError:
            logging.info("Timeout while generating new Inputs!")
            new_inputs = self.inputs

        return new_inputs

    def _do_more_iterations(self):
        if -1 == self._max_iterations:
            return True
        if self._iteration >= self._max_iterations:
            if self.logging:
                logging.info("Terminate due to maximal iterations reached")
            return False
        return True

    def _generate_input_files(self, probabilistic_grammar):
        if self.logging:
            logging.info("Generating new Test Inputs")
        probabilistic_fuzzer = ProbabilisticGrammarFuzzer(probabilistic_grammar)
        new_test_inputs = set()
        for _ in range(self._number_individuals):
            new_test_inputs.add(
                Input(DerivationTree.from_parse_tree(probabilistic_fuzzer.fuzz_tree()))
            )
        if self.logging:
            logging.info(f"Generated {len(new_test_inputs)} new Test Inputs")
        return new_test_inputs

    def _safe_fitness_for_grammar(self, sum_fitness: float):
        grammar_tuple: Tuple[
            Grammar, GrammarType, float
        ] = self._probabilistic_grammars.pop()
        grammar, grammar_type, _ = grammar_tuple
        self._probabilistic_grammars.append((grammar, grammar_type, sum_fitness))

    def _select_fittest_individuals(self, test_inputs: Set[Input]) -> Set[Input]:
        fittest_individuals = Tournament(
            test_inputs, self._tournament_number, self._tournament_size
        ).select_fittest_individuals()

        sum_fitness = sum([inp.fitness for inp in fittest_individuals])
        if self.logging:
            logging.debug(
            f"Current probabilistic grammar achieved a combined fitness of: {sum_fitness}"
        )
        self._safe_fitness_for_grammar(sum_fitness)

        return fittest_individuals

    def _learn_probabilistic_grammar(self, test_inputs: Set[Input], reset=True):
        if self.logging:
            logging.info("Learning new Grammar")

        # learning_trees = list(inp.tree for inp in test_inputs)
        # print("\n new learning")
        # print(input_strings)

        if reset:
            self._probabilistic_grammar_miner.reset()

        probabilistic_grammar = (
            self._probabilistic_grammar_miner.mine_probabilistic_grammar(test_inputs)
        )

        assert is_valid_probabilistic_grammar(
            probabilistic_grammar
        ), "Exit! Newly generated Grammar is not valid!"

        return probabilistic_grammar

    @staticmethod
    def _mutate_grammar(probabilistic_grammar):
        logging.info("Mutating new Grammar")

        mutated_grammar = deepcopy(probabilistic_grammar)

        # TODO if prev_avg < avg_fitness*1.025 -> Mutate

        # Only select production_rules with > 2 alternatives
        filtered = list(
            filter(lambda x: len(mutated_grammar[x]) > 1, list(mutated_grammar))
        )
        selected = choice(filtered)
        logging.debug(f"Selected rule {selected} to be mutated.")
        new_probs = np.random.random(size=len(mutated_grammar[selected]))
        new_probs /= new_probs.sum()

        for count, child in enumerate(mutated_grammar[selected]):
            child[1]["prob"] = list(new_probs)[count]

        for rule in mutated_grammar:
            logging.debug(rule.ljust(30) + str(mutated_grammar[rule]))

        return mutated_grammar

    def _finalize(self, **kwargs):
        if self.logging:
            logging.info("Exiting EvoGFuzz!")
            logging.info("Final Grammar:")

        final_grammar = self._get_latest_grammar()

        for rule in final_grammar:
            if self.logging:
                logging.info(rule.ljust(30) + str(final_grammar[rule]))

    def _get_latest_grammar(self):
        return self._probabilistic_grammars[-1][0]

    def _check_part_of_language(self, inp: str) -> bool:
        parser = EarleyParser(self.grammar)
        try:
            parser.parse(inp)
            return True
        except SyntaxError:
            # return False
            exit(-1)

    def get_found_exceptions_inputs(self) -> Set[Input]:
        return set(self.report.get_all_failing_inputs())

    def get_found_exceptions_strings(self) -> Set[str]:
        return {str(inp) for inp in self.report.get_all_failing_inputs()}

    def get_last_grammar(self):
        return self._get_latest_grammar()

    def get_all_inputs(self):
        return self._all_inputs


class EvoGFuzz(EvoGFrame):
    """
    This is the classic EvoGFuzz - the original grammar-based fuzzer!
    """

    def fuzz(self) -> Set[Input]:
        if self.logging:
            logging.info("Fuzzing with EvoGFuzz")
        new_population: Set[Input] = self._setup()

        while self._do_more_iterations():
            if self.logging:
                logging.info(f"Starting iteration {self._iteration}")
            new_population = self._loop(new_population)
            self._iteration = self._iteration + 1

        self._finalize()

        return self.get_found_exceptions_inputs()


class EvoGGen(EvoGFrame):
    """
    This is EvoGGen - a new extension to EvoGFuzz. EvoGGen is used to learn the properties of a given failure by
    learning a probabilistic grammar that will reproduce the defect efficiently.
        - Exploit, Explore Phase

        1. check failure (BUG!), Done
        2. reproduce failure (BUG Class)
        3. fitness function -> has prop to create diverse failing inputs
        4. Only learn from behavior triggering inputs?
                How Can we ensure that they are diverse?? -> LAM
        5.
    """

    def __init__(
        self,
        grammar: Grammar,
        oracle: Callable[[Union[Input, str]], OracleResult],
        inputs: List[str],
        fitness_function: Callable[[Input], float] = fitness_function_failure,
        iterations: int = 10,
        transform_grammar: bool = False,
        logging: bool = False,
    ):
        super().__init__(
            grammar=grammar,
            oracle=oracle,
            inputs=inputs,
            fitness_function=fitness_function,
            iterations=iterations,
            logging=logging
        )
        self.transform_grammar = transform_grammar
        self.failure_inducing_inputs: Set[Input] = set()

    def _setup(self):
        for inp in self.inputs:
            inp.oracle = self._oracle(inp)

        self.failure_inducing_inputs.update(
            {inp for inp in self.inputs if inp.oracle == OracleResult.FAILING}
        )

        assert True in set(
            True if inp.oracle[0] == OracleResult.FAILING else False for inp in self.inputs
        ), "EvoGGen needs at least one bug-triggering input."

        if self.transform_grammar:
            # ToDo find better implementation as this essentially overwrites __init__() from EvoFrame
            self.grammar = get_transformed_grammar(
                self.failure_inducing_inputs, self.grammar, recursive=False
            )

            # Overwrite the Probabilistic Grammar Miner
            self._probabilistic_grammar_miner = ProbabilisticGrammarMinerExtended(
                EarleyParser(self.grammar)
            )

    def optimize(self) -> (Grammar, Set[Input]):
        if self.logging:
            logging.info("Optimizing with EvoGGen")
        self.scenario = Scenario.GENERATOR

        self._setup()

        new_test_inputs = self.failure_inducing_inputs
        while self._do_more_iterations():
            if self.logging:
                logging.info(f"Starting Iteration {self._iteration}")
            generated_inputs = self._optimize_loop(new_test_inputs)
            new_test_inputs = {
                inp for inp in generated_inputs if inp.oracle == OracleResult.FAILING
            }
            self.failure_inducing_inputs.update(new_test_inputs)
            self._iteration = self._iteration + 1

        # Finalize
        return self._finalize(failing_test_inputs=self.failure_inducing_inputs)

    def _optimize_loop(self, failing_test_inputs: Set[Input]) -> Set[Input]:
        # determine fitness of failing inputs
        # we keep this for now, even if this has currently effect
        for inp in failing_test_inputs:
            if inp.fitness is None:
                inp.fitness = self.fitness_function(inp)

        # no selectio as we learn from all failing inputs
        # fittest_individuals: Set[Input] = self._select_fittest_individuals(failing_test_inputs)

        learning_set = failing_test_inputs - self.failure_inducing_inputs

        # learn new probabilistic grammar; Learn only from the most
        probabilistic_grammar = self._learn_probabilistic_grammar(
            learning_set, reset=False
        )
        self._probabilistic_grammars.append(
            (deepcopy(probabilistic_grammar), GrammarType.LEARNED, -1)
        )

        # mutate grammar
        mutated_grammar = self._mutate_grammar(probabilistic_grammar)
        self._probabilistic_grammars.append((mutated_grammar, GrammarType.MUTATED, -1))

        new_inputs: Set[Input] = set()
        new_inputs.update(self._generate_input_files(probabilistic_grammar))
        new_inputs.update(self._generate_input_files(mutated_grammar))

        for inp in new_inputs:
            label = self._oracle(inp)
            inp.oracle = label

        return new_inputs

    def finalize(self, failing_test_inputs: Set[Input]) -> (Grammar, Set[Input]):
        return (
            self._learn_probabilistic_grammar(failing_test_inputs, reset=True),
            failing_test_inputs,
        )
