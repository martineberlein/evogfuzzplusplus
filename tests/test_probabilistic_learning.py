import unittest
from evogfuzz.helper import patch

from fuzzingbook.Parser import EarleyParser, is_valid_grammar, tree_to_string, Grammar
from fuzzingbook.ProbabilisticGrammarFuzzer import ProbabilisticGrammarMiner


class TestProbabilisticLearner(unittest.TestCase):
    def setUp(self) -> None:
        patch()
        self.grammar: Grammar = {
            "<start>": ["<maybe_minus><number>"],
            "<maybe_minus>": ["", "-"],
            "<number>": ["1", "2", "3"],
        }
        self.initial_inputs = ["-1", "3", "2", "1"]
        assert is_valid_grammar(grammar=self.grammar)
        p = EarleyParser(self.grammar)
        for inp in self.initial_inputs:
            for tree in p.parse(inp):
                assert tree_to_string(tree) == inp

    def test_probabilistic_miner(self):
        probabilistic_grammar_miner = ProbabilisticGrammarMiner(
            EarleyParser(self.grammar)
        )
        probabilistic_grammar = probabilistic_grammar_miner.mine_probabilistic_grammar(
            list(self.initial_inputs)
        )

        expected = {
            "<start>": [("<maybe_minus><number>", {"prob": None})],
            "<maybe_minus>": [("", {"prob": 0.75}), ("-", {"prob": 0.25})],
            "<number>": [
                ("1", {"prob": 0.5}),
                ("2", {"prob": 0.25}),
                ("3", {"prob": 0.25}),
            ],
        }
        self.assertEqual(expected, probabilistic_grammar)

        for rule in probabilistic_grammar:
            print(rule.ljust(30) + str(probabilistic_grammar[rule]))

    def test_probabilistic_miner_new(self):
        grammar: Grammar = {
            "<start>": ["<number>"],
            "<number>": ["<maybe_minus><one_nine>"],
            "<maybe_minus>": ["-", ""],
            "<one_nine>": [str(i) for i in range(1, 10)],
        }
        assert is_valid_grammar(grammar=self.grammar)
        initial_inputs = ["-8", "-9"]

        probabilistic_grammar_miner = ProbabilisticGrammarMiner(EarleyParser(grammar))
        probabilistic_grammar = probabilistic_grammar_miner.mine_probabilistic_grammar(
            initial_inputs
        )

        expected = {
            "<start>": [("<number>", {"prob": None})],
            "<maybe_minus>": [("-", {"prob": 1.0}), ("", {"prob": 0.0})],
            "<number>": [("<maybe_minus><one_nine>", {"prob": None})],
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
        self.assertEqual(expected, probabilistic_grammar)
