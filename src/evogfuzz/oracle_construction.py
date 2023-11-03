from typing import Callable, Dict, Type, Optional, Tuple

from evogfuzz.oracle import OracleResult
from evogfuzz.input import Input
from evogfuzz.timeout_manager import ManageTimeout


class UnexpectedResultError(Exception):
    pass


def construct_oracle(
    program_under_test: Callable,
    program_oracle: Optional[Callable],
    error_definitions: Optional[Dict[Type[Exception], OracleResult]] = None,
    timeout: float = 1,
    default_oracle_result: OracleResult = OracleResult.UNDEF,
    harness_function: Callable = None,
) -> Callable[[Input], OracleResult]:
    error_definitions = error_definitions or {}
    default_oracle_result = (
        OracleResult.BUG if not error_definitions else default_oracle_result
    )

    if not isinstance(error_definitions, dict):
        raise ValueError(f"Invalid value for expected_error: {error_definitions}")

    # Choose oracle construction method based on presence of program_oracle
    oracle_constructor = (
        _construct_functional_oracle if program_oracle else _construct_failure_oracle
    )

    return oracle_constructor(
        program_under_test,
        program_oracle,
        error_definitions,
        timeout,
        default_oracle_result,
        harness_function,
    )


def _construct_functional_oracle(
    program_under_test: Callable,
    program_oracle: Callable,
    error_definitions: Dict[Type[Exception], OracleResult],
    timeout: float,
    default_oracle_result: OracleResult,
    harness_function: Callable,
):
    def oracle(inp: Input) -> Tuple[OracleResult, Optional[Exception]]:
        # param = list(map(int, str(inp).strip().split()))  # This might become a problem
        param = harness_function(str(inp)) if harness_function else str(inp)

        try:
            with ManageTimeout(timeout):
                produced_result = program_under_test(*param)

            expected_result = program_oracle(*param)
            if expected_result != produced_result:
                raise UnexpectedResultError("Results do not match")
        except Exception as e:
            return error_definitions.get(type(e), default_oracle_result), e
        return OracleResult.NO_BUG, None

    return oracle


def _construct_failure_oracle(
    program_under_test: Callable,
    error_definitions: Dict[Type[Exception], OracleResult],
    timeout: int,
    default_oracle_result: OracleResult,
    harness_function: Callable,
):
    def oracle(inp: Input) -> OracleResult:
        param = harness_function(str(inp)) if harness_function else str(inp)
        try:
            with ManageTimeout(timeout):
                program_under_test(*param)
        except Exception as e:
            return error_definitions.get(type(e), default_oracle_result)
        return OracleResult.NO_BUG

    return oracle
