from debugging_framework.input import Input
from debugging_framework.oracle import OracleResult


def fitness_function_failure(test_input: Input) -> float:
    return get_fitness(test_input)


def get_fitness(test_input: Input) -> int:
    if test_input.oracle == OracleResult.FAILING:
        return 1
    else:
        return 0
