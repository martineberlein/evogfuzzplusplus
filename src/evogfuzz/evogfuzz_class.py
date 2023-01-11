import logging
from typing import Callable, List, Union, Set, Tuple
from pathlib import Path
from random import choice
import numpy as np
from enum import Enum
from copy import deepcopy

from fuzzingbook.Grammars import Grammar
from fuzzingbook.Parser import EarleyParser, DerivationTree
from fuzzingbook.ProbabilisticGrammarFuzzer import (
    is_valid_probabilistic_grammar,
    ProbabilisticGrammarMiner,
    ProbabilisticGrammarFuzzer,
)

from evogfuzz.tournament_selection import Tournament
from evogfuzz.fitness_functions import fitness_function_failure


class GrammarType(Enum):
    MUTATED = "mutated"
    LEARNED = "learned"

    def __str__(self):
        return self.value


class EvoGFuzz:
    def __init__(
        self,
        grammar: Grammar,
        prop: Callable[[Union[DerivationTree, str]], bool],
        inputs: List[str],
        fitness_function: Callable[
            [Set[Tuple[DerivationTree, bool]]], Set[Tuple[DerivationTree, bool, float]]
        ] = fitness_function_failure,
        iterations: int = 10,
        working_dir: Path = None,
    ):
        self.grammar = grammar
        self._prop = prop
        self.initial_inputs = set(inputs)
        self.working_dir = working_dir
        self._probabilistic_grammars: List[Tuple[Grammar, GrammarType, float]] = []
        self._iteration: int = 0
        self._max_iterations: int = iterations
        self._number_individuals: int = 100
        self._parameter_lambda: float = 2
        self._elitism_rate: int = 5
        self._tournament_size: int = 10
        self._tournament_number: int = 10
        self._all_data = None
        self._avg_prev_data = 0
        self.fitness_function: Union[
            Callable[
                [Set[Tuple[DerivationTree, bool]]],
                Set[Tuple[DerivationTree, bool, float]],
            ],
            None,
        ] = fitness_function
        self._probabilistic_grammar_miner = None

    def execute(self):
        logging.info("Fuzzing with EvoGFuzz")
        self.initialize()
        while self._do_more_iterations():
            logging.info(f"Starting iteration {self._iteration}")
            self._loop()
            self._iteration = self._iteration + 1
        self._finalize()

    def optimize(self) -> Grammar:
        logging.info("Optimizing with EvoGFuzz")
        self.initialize()
        while self._do_more_iterations():
            logging.info("Starting to optimize probabilities")

        # Return best Grammar
        return Grammar

    def _loop(self):
        # generate input files
        new_inputs = self._generate_input_files()
        # execute input files
        execution_outcome = self._execute_input_files(new_inputs)
        data = set()
        for i in zip(new_inputs, execution_outcome):
            data.add(i)
        # determine fitness of individuals
        fitness = self._determine_fitness(data)
        # select fittest individuals
        fittest_individuals = self._select_fittest_individuals(fitness)
        # learn new probabilistic grammar
        self._learn_new_grammar(fittest_individuals)
        # mutate grammar
        self._mutate_grammar()  # TODO Only mutate when no improvement
        # collect new data
        self._add_new_data(fittest_individuals)
        # display stats
        # self.__show_stats()

    def initialize(self):
        execution_outcome = self._execute_input_files(self.initial_inputs)
        logging.info("exec: " + str(execution_outcome))
        logging.info("inp: " + str(self.initial_inputs))

        data = zip(self.initial_inputs, execution_outcome)
        logging.info("zip_list: " + str(list(data)))
        # positive_data: Set[Tuple[str, bool]] = {inp for inp in data if inp[1] is True}
        # positive_inputs: List[str] = [inp[0] for inp in positive_data]

        logging.info("New Learning.")
        self._probabilistic_grammar_miner = ProbabilisticGrammarMiner(
            EarleyParser(self.grammar)
        )
        probabilistic_grammar = (
            self._probabilistic_grammar_miner.mine_probabilistic_grammar(
                list(self.initial_inputs)
            )
        )

        logging.debug("Learned probabilistic grammar:")
        for rule in probabilistic_grammar:
            logging.debug(rule.ljust(40) + str(probabilistic_grammar[rule]))

        self._probabilistic_grammars.append(
            (deepcopy(probabilistic_grammar), GrammarType.LEARNED, -1)
        )

        assert is_valid_probabilistic_grammar(probabilistic_grammar)

    def _do_more_iterations(self):
        if -1 == self._max_iterations:
            return True
        if self._iteration >= self._max_iterations:
            logging.info("Terminate due to maximal iterations reached")
            return False
        return True

    def _generate_input_files(self):
        grammar = self._get_latest_grammar()
        probabilistic_fuzzer = ProbabilisticGrammarFuzzer(grammar)
        new_inputs = set()
        for _ in range(self._number_individuals):
            new_inputs.add(probabilistic_fuzzer.fuzz())

        logging.info(f"Generated {len(new_inputs)} unique inputs")
        return new_inputs

    def _execute_input_files(
        self, input_samples: Set[Union[DerivationTree, str]]
    ) -> List[bool]:
        logging.info("Executing input files")

        exec_oracle = []
        for inp in input_samples:
            exec_oracle.append(self._prop(inp))

        return exec_oracle

    def _determine_fitness(self, data: Set[Tuple[DerivationTree, bool]]):
        return self.fitness_function(data)

    def _safe_fitness_for_grammar(self, sum_fitness):
        g = self._probabilistic_grammars.pop()
        lst = list(g)
        lst[2] = sum_fitness
        self._probabilistic_grammars.append(tuple(lst))

    def _select_fittest_individuals(
        self, data
    ) -> Set[Tuple[DerivationTree, bool, float]]:
        fittest_individuals = Tournament(
            data, self._tournament_number
        ).select_fittest_individuals()
        sum_fitness = sum([x[2] for x in fittest_individuals])
        logging.info(
            f"Current probabilistic grammar achived a fitness of: {sum_fitness}"
        )
        self._safe_fitness_for_grammar(sum_fitness)

        return fittest_individuals

    def _learn_new_grammar(self, fittest_individuals):
        logging.info("Learning new Grammar")

        # Unpacking input samples
        input_samples = list(x[0] for x in fittest_individuals)
        logging.info(input_samples)

        probabilistic_grammar_miner = ProbabilisticGrammarMiner(
            EarleyParser(self.grammar)
        )
        new_probabilistic_grammar = (
            probabilistic_grammar_miner.mine_probabilistic_grammar(input_samples)
        )
        assert is_valid_probabilistic_grammar(
            new_probabilistic_grammar
        ), "Exit! Newly generated Grammar is not valid!"

        self._probabilistic_grammars.append(
            (deepcopy(new_probabilistic_grammar), GrammarType.LEARNED, -1)
        )

    def _mutate_grammar(self):
        logging.info("Mutating new Grammar")

        mutated_grammar = deepcopy(self._get_latest_grammar())

        # if prev_avg < avg_fitness*1.025 -> Mutate
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

        self._probabilistic_grammars.append((mutated_grammar, GrammarType.MUTATED, -1))

    def _add_new_data(self, fittest_individuals):
        if self._all_data is None:
            self._all_data = fittest_individuals
        else:
            self._all_data.update(fittest_individuals)

    def _finalize(self):
        logging.info("Exiting EvoGFuzz!")
        logging.info("Final Grammar:")

        final_grammar = self._get_latest_grammar()

        for rule in final_grammar:
            logging.info(rule.ljust(30) + str(final_grammar[rule]))

    def _get_latest_grammar(self):
        return self._probabilistic_grammars[-1][0]
