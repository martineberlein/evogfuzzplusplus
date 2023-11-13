from abc import abstractmethod

from fuzzingbook.Grammars import Grammar
from debugging_framework.tools import Tool, GrammarBasedEvaluationTool
from fuzzingbook.Grammars import Grammar
from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.ProbabilisticGrammarFuzzer import (
    ProbabilisticGrammarMiner,
    ProbabilisticGrammarFuzzer,
)
from fuzzingbook.Parser import EarleyParser
from isla.fuzzer import GrammarFuzzer as ISLaGrammarFuzzer

from debugging_framework.execution_handler import SingleExecutionHandler
from debugging_framework.report import MultipleFailureReport, Report

from evogfuzz.evogfuzz_class import EvoGFuzz, EvoGGen


class EvoGFuzzEvaluationTool(Tool):
    name = "EvoGFuzz"

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


class ReproducerTool:
    def __init__(self, grammar, oracle, initial_inputs, **kwargs):
        self.oracle = oracle
        self.grammar = grammar
        self.initial_inputs = initial_inputs

    @abstractmethod
    def run(self) -> Grammar:
        raise NotImplementedError


class InputsFromHellReproducerTool(ReproducerTool):
    name = "InputsFromHell-MoreOfTheSame"

    def run(self) -> Grammar:
        prob_grammar = ProbabilisticGrammarMiner(
            EarleyParser(self.grammar)
        ).mine_probabilistic_grammar(inputs=self.initial_inputs)

        return prob_grammar


class EvoGGenEvaluationTool(ReproducerTool):
    name = "EvoGGen"

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

    def run(self) -> Grammar:
        evoggen = EvoGGen(
            self.grammar,
            self.oracle,
            self.initial_inputs,
            iterations=self.max_iterations,
            transform_grammar=self.transform_grammar,
        )
        grammar, _ = evoggen.optimize()

        return grammar
