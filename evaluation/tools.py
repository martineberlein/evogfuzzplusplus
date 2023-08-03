from abc import ABC, abstractmethod

from fuzzingbook.Grammars import Grammar, srange
from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.ProbabilisticGrammarFuzzer import (
    ProbabilisticGrammarMiner,
    ProbabilisticGrammarFuzzer,
)
from fuzzingbook.Parser import EarleyParser

from evogfuzz.evogfuzz_class import EvoGFuzz
from evogfuzz.input import Input
from evogfuzz.oracle import OracleResult
from evogfuzz.execution_handler import SingleExecutionHandler

from evogfuzz.report import MultipleFailureReport, Report


class Tool(ABC):
    def __init__(self, grammar, oracle, initial_inputs):
        self.oracle = oracle
        self.grammar = grammar
        self.initial_inputs = initial_inputs

        self.report = MultipleFailureReport(name=str(type(self)))
        self.execution_handler = SingleExecutionHandler(self.oracle)


class GrammarBasedTool(Tool):
    def __init__(
        self,
        grammar,
        oracle,
        initial_inputs,
        max_nonterminals: int = 5,
        max_generated_inputs: int = 10000,
    ):
        super().__init__(grammar, oracle, initial_inputs)
        self.max_nonterminals = max_nonterminals
        self.max_generated_inputs = max_generated_inputs

    @abstractmethod
    def run(self) -> Report:
        raise NotImplementedError


class GrammarBasedFuzzer(GrammarBasedTool):
    def run(self) -> Report:
        fuzzer = GrammarFuzzer(self.grammar, max_nonterminals=self.max_nonterminals)

        test_inputs = set()
        for _ in range(self.max_generated_inputs):
            test_inputs.add(fuzzer.fuzz())

        self.execution_handler.label_strings(test_inputs, self.report)
        return self.report


class InputsFromHellFuzzer(GrammarBasedTool):
    def run(self) -> Report:
        prob_grammar = ProbabilisticGrammarMiner(
            EarleyParser(self.grammar)
        ).mine_probabilistic_grammar(inputs=self.initial_inputs)
        fuzzer = ProbabilisticGrammarFuzzer(
            prob_grammar, max_nonterminals=self.max_nonterminals
        )

        test_inputs = set()
        for _ in range(self.max_generated_inputs):
            test_inputs.add(fuzzer.fuzz())

        self.execution_handler.label_strings(test_inputs, self.report)
        return self.report
