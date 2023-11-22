from typing import List, Type
import logging

from debugging_benchmark.tests4py_benchmark import (
    PysnooperBenchmarkRepository,
    MiddleBenchmarkRepository,
    CookieCutterBenchmarkRepository,
    FastAPIBenchmarkRepository,
    BenchmarkRepository
)

from debugging_framework.tools import Tool
from debugging_framework.evaluator import Evaluation
from debugging_framework.benchmark import BenchmarkProgram
from debugging_framework.tools import InputsFromHellEvaluationFuzzer

from tools import EvoGFuzzEvaluationTool


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:  %(message)s")

    tools: List[Type[Tool]] = [
        InputsFromHellEvaluationFuzzer,
        EvoGFuzzEvaluationTool
    ]

    repositories: List[BenchmarkRepository] = [
        PysnooperBenchmarkRepository(),
        CookieCutterBenchmarkRepository(),
        FastAPIBenchmarkRepository(),
    ]

    subjects: List[BenchmarkProgram] = []
    for repository in repositories:
        subjects_ = repository.build()
        subjects += subjects_

    report = Evaluation(
        tools=tools,
        subjects=subjects,
        repetitions=10,
        timeout=3600,
        out_file="./results_tests4py.pkl",
        tool_param={"max_non_terminals": 10, "max_generated_inputs": 1000, "max_iterations": 10},
    ).run()

    print(report)


if __name__ == "__main__":
    exit(main())
