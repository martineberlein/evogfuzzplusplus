import unittest
from typing import Tuple, Union

from debugging_framework.oracle import OracleResult
from debugging_framework.report import TResultMonad


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
        return OracleResult.FAILING, exp
    else:
        return OracleResult.PASSING


def get_label(test_input) -> TResultMonad:
    return TResultMonad(oracle(test_input))


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


if __name__ == "__main__":
    unittest.main()
