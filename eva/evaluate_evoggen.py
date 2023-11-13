from typing import List, Type, Set
import logging
import random

from fuzzingbook.ProbabilisticGrammarFuzzer import ProbabilisticGrammarFuzzer
from isla.derivation_tree import DerivationTree
from debugging_benchmark.tests4py_benchmark import (
    PysnooperBenchmarkRepository,
    BenchmarkRepository,
)
from debugging_framework.evaluator import Evaluation
from debugging_framework.tools import InputsFromHellEvaluationFuzzer
from debugging_framework.input import Input
from debugging_framework.oracle import OracleResult

from tools import EvoGGenEvaluationTool, InputsFromHellReproducerTool, ReproducerTool
from evaluator import ReproducerEvaluation

SEEDS = [1231324, 1482323, 1921, 71291]

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:  %(message)s")

    tools: List[Type[ReproducerTool]] = [
        InputsFromHellReproducerTool,
        EvoGGenEvaluationTool
    ]

    subjects = PysnooperBenchmarkRepository().build()[:1]

    result = ReproducerEvaluation(
        tools=tools, subjects=subjects, repetitions=10, timeout=3600, tool_param={"max_iterations": 3}
    ).run()

    result.to_pickle("pysnooper_2")
    print(result)

    # for subject in subjects:
    #     param = {
    #         **subject.to_dict(),
    #         **{"max_iterations": 3},
    #         "initial_inputs": [
    #             "-d=7 -p='test' -w='e.nest2' -c=bool=str,int=str -O ",
    #             "-o -d=7 -p='1' -w='e.nest2' -c=bool=str,int=str -T ",
    #         ],
    #     }
    # for tool in tools:
    #     for seed in SEEDS:
    #         random.seed(seed)
    #         probabilistic_grammar = tool(**param).run()
    #         prob_fuzzer = ProbabilisticGrammarFuzzer(probabilistic_grammar)
    #
    #         evaluation_inputs: Set[Input] = set()
    #         oracle = param.get("oracle")
    #         for _ in range(100):
    #             inp_tree = prob_fuzzer.fuzz_tree()
    #             inp = Input(tree=DerivationTree.from_parse_tree(inp_tree))
    #             inp.oracle, _ = oracle(str(inp))
    #             evaluation_inputs.add(inp)
    #
    #         for inp in evaluation_inputs:
    #             print(inp, inp.oracle)
    #         print(f"Auswertung für {subject.name}_{subject.bug_id}")
    #         print(f"Generated: {len(evaluation_inputs)} unique inputs.")
    #         failing = [
    #             inp
    #             for inp in evaluation_inputs
    #             if inp.oracle == OracleResult.FAILING
    #         ]
    #         passing = [
    #             inp
    #             for inp in evaluation_inputs
    #             if inp.oracle == OracleResult.PASSING
    #         ]
    #         undefined = [
    #             inp
    #             for inp in evaluation_inputs
    #             if inp.oracle == OracleResult.UNDEFINED
    #         ]
    #
    #         print(
    #             f"{len(failing)} failing, {len(passing)} passing, {len(undefined)} undefined."
    #         )
