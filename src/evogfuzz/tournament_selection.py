import logging
from typing import Set, List

from debugging_framework.input import Input


class Tournament:
    def __init__(
        self,
        test_inputs: Set[Input],
        tournament_rounds: int = 10,
        tournament_size: int = 10,
    ):
        self.test_inputs: Set[Input] = test_inputs
        self.tournament_rounds: int = tournament_rounds
        self.tournament_size: int = tournament_size

    def select_fittest_individuals(self):
        # print(len(self.test_inputs), self.tournament_rounds)
        # assert self.tournament_rounds < len(self.test_inputs)

        fittest: Set[Input] = set()

        try:
            for _ in range(self.tournament_rounds):
                current_round: List[Input] = list(self.test_inputs)[
                    : self.tournament_size
                ]
                for inp in current_round:
                    self.test_inputs.remove(inp)
                fi = sorted(
                    current_round, key=lambda inp: inp.fitness, reverse=False
                ).pop()
                fittest.add(fi)
        except IndexError:
            logging.debug("Tournament Size too big! No more Inputs left to select!")

        return fittest
