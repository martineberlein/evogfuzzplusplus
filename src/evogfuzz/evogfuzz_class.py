import logging
from typing import Callable, List, Union, Set, Tuple
from pathlib import Path
from random import choice
import numpy as np
from copy import deepcopy

from fuzzingbook.Grammars import Grammar
from fuzzingbook.Parser import EarleyParser
from fuzzingbook.ProbabilisticGrammarFuzzer import (
    is_valid_probabilistic_grammar,
    ProbabilisticGrammarMiner,
    ProbabilisticGrammarFuzzer,
)
from isla.derivation_tree import DerivationTree

from evogfuzz.tournament_selection import Tournament
from evogfuzz.fitness_functions import fitness_function_failure
from evogfuzz import helper
from evogfuzz.oracle import OracleResult
from evogfuzz.input import Input
from evogfuzz.grammar_transformation import transform_grammar_with_strings
from evogfuzz.types import GrammarType, Scenario


class EvoGFrame:
    scenario: Scenario = Scenario.FUZZING

    def __init__(
        self,
        grammar: Grammar,
        prop: Callable[[Union[Input, str]], OracleResult],
        inputs: List[str],
        fitness_function: Callable[[Input], float] = fitness_function_failure,
        iterations: int = 10,
        working_dir: Path = None,
    ):
        self.grammar = grammar
        self._prop: Callable[[Input], OracleResult] = prop
        self.working_dir = working_dir
        self._probabilistic_grammars: List[Tuple[Grammar, GrammarType, float]] = []
        self._iteration: int = 0
        self._max_iterations: int = iterations
        self._number_individuals: int = 100
        self._parameter_lambda: float = 2
        self._elitism_rate: int = 5
        self._tournament_size: int = 4
        self._tournament_number: int = 25
        self._all_inputs = None
        self._avg_prev_data = 0
        self.fitness_function: Union[
            Callable[
                [Input],
                float,
            ],
            None,
        ] = fitness_function

        # Fuzzing
        self.found_exceptions = set()

        self._probabilistic_grammar_miner = ProbabilisticGrammarMiner(
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

        # Apply patch to fuzzingbook
        helper.patch()

    def _setup(self, optimize: bool = False):
        for inp in self.inputs:
            inp.oracle = self._prop(inp)

        if optimize:
            assert True in set(
                True if inp.oracle == OracleResult.BUG else False for inp in self.inputs
            ), "EvoGFuzz needs at least one bug-triggering input."

        probabilistic_grammar = self._learn_probabilistic_grammar(self.inputs)
        self._probabilistic_grammars.append(
            (deepcopy(probabilistic_grammar), GrammarType.LEARNED, -1)
        )
        initial_population = self._generate_input_files(probabilistic_grammar)

        return initial_population

    def _loop(self, test_inputs: Set[Input]):
        # obtain labels, execute samples (Initial Step, Activity 5)
        for inp in test_inputs:
            label = self._prop(inp)
            if label == OracleResult.BUG:
                self.found_exceptions.add(inp)
            inp.oracle = label

        # determine fitness of individuals
        for inp in test_inputs:
            inp.fitness = self.fitness_function(inp)

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

        # generate new population
        return self._generate_input_files(mutated_grammar)

    def _do_more_iterations(self):
        if -1 == self._max_iterations:
            return True
        if self._iteration >= self._max_iterations:
            logging.info("Terminate due to maximal iterations reached")
            return False
        return True

    def _generate_input_files(self, probabilistic_grammar):
        logging.info("Generating new Test Inputs")
        probabilistic_fuzzer = ProbabilisticGrammarFuzzer(probabilistic_grammar)
        new_test_inputs = set()
        for _ in range(self._number_individuals):
            new_test_inputs.add(
                Input(DerivationTree.from_parse_tree(probabilistic_fuzzer.fuzz_tree()))
            )
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
        logging.debug(
            f"Current probabilistic grammar achieved a combined fitness of: {sum_fitness}"
        )
        self._safe_fitness_for_grammar(sum_fitness)

        return fittest_individuals

    def _learn_probabilistic_grammar(self, test_inputs: Set[Input]):
        logging.info("Learning new Grammar")

        input_strings = list(str(inp.tree) for inp in test_inputs)
        # print("\n new learning")
        # print(input_strings)

        probabilistic_grammar = (
            self._probabilistic_grammar_miner.mine_probabilistic_grammar(input_strings)
        )
        self._probabilistic_grammar_miner.reset()

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
        logging.info("Exiting EvoGFuzz!")
        logging.info("Final Grammar:")

        final_grammar = self._get_latest_grammar()

        for rule in final_grammar:
            logging.info(rule.ljust(30) + str(final_grammar[rule]))

    def _get_latest_grammar(self):
        return self._probabilistic_grammars[-1][0]


class EvoGFuzz(EvoGFrame):
    """
    This is the classic EvoGFuzz - the original grammar-based fuzzer!
    """

    def fuzz(self):
        logging.info("Fuzzing with EvoGFuzz")
        new_population: Set[Input] = self._setup()

        while self._do_more_iterations():
            logging.info(f"Starting iteration {self._iteration}")
            new_population = self._loop(new_population)
            self._iteration = self._iteration + 1

        self._finalize()

        return self.found_exceptions


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

    failure_inducing_inputs: Set[Input] = set()

    def setup(self):
        for inp in self.inputs:
            inp.oracle = self._prop(inp)

        assert True in set(
            True if inp.oracle == OracleResult.BUG else False for inp in self.inputs
        ), "EvoGGen needs at least one bug-triggering input."

    def optimize(self) -> (Grammar, Set[Input]):
        logging.info("Optimizing with EvoGFuzz")
        self.scenario = Scenario.GENERATOR

        self.setup()
        self.failure_inducing_inputs.update(
            {inp for inp in self.inputs if inp.oracle == OracleResult.BUG}
        )

        while self._do_more_iterations():
            logging.info("Starting to optimize probabilities")
            new_test_inputs = self._optimize_loop(self.failure_inducing_inputs)
            self.failure_inducing_inputs.update(
                {inp for inp in new_test_inputs if inp.oracle == OracleResult.BUG}
            )
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

        # learn new probabilistic grammar; Learn only from the most
        probabilistic_grammar = self._learn_probabilistic_grammar(failing_test_inputs)
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
            label = self._prop(inp)
            inp.oracle = label

        return new_inputs

    def _finalize(self, failing_test_inputs: Set[Input]) -> (Grammar, Set[Input]):
        failing_test_inputs_clean = {str(inp) for inp in failing_test_inputs}
        return (
            self._learn_probabilistic_grammar(failing_test_inputs),
            failing_test_inputs_clean,
        )
