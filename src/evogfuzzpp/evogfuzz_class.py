import logging
from typing import Callable, List, Union, Set, Tuple
from pathlib import Path

from fuzzingbook.Grammars import Grammar
from fuzzingbook.Parser import EarleyParser
from fuzzingbook.ProbabilisticGrammarFuzzer import is_valid_probabilistic_grammar, ProbabilisticGrammarMiner, ProbabilisticGrammarFuzzer

from isla.language import DerivationTree
from evogfuzzpp.tournament_selection import Tournament


class EvoGFuzz:

    def __init__(
            self,
            grammar: Grammar,
            prop: Callable[[Union[DerivationTree, str]], bool],
            inputs: List[str],
            fitness_function: Callable[[Set[Tuple[DerivationTree, bool]]], Set[Tuple[DerivationTree, bool, float]]],
            working_dir: Path
    ):
        self.grammar = grammar
        self._prop = prop
        self.initial_inputs = set(inputs)
        self.working_dir = working_dir
        self._probabilistic_grammars: List[Grammar] = []
        self._iteration: int = 0
        self._max_iterations: int = 100
        self._number_individuals: int = 100
        self._parameter_lambda: float = 2
        self._elitism_rate: int = 5
        self._tournament_size: int = 10
        self._tournament_number: int = 10
        self._all_data = None
        self._avg_prev_data = 0
        self.fitness_function: Union[Callable[[Set[Tuple[DerivationTree, bool]]], Set[Tuple[DerivationTree, bool, float]]], None] = fitness_function

    def execute(self):
        logging.info("Executing EvoGFuzz")
        self.initialize()
        while self._do_more_iterations():
            logging.info(f"Starting iteration {self._iteration}")
            self._loop()
            self._iteration = self._iteration + 1

    def _loop(self):
        # generate input files
        new_inputs = self._generate_input_files()
        # execute input files
        execution_outcome = self._execute_input_files(new_inputs)
        data = set()
        for i in zip(new_inputs, execution_outcome):
            print(i)
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

        data = zip(self.initial_inputs, execution_outcome)
        positive_data: Set[Tuple[str, bool]] = {inp for inp in data if inp[1] is True}
        positive_inputs: List[str] = [inp[0] for inp in positive_data]

        probabilistic_grammar_miner = ProbabilisticGrammarMiner(
            EarleyParser(self.grammar))
        probabilistic_grammar = probabilistic_grammar_miner.mine_probabilistic_grammar(positive_inputs)

        logging.debug("Learned probabilistic grammar:")
        for rule in probabilistic_grammar:
            logging.debug(rule.ljust(40) + str(probabilistic_grammar[rule]))

        self._probabilistic_grammars.append(probabilistic_grammar)

        assert is_valid_probabilistic_grammar(probabilistic_grammar)

    def _do_more_iterations(self):
        if -1 == self._max_iterations:
            return True
        if self._iteration >= self._max_iterations:
            logging.info("Terminate due to maximal iterations reached")
            return False
        return True

    def _generate_input_files(self):
        probabilistic_fuzzer = ProbabilisticGrammarFuzzer(self._probabilistic_grammars[-1])
        new_inputs = set()
        for _ in range(self._number_individuals):
            new_inputs.add(probabilistic_fuzzer.fuzz())

        logging.info(f"Generated {len(new_inputs)} unique inputs")
        return new_inputs

    def _execute_input_files(self, input_samples: Set[Union[DerivationTree, str]]) -> List[bool]:
        logging.info("Executing input files")

        exec_oracle = []
        for inp in input_samples:
            print(inp)
            exec_oracle.append(self._prop(inp))

        return exec_oracle

    def _determine_fitness(self, data: Set[Tuple[DerivationTree, bool]]):
        return self.fitness_function(data)

    def _select_fittest_individuals(self, data) -> Set[Tuple[DerivationTree, bool, float]]:
        return Tournament(data, self._tournament_number).select_fittest_individuals()

    def _learn_new_grammar(self, fittest_individuals):
        pass

    def _mutate_grammar(self):
        pass

    def _add_new_data(self, fittest_individuals):
        if self._all_data is None:
            self._all_data = fittest_individuals
        else:
            self._all_data.update(fittest_individuals)

