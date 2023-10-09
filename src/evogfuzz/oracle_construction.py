from typing import Callable, Dict, Type, Optional, Tuple
import signal
from evogfuzz.oracle import OracleResult
from evogfuzz.input import Input


import signal

class ManageTimeout:
    def __init__(self, timeout: float):
        self.timeout = timeout

    def __enter__(self):
        self.old_handler = signal.signal(signal.SIGALRM, self.alarm_handler)
        self.set_alarm(self.timeout)

    def __exit__(self, exc_type, exc_value, traceback):
        self.cancel_alarm()
        signal.signal(signal.SIGALRM, self.old_handler)  # Restore old signal handler

    @staticmethod
    def alarm_handler(signum, frame):
        raise TimeoutError("Function call timed out")

    @staticmethod
    def set_alarm(seconds: float):
        signal.setitimer(signal.ITIMER_REAL, seconds)

    @staticmethod
    def cancel_alarm():
        signal.setitimer(signal.ITIMER_REAL, 0)


class UnexpectedResultError(Exception):
    pass


# Define the handler to be called when the alarm signal is received
def alarm_handler(signum, frame):
    raise TimeoutError("Function call timed out")


# Set the alarm signal handler
signal.signal(signal.SIGALRM, alarm_handler)


def set_alarm(seconds: int):
    signal.alarm(seconds)


def cancel_alarm():
    signal.alarm(0)


def construct_oracle(
    program_under_test: Callable,
    program_oracle: Optional[Callable],
    error_definitions: Optional[Dict[Type[Exception], OracleResult]] = None,
    timeout: float = 1,
    default_oracle_result: OracleResult = OracleResult.UNDEF,
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
    )


def _construct_functional_oracle(
    program_under_test: Callable,
    program_oracle: Callable,
    error_definitions: Dict[Type[Exception], OracleResult],
    timeout: float,
    default_oracle_result: OracleResult,
):
    def oracle(inp: Input) -> Tuple[OracleResult, Optional[Exception]]:
        param = list(map(int, str(inp).strip().split()))  # This might become a problem
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
):
    def oracle(inp: Input) -> OracleResult:
        try:
            with ManageTimeout(timeout):
                program_under_test(str(inp))
        except Exception as e:
            return error_definitions.get(type(e), default_oracle_result)
        return OracleResult.NO_BUG

    return oracle
