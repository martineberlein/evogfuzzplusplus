import unittest
from typing import Set, Optional, Sequence, Tuple, List, Any, Union

from evogfuzz.oracle import OracleResult
from evogfuzz.report import TestResultMonad


def program(test_input: str):
    if test_input == "pass":
        pass
    elif test_input == "failure_1":
        raise NotImplementedError("Failure_1")
    elif test_input == "failure_2":
        raise AssertionError("Failure_2")


def oracle(test_input: str) -> Union[Tuple[OracleResult, Exception], OracleResult]:
    try:
        program(test_input)
    except Exception as exp:
        return OracleResult.BUG, exp
    else:
        return OracleResult.NO_BUG


def get_label(test_input) -> TestResultMonad:
    return TestResultMonad(oracle(test_input))


class TestGenericOracle(unittest.TestCase):

    def test_generic_oracle(self):
        result = get_label("failure_1")
        label, exception = result.value()

        self.assertTrue(isinstance(label, OracleResult))
        self.assertTrue(isinstance(exception, Exception))
        self.assertTrue(isinstance(exception, NotImplementedError))

        result = get_label("failure_2")
        label, exception = result.value()
        self.assertTrue(isinstance(label, OracleResult))
        self.assertTrue(isinstance(exception, AssertionError))

        result = get_label("pass")
        label, exception = result.value()
        self.assertTrue(isinstance(label, OracleResult))
        self.assertEqual(exception, None)


if __name__ == '__main__':
    unittest.main()
