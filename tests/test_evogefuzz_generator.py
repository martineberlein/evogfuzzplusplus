import unittest
from pprint import pprint
from typing import Dict
from fuzzingbook.Grammars import Grammar, is_valid_grammar
from fuzzingbook.Parser import EarleyParser, tree_to_string

from evogfuzz.evogfuzz_class import EvoGGen
from evogfuzz.input import Input
from evogfuzz.oracle import OracleResult


def oracle(inp: Input | str):
    def subject_program(inp_):
        if eval(str(inp_)) <= -8:
            return True
        else:
            return False

    try:
        return OracleResult.BUG if subject_program(inp) else OracleResult.NO_BUG
    except SyntaxError:
        return OracleResult.UNDEF


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.grammar: Grammar = {
            "<start>": ["<number>"],
            "<number>": ["<maybe_minus><one_nine>"],
            "<maybe_minus>": ["-", ""],
            "<one_nine>": [str(i) for i in range(1, 10)],
        }
        assert is_valid_grammar(grammar=self.grammar)
        self.initial_inputs = ["-8", "1"]

        parser = EarleyParser(grammar=self.grammar)
        for inp in self.initial_inputs:
            for tree in parser.parse(inp):
                assert inp == tree_to_string(tree=tree)

        assert oracle(self.initial_inputs[0]) == OracleResult.BUG
        assert oracle(self.initial_inputs[1]) == OracleResult.NO_BUG

    def test_evogfuzz_generator(self):
        expected_grammar: Grammar = {
            "<start>": [("<number>", {"prob": None})],
            "<number>": [("<maybe_minus><one_nine>", {"prob": None})],
            "<maybe_minus>": [("-", {"prob": 1}), ("", {"prob": 0})],
            "<one_nine>": [
                ("1", {"prob": 0.0}),
                ("2", {"prob": 0.0}),
                ("3", {"prob": 0.0}),
                ("4", {"prob": 0.0}),
                ("5", {"prob": 0.0}),
                ("6", {"prob": 0.0}),
                ("7", {"prob": 0.0}),
                ("8", {"prob": 0.5}),
                ("9", {"prob": 0.5}),
            ],
        }

        evo = EvoGGen(
            grammar=self.grammar, inputs=self.initial_inputs, oracle=oracle, iterations=10
        )

        generator_grammar, failing_inputs = evo.optimize()
        self.assertEqual(generator_grammar, expected_grammar)
        self.assertEqual(failing_inputs, {"-8", "-9"})


if __name__ == "__main__":
    unittest.main()
