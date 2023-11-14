from typing import List, Type
import logging

from debugging_benchmark.tests4py_benchmark import (
    PysnooperBenchmarkRepository,
    YoutubeDLBenchmarkRepository
)

from tools import EvoGGenEvaluationTool, InputsFromHellReproducerTool, ReproducerTool
from evaluator import ReproducerEvaluation

SEEDS = [1231324, 1482323, 1921, 71291]

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:  %(message)s")

    tools: List[Type[ReproducerTool]] = [
        InputsFromHellReproducerTool,
        EvoGGenEvaluationTool
    ]

    subjects = PysnooperBenchmarkRepository().build()[1:2]
    # subjects = YoutubeDLBenchmarkRepository().build()

    result = ReproducerEvaluation(
        tools=tools, subjects=subjects, repetitions=10, timeout=3600, tool_param={"max_iterations": 10}
    ).run()

    result.to_pickle("youtube_dl.pkl")
    print(result)
