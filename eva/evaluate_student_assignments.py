from typing import List, Type
import logging

from debugging_benchmark.student_assignments import (
    NPrTestSubject,
    SquareRootTestSubject,
    GCDTestSubject,
    SieveOfEratosthenesTestSubject,
    MiddleTestSubject,
    FibonacciTestSubject,
    BubbleSortTestSubject,
    PalindromeTestSubject,
    RemoveVowelTestSubject,
    MergeStringsTestSubject,
    MPITestSubjectFactory,
)
from debugging_framework.tools import Tool
from debugging_framework.evaluator import Evaluation

from debugging_framework.tools import InputsFromHellEvaluationFuzzer

from tools import EvoGFuzzEvaluationTool


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:  %(message)s")

    tools: List[Type[Tool]] = [InputsFromHellEvaluationFuzzer, EvoGFuzzEvaluationTool]

    subjects = MPITestSubjectFactory(
        [
            NPrTestSubject,
            SquareRootTestSubject,
            GCDTestSubject,
            SieveOfEratosthenesTestSubject,
            MiddleTestSubject,
            BubbleSortTestSubject,
            PalindromeTestSubject,
            RemoveVowelTestSubject,
            MergeStringsTestSubject,
            FibonacciTestSubject,
        ]
    ).build()

    Evaluation(
        tools=tools,
        subjects=subjects,
        repetitions=1,
        timeout=3600,
        out_file="./results.pkl",
    ).run()


if __name__ == "__main__":
    exit(main())
