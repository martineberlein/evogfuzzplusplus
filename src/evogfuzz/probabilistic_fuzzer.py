from typing import List, Union, Set

from debugging_framework.types import Grammar
from debugging_framework.grammar import expansion_key
from debugging_framework.probalistic_grammar_miner import ProbabilisticGrammarMiner
from isla.parser import Parser
from isla.derivation_tree import DerivationTree

from evogfuzz.input import Input


class ProbabilisticGrammarMinerExtended(ProbabilisticGrammarMiner):
    def __init__(self, parser: Parser, log: bool = False) -> None:
        super().__init__(parser, log)

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
