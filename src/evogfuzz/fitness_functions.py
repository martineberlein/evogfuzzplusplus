from typing import Tuple, Set
from fuzzingbook.Parser import DerivationTree


def fitness_function_failure(data: Set[Tuple[DerivationTree, bool]]) -> Set[Tuple[DerivationTree, bool, float]]:
    fitness_data = set()
    for inp in data:
        fitness = get_fitness(inp)
        fitness_data.add((inp[0], inp[1], fitness))

    return fitness_data


def get_fitness(inp: Tuple[DerivationTree, bool]) -> int:
    if inp[1]:
        return 1
    else:
        return 0