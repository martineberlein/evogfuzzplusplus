from typing import Set, Tuple
from operator import itemgetter


class Tournament:

    def __init__(self, fitness_data: Set[Tuple[str, bool, float]],
                 tournament_rounds: int = 10,
                 tournament_size: int = 10
                 ):
        self._fitness_data = fitness_data # sorted(fitness_data,key=itemgetter(1), reverse=True)
        self._tournament_rounds = tournament_rounds
        self._tournament_size = tournament_size

    def select_fittest_individuals(self):
        fittest = set()

        for _ in range(self._tournament_rounds):
            f = list(self._fitness_data)[:10]
            fi = sorted(f, key=itemgetter(1), reverse=True)[0]
            fittest.add(fi)
            self._fitness_data.remove(fi)

        return fittest
