import unittest
from typing import Set, Tuple, Union

from isla.derivation_tree import DerivationTree
from fuzzingbook.Parser import EarleyParser

from evogfuzz.execution_handler import (
    SingleExecutionHandler,
    BatchExecutionHandler,
)
from evogfuzz.input import Input
from evogfuzz.oracle import OracleResult
from evogfuzz.report import MultipleFailureReport

from evogfuzz_formalizations.calculator import grammar_alhazen as grammar


def program(test_input: str):
    if test_input == "sin(1)":
        pass
    elif test_input == "sqrt(-900)":
        raise NotImplementedError("Failure_1")
    elif test_input == "cos(10)":
        raise AssertionError("Failure_2")


def oracle(test_input: str) -> Union[Tuple[OracleResult, Exception], OracleResult]:
    try:
        program(str(test_input))
    except Exception as exp:
        return OracleResult.BUG, exp
    else:
        return OracleResult.NO_BUG


def batch_oracle(test_inputs: Set[Input]):
    result = list()
    for inp in test_inputs:
        try:
            program(str(inp))
        except Exception as exp:
            result.append((OracleResult.BUG, exp))
        else:
            result.append((OracleResult.NO_BUG, None))

    return result


class TestExecutionHandler(unittest.TestCase):
    def setUp(self) -> None:
        inputs = {"sqrt(-900)", "cos(10)", "sin(1)"}

        self.test_inputs = set()
        for inp in inputs:
            self.test_inputs.add(
                Input(
                    DerivationTree.from_parse_tree(
                        next(EarleyParser(grammar).parse(inp))
                    )
                )
            )

    def test_execution_handler(self):
        handler = SingleExecutionHandler(oracle=oracle)
        report = MultipleFailureReport()

        handler.label(self.test_inputs, report)
        print(report)
        for inp in self.test_inputs:
            print(inp, inp.oracle)

    def test_batch_execution_handler(self):
        handler = BatchExecutionHandler(oracle=batch_oracle)
        report = MultipleFailureReport()

        handler.label(self.test_inputs, report)
        print(report)
        for inp in self.test_inputs:
            print(inp, inp.oracle)


if __name__ == "__main__":
    unittest.main()
