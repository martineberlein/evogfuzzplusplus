from debugging_framework.input.input import Input as TestInput
from debugging_framework.input.oracle import OracleResult
from isla.language import DerivationTree


class Input(TestInput):
    def __init__(self, tree: DerivationTree, oracle: OracleResult = None):
        super().__init__(tree, oracle)
        self.__fitness: float = float()

    @property
    def fitness(self) -> float:
        return self.__fitness

    @fitness.setter
    def fitness(self, fitness_: float):
        self.__fitness = fitness_
