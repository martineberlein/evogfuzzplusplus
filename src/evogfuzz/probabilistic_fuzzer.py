from typing import List, Union, Set, Tuple, Optional, Any

from debugging_framework.types import Grammar, Expansion
from debugging_framework.grammar import all_terminals
from debugging_framework.input import Input

from isla.parser import Parser
from isla.derivation_tree import DerivationTree

from fuzzingbook.ProbabilisticGrammarFuzzer import ProbabilisticGrammarMiner


def expansion_key(
    symbol: str,
    expansion: Union[Expansion, Tuple[str, Optional[List[Any]]], List[DerivationTree]],
) -> str:
    """Convert (symbol, `expansion`) into a key "SYMBOL -> EXPRESSION".
    `expansion` can be an expansion string, a derivation tree,
       or a list of derivation trees."""

    if isinstance(expansion, tuple):
        # Expansion or single derivation tree
        expansion, _ = expansion

    # Check for empty list expansion
    if isinstance(expansion, list) and not expansion:
        expansion = ""

    if not isinstance(expansion, str):
        # Derivation tree
        children = expansion
        expansion = all_terminals((symbol, children))

    assert isinstance(expansion, str)

    return symbol + " -> " + expansion


class ProbabilisticGrammarMinerExtended(ProbabilisticGrammarMiner):
    def __int__(self, parser: Parser, log: bool = False) -> None:
        super().__int__(parser, log)

    def add_coverage(self, symbol: str, children: List[DerivationTree]) -> None:
        key = expansion_key(symbol, children)

        if self.log:
            print("Found", key)

        if key not in self.expansion_counts:
            self.expansion_counts[key] = 0
        self.expansion_counts[key] += 1

    def count_expansions(self, inputs: Union[List[str], Set[Input]]) -> None:
        for inp in inputs:
            if isinstance(inp, str):
                tree, *_ = self.parser.parse(inp)
            elif isinstance(inp, Input):
                tree = inp.tree
            else:
                raise AssertionError("Could not learn from input ", inp)
            self.add_tree(tree)
            # for tree in self.parser.parse(inp):
            # tree, *_ = self.parser.parse(inp)
            #    self.add_tree(tree)

    def mine_probabilistic_grammar(
        self, inputs: Union[List[str], Set[Input]]
    ) -> Grammar:
        self.count_expansions(inputs)
        self.set_probabilities(self.counts())
        return self.grammar
