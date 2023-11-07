import unittest

from debugging_benchmark.calculator.calculator import grammar, initial_inputs, oracle

from evogfuzz import EvoGFuzz
from evogfuzz.visualization import parse_prob_grammars, plot

ITERATIONS = 3


class TestEvoGFuzzVisualization(unittest.TestCase):
    def setUp(self) -> None:
        self.evogfuzz = EvoGFuzz(
            grammar=grammar, oracle=oracle, inputs=initial_inputs, iterations=ITERATIONS
        )
        self.evogfuzz.fuzz()
        self.all_prob_grammars = self.evogfuzz._probabilistic_grammars
        assert len(self.all_prob_grammars) == ITERATIONS * 2 + 1

    def test_parse_prob_grammars(self):
        grammar_list = [x[0] for x in self.all_prob_grammars]
        res = parse_prob_grammars(grammar_list)
        expected = {
            "<start>-><arith_expr>",
            "<arith_expr>-><function>(<number>)",
            "<function>->sqrt",
            "<function>->sin",
            "<function>->cos",
            "<function>->tan",
            "<number>-><maybe_minus><onenine><maybe_digits><maybe_frac>",
            "<maybe_minus>->",
            "<maybe_minus>->-",
            "<onenine>->1",
            "<onenine>->2",
            "<onenine>->3",
            "<onenine>->4",
            "<onenine>->5",
            "<onenine>->6",
            "<onenine>->7",
            "<onenine>->8",
            "<onenine>->9",
            "<digit>->0",
            "<digit>->1",
            "<digit>->2",
            "<digit>->3",
            "<digit>->4",
            "<digit>->5",
            "<digit>->6",
            "<digit>->7",
            "<digit>->8",
            "<digit>->9",
            "<maybe_digits>->",
            "<maybe_digits>-><digits>",
            "<digits>-><digit>",
            "<digits>-><digit><digits>",
            "<maybe_frac>->",
            "<maybe_frac>->.<digits>",
        }
        actual = set(res.keys())
        self.assertEqual(expected, actual)

        for expansion_key in res.keys():
            assert len(res[expansion_key]) == ITERATIONS * 2 + 1

    def test_visualization_plot(self):
        plot(self.all_prob_grammars)
