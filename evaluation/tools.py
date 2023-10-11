from abc import ABC, abstractmethod

from fuzzingbook.Grammars import Grammar, srange
from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.ProbabilisticGrammarFuzzer import (
    ProbabilisticGrammarMiner,
    ProbabilisticGrammarFuzzer,
)
from fuzzingbook.Parser import EarleyParser
from isla.fuzzer import GrammarFuzzer as ISLaGrammarFuzzer

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
        self.generated_inputs = set()

    @abstractmethod
    def run(self) -> Report:
        raise NotImplementedError

    def get_generated_inputs(self):
        return self.generated_inputs


class GrammarBasedEvaluationTool(Tool, ABC):
    def __init__(
        self,
        grammar,
        oracle,
        initial_inputs,
        max_nonterminals: int = 5,
        max_generated_inputs: int = 10000,
        **kwargs
    ):
        super().__init__(grammar, oracle, initial_inputs)
        self.report = MultipleFailureReport(name=type(self).__name__)
        self.execution_handler = SingleExecutionHandler(self.oracle)

        self.max_nonterminals = max_nonterminals
        self.max_generated_inputs = max_generated_inputs


class GrammarBasedEvaluationFuzzer(GrammarBasedEvaluationTool):
    def run(self) -> Report:
        fuzzer = GrammarFuzzer(self.grammar, max_nonterminals=self.max_nonterminals)

        test_inputs = set()
        for _ in range(self.max_generated_inputs):
            test_inputs.add(fuzzer.fuzz())

        self.execution_handler.label_strings(test_inputs, self.report)
        self.generated_inputs = test_inputs
        return self.report


class InputsFromHellEvaluationFuzzer(GrammarBasedEvaluationTool):
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
        self.generated_inputs = test_inputs
        return self.report


class ISLaGrammarEvaluationFuzzer(GrammarBasedEvaluationTool):
    def run(self) -> Report:
        fuzzer = ISLaGrammarFuzzer(self.grammar, max_nonterminals=self.max_nonterminals)

        test_inputs = set()
        for _ in range(self.max_generated_inputs):
            test_inputs.add(fuzzer.fuzz())

        self.execution_handler.label_strings(test_inputs, self.report)
        self.generated_inputs = test_inputs
        return self.report


class EvoGFuzzEvaluationTool(Tool):
    def __init__(
        self,
        grammar,
        oracle,
        initial_inputs,
        max_iterations=100,
        transform_grammar=True,
        **kwargs
    ):
        super().__init__(grammar, oracle, initial_inputs)
        self.max_iterations = max_iterations
        self.transform_grammar = transform_grammar

    def run(self) -> Report:
        evogfuzz = EvoGFuzz(
            self.grammar,
            self.oracle,
            self.initial_inputs,
            iterations=self.max_iterations,
            transform_grammar=self.transform_grammar,
        )
        _ = evogfuzz.fuzz()

        self.generated_inputs = evogfuzz.get_all_inputs()
        return evogfuzz.report
