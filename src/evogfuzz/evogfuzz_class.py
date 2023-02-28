import logging
from typing import Callable, List, Union, Set, Tuple
from pathlib import Path
from random import choice
import numpy as np
from enum import Enum
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


class GrammarType(Enum):
    MUTATED = "mutated"
    LEARNED = "learned"

    def __str__(self):
        return self.value


class EvoGFuzz:
    def __init__(
        self,
        grammar: Grammar,
        prop: Callable[[Union[Input, str]], OracleResult],
        inputs: List[str],
        fitness_function: Callable[
            [Input], float
        ] = fitness_function_failure,
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
        self._tournament_size: int = 10
        self._tournament_number: int = 10
        self._all_inputs = None
        self._avg_prev_data = 0
        self.fitness_function: Union[
            Callable[
                [Input],
                float,
            ],
            None,
        ] = fitness_function

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

    def setup(self):
        for inp in self.inputs:
            inp.oracle = self._prop(inp)

        probabilistic_grammar = self._learn_probabilistic_grammar(self.inputs)
        self._probabilistic_grammars.append(
            (deepcopy(probabilistic_grammar), GrammarType.LEARNED, -1)
        )
        initial_population = self._generate_input_files(probabilistic_grammar)

        return initial_population

    def fuzz(self):
        logging.info("Fuzzing with EvoGFuzz")
        new_population: Set[Input] = self.setup()
        while self._do_more_iterations():
            logging.info(f"Starting iteration {self._iteration}")
            new_population = self._loop(new_population)
            self._iteration = self._iteration + 1
        self._finalize()

    def optimize(self) -> Grammar:
        logging.info("Optimizing with EvoGFuzz")
        while self._do_more_iterations():
            logging.info("Starting to optimize probabilities")

        # Return best Grammar
        return Grammar

    def _loop(self, test_inputs: Set[Input]):
        # obtain labels, execute samples (Initial Step, Activity 5)
        for inp in test_inputs:
            inp.oracle = self._prop(inp)

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
            new_test_inputs.add(Input(
                DerivationTree.from_parse_tree(probabilistic_fuzzer.fuzz_tree())
                )
            )
        return new_test_inputs

    def _safe_fitness_for_grammar(self, sum_fitness: float):
        grammar_tuple: Tuple[Grammar, GrammarType, float] = self._probabilistic_grammars.pop()
        grammar, grammar_type, _ = grammar_tuple
        self._probabilistic_grammars.append((grammar, grammar_type, sum_fitness))

    def _select_fittest_individuals(
        self, test_inputs: Set[Input]
    ) -> Set[Input]:

        fittest_individuals = Tournament(
            test_inputs, self._tournament_number
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

        probabilistic_grammar = (
            self._probabilistic_grammar_miner.mine_probabilistic_grammar(input_strings)
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
        logging.info(f"Selected rule {selected} to be mutated.")
        new_probs = np.random.random(size=len(mutated_grammar[selected]))
        new_probs /= new_probs.sum()

        for count, child in enumerate(mutated_grammar[selected]):
            child[1]["prob"] = list(new_probs)[count]

        for rule in mutated_grammar:
            logging.info(rule.ljust(30) + str(mutated_grammar[rule]))

        return mutated_grammar

    def _finalize(self):
        logging.info("Exiting EvoGFuzz!")
        logging.info("Final Grammar:")

        final_grammar = self._get_latest_grammar()

        for rule in final_grammar:
            logging.info(rule.ljust(30) + str(final_grammar[rule]))

    def _get_latest_grammar(self):
        return self._probabilistic_grammars[-1][0]
