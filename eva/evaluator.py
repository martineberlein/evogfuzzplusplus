import pandas as pd
import random
from typing import Callable, Union, Optional, Tuple, Set, Dict

from fuzzingbook.ProbabilisticGrammarFuzzer import ProbabilisticGrammarFuzzer
from isla.derivation_tree import DerivationTree
from debugging_benchmark.tests4py_benchmark import (
    PysnooperBenchmarkRepository,
    BenchmarkRepository,
)

from debugging_framework.evaluator import Evaluation
from debugging_framework.oracle import OracleResult
from debugging_framework.input import Input

SEEDS = [1231324, 1482323, 1921, 71291]


class ReproducerEvaluation(Evaluation):
    @staticmethod
    def asses_probabilistic_grammar(
        prob_grammar,
        oracle: Callable[[Input], Tuple[OracleResult, Optional[Exception]]],
    ) -> Dict[str, int]:
        prob_fuzzer = ProbabilisticGrammarFuzzer(prob_grammar)

        evaluation_inputs: Set[Input] = set()
        for _ in range(100):
            inp_tree = prob_fuzzer.fuzz_tree()
            inp = Input(tree=DerivationTree.from_parse_tree(inp_tree))
            inp.oracle, _ = oracle(inp)
            evaluation_inputs.add(inp)

        failing = len([
            inp for inp in evaluation_inputs if inp.oracle == OracleResult.FAILING
        ])
        passing = len([
            inp for inp in evaluation_inputs if inp.oracle == OracleResult.PASSING
        ])
        undefined = len([
            inp for inp in evaluation_inputs if inp.oracle == OracleResult.UNDEFINED
        ])

        return {
            "unique": len(evaluation_inputs),
            "failing": failing,
            "passing": passing,
            "undefined": undefined,
        }

    def run(self) -> pd.DataFrame:
        df_results = self.initialize_result_dataframe()

        for subject in self.subjects:
            # param = {**subject.to_dict(), **self.tool_param}
            param = {
                **subject.to_dict(),
                ** self.tool_param,
            }

            for tool in self.tools:
                for i in range(1, self.repetitions + 1):
                    random.seed(i)

                    prob_grammar = tool(**param).run()

                    oracle = param.get("oracle")

                    df_results.at[
                        (i, tool.name), (subject.name, subject.bug_id)
                    ] = self.asses_probabilistic_grammar(prob_grammar, oracle)

        if self.out_file:
            df_results.to_pickle(self.out_file)

        return df_results
