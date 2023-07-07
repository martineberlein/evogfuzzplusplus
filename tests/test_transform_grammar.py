import unittest

from fuzzingbook.Grammars import EXPR_GRAMMAR
from fuzzingbook.Parser import EarleyParser
from isla.derivation_tree import DerivationTree
from evogfuzz.input import Input
from evogfuzz.grammar_transformation import get_transformed_grammar


class TestGrammarTransformation(unittest.TestCase):
    def test_grammar_transformation(self):
        test_inputs = set()
        for inp in ["1 + 2", "2 + 1"]:
            test_inputs.add(
                Input(
                    DerivationTree.from_parse_tree(
                        next(EarleyParser(EXPR_GRAMMAR).parse(inp))
                    )
                )
            )

        transformed_grammar = get_transformed_grammar(
            test_inputs, EXPR_GRAMMAR, recursive=True
        )
        print(transformed_grammar)

        self.assertTrue(
            all(map(lambda x: x in transformed_grammar["<expr>"], ["1 + 2", "2"]))
        )
        self.assertTrue(
            all(map(lambda x: x in transformed_grammar["<term>"], ["1", "2"]))
        )
        self.assertTrue(
            all(map(lambda x: x in transformed_grammar["<factor>"], ["1", "2"]))
        )
        self.assertTrue(
            all(map(lambda x: x in transformed_grammar["<integer>"], ["1", "2"]))
        )
        self.assertTrue(
            all(map(lambda x: x in transformed_grammar["<digit>"], ["1", "2"]))
        )

        n = set()
        inp = "1 + 2"
        # transformed_grammar['<start>'] = ["<expr>"]

        p = EarleyParser(transformed_grammar)
        for tree in p.parse(inp):
            n.add(Input(DerivationTree.from_parse_tree(tree)))

        self.assertTrue(len(n) == 22)


if __name__ == "__main__":
    unittest.main()
