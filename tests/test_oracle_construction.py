import unittest
from debugging_framework.oracle_construction import (
    construct_oracle,
    OracleResult,
    Input,
    UnexpectedResultError,
)
from fuzzingbook.Grammars import Grammar
import string


grammar: Grammar = {
    "<start>": ["<input>"],
    "<input>": ["<first> <second>"],
    "<first>": ["<integer>"],
    "<second>": ["<integer>"],
    "<integer>": ["<one_nine><maybe_digits>"],  # no 0 at the moment
    "<one_nine>": [str(num) for num in range(1, 10)],
    "<digit>": list(string.digits),
    "<maybe_digits>": ["", "<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],
}


class TestConstructOracle(unittest.TestCase):
    def setUp(self):
        self.error_definitions = {
            UnexpectedResultError: OracleResult.FAILING,
            TimeoutError: OracleResult.UNDEFINED,
        }
        self.harness_function = lambda inp: list(map(int, str(inp).strip().split()))

    def test_same_result(self):
        def oracle(x, y):
            return x + y

        def under_test(x, y):
            return x + y

        my_oracle = construct_oracle(
            under_test,
            oracle,
            self.error_definitions,
            harness_function=self.harness_function,
        )
        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertEqual(oracle_result, OracleResult.PASSING)

    def test_different_result(self):
        def oracle(x, y):
            return x + y

        def under_test(x, y):
            return x - y

        my_oracle = construct_oracle(
            under_test,
            oracle,
            self.error_definitions,
            harness_function=self.harness_function,
        )
        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertEqual(oracle_result, OracleResult.FAILING)

    def test_defined_exception(self):
        def oracle(x, y):
            return x + y

        def under_test(x, y):
            raise TimeoutError()

        my_oracle = construct_oracle(
            oracle,
            under_test,
            self.error_definitions,
            harness_function=self.harness_function,
        )
        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertEqual(oracle_result, OracleResult.UNDEFINED)

    def test_undefined_exception(self):
        def oracle(x, y):
            return x + y

        def under_test(x, y):
            raise ValueError()

        my_oracle = construct_oracle(
            oracle,
            under_test,
            self.error_definitions,
            harness_function=self.harness_function,
        )
        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertEqual(oracle_result, OracleResult.UNDEFINED)

    def test_timeout_sleep(self):
        def oracle(x, y):
            return x + y

        def under_test(x, y):
            import time

            time.sleep(2)
            return x + y

        my_oracle = construct_oracle(
            under_test,
            oracle,
            {TimeoutError: OracleResult.FAILING},
            timeout=1,
            harness_function=self.harness_function,
        )

        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertEqual(oracle_result, OracleResult.FAILING)

    def test_no_error_definition(self):
        def oracle(x, y):
            return x + y

        def under_test(x, y):
            raise ValueError

        def under_test_unexpected_result_error(x, y):
            raise x + y + 1

        def under_test_timeout(x, y):
            import time

            time.sleep(2)
            return x + y

        my_oracle = construct_oracle(
            under_test, oracle, harness_function=self.harness_function
        )
        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertEqual(oracle_result, OracleResult.FAILING)

        my_oracle = construct_oracle(
            under_test_unexpected_result_error,
            oracle,
            harness_function=self.harness_function,
        )
        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertEqual(oracle_result, OracleResult.FAILING)

        my_oracle = construct_oracle(
            under_test_timeout, oracle, harness_function=self.harness_function
        )
        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertEqual(oracle_result, OracleResult.FAILING)

    def test_timeout_sleep_fraction(self):
        def oracle(x, y):
            return x + y

        def under_test(x, y):
            import time

            time.sleep(2)
            return x + y

        my_oracle = construct_oracle(
            under_test,
            oracle,
            {TimeoutError: OracleResult.FAILING},
            timeout=0.5,
            harness_function=self.harness_function,
        )

        oracle_result, _ = my_oracle(Input.from_str(grammar, "1 1"))
        self.assertEqual(oracle_result, OracleResult.FAILING)


if __name__ == "__main__":
    unittest.main()
