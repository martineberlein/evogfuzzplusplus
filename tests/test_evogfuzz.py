import unittest
from evogfuzz.evogfuzz_class import EvoGFuzz

from test_data import GRAMMAR, INITIAL_INPUTS, prop
from evogfuzz.fitness_functions import fitness_function_failure as fitness_function


class TestEvoGFuzz(unittest.TestCase):

    def test_evogfuzz_initialize(self):
        evogfuzz = EvoGFuzz(
            grammar=GRAMMAR,
            inputs=INITIAL_INPUTS,
            prop=prop,
            fitness_function=fitness_function,
        )
        evogfuzz.initialize()

    def test_something(self):
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
