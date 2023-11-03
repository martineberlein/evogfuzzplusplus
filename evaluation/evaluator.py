from typing import List, Type
import logging

from results import initialize_dataframe
from tools import Tool
from subjects import TestSubject


VLOGGER = logging.getLogger("evaluation")
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s :: %(levelname)-8s :: %(message)s",
)

OUT_FILE = "evo_results.pkl"


class Evaluation:
    def __init__(self, tools, subjects, repetitions, timeout):
        self.tools: List[Type[Tool]] = tools
        self.subjects: List[TestSubject] = subjects
        self.repetitions: int = repetitions
        self.timeout: int = timeout

    def run(self):
        subject_names = [(sub.name, sub.id) for sub in self.subjects]
        tool_names = [tool.name for tool in self.tools]
        df_results = initialize_dataframe(subject_names, tool_names, self.repetitions)

        for subject in self.subjects:
            VLOGGER.info(
                f"Evaluating Subject {subject.__class__.__name__}_{subject.id}"
            )

            param = subject.to_dict()
            for tool in self.tools:
                for i in range(1, self.repetitions + 1):
                    report = tool(**param).run()
                    df_results.at[
                        (i, tool.name), (subject.name, subject.id)
                    ] = report.to_dict()

        VLOGGER.info(f"Saving results to {OUT_FILE}")
        df_results.to_pickle(OUT_FILE)


def main():
    from subjects_mpi import (
        GCDTestSubject,
        SquareRootTestSubject,
        MiddleTestSubject,
        MPITestSubjectFactory,
    )
    from tools import EvoGFuzzEvaluationTool, InputsFromHellEvaluationFuzzer

    subjects = MPITestSubjectFactory(
        [GCDTestSubject, SquareRootTestSubject, MiddleTestSubject]
    ).build()
    tools = [EvoGFuzzEvaluationTool, InputsFromHellEvaluationFuzzer]

    Evaluation(tools=tools, subjects=subjects, repetitions=10, timeout=3600).run()


def main2():
    from subjects_mpi import GCDTestSubject, MPITestSubjectFactory

    subjects = MPITestSubjectFactory([GCDTestSubject]).build()
    for sub in subjects:
        print(sub.name, sub.id)


if __name__ == "__main__":
    main()
