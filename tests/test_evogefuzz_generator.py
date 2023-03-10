import unittest

from evogfuzz.evogfuzz_class import EvoGFuzz

from evogfuzz_formalizations.calculator import grammar_alhazen as grammar, initial_inputs, prop
from evogfuzz.fitness_functions import fitness_function_failure as fitness_function


class MyTestCase(unittest.TestCase):
    def test_evogfuzz_generator(self):
        evo = EvoGFuzz(
            grammar=grammar,
            inputs=initial_inputs,
            prop=prop
        )

        result = evo.optimize()
        print(result)


if __name__ == '__main__':
    unittest.main()
