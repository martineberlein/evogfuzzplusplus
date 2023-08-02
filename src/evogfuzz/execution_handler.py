from abc import ABC, abstractmethod
from typing import Callable, Union, Sequence, Optional, Set, List, Tuple

from evogfuzz.input import Input
from evogfuzz.oracle import OracleResult
from evogfuzz.report import TestResultMonad, Report


class ExecutionHandler(ABC):

    def __init__(self, oracle: Callable[[Union[Input, str, Set[Input]]], Union[OracleResult, Sequence]]):
        self.oracle = oracle

    @staticmethod
    def map_result(result: OracleResult) -> bool:
        match result:
            case OracleResult.BUG:
                return True
            case OracleResult.NO_BUG:
                return False
            case _:
                return False

    @staticmethod
    def add_to_report(report: Report, test_input: Input, exception: Optional[Exception]):
        report.add_failure(test_input, exception)

    @abstractmethod
    def label(self, **kwargs):
        raise NotImplementedError


class SingleExecutionHandler(ExecutionHandler):

    def _get_label(self, test_input: Input) -> TestResultMonad:
        return TestResultMonad(self.oracle(test_input))

    def label(self, test_inputs: Set[Input], report: Report, **kwargs):
        for inp in test_inputs:
            label, exception = self._get_label(inp).value()
            inp.oracle = label
            if self.map_result(label):
                self.add_to_report(report, inp, exception)


class BatchExecutionHandler(ExecutionHandler):

    def _get_label(self, test_inputs: Set[Input]) -> List[Tuple[Input, TestResultMonad]]:
        results = self.oracle(test_inputs)

        return [(inp, TestResultMonad(result)) for inp, result in zip(test_inputs, results)]

    def label(self, test_inputs: Set[Input], report: Report, **kwargs):
        test_results = self._get_label(test_inputs)

        for inp, test_result in test_results:
            label, exception = test_result.value()
            inp.oracle = label
            if self.map_result(label):
                self.add_to_report(report, inp, exception)
