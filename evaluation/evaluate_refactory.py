from typing import List, Type

from tools import Tool, InputsFromHellEvaluationFuzzer, EvoGFuzzEvaluationTool
from subjects import (
    Question1RefactoryTestSubject,
    RefactoryTestSubjectFactory,
    RefactoryTestSubject,
    population_coverage,
    population_branch_coverage,
)


def main():
    mpi_subject_types: List[Type[RefactoryTestSubject]] = [
        Question1RefactoryTestSubject
    ]

    tools: List[Type[Tool]] = [
        InputsFromHellEvaluationFuzzer,
        EvoGFuzzEvaluationTool
    ]

    for subject_type in mpi_subject_types:
        subjects = RefactoryTestSubjectFactory(subject_type).build(solution_type="correct")
        for i, subject in enumerate(subjects):
            print("Eval for subject:", subject.__class__.__name__, i, "\n\n")

            param = subject.to_dict()
            for tool in tools:
                tool = tool(**param)
                report = tool.run()
                print(report)
                # print(f"Generated {len(tool.generated_inputs)} inputs.")
                # all_, cum_ = population_coverage(
                #     tool.generated_inputs, subject.get_implementation()
                # )
                # print(f"Achieved coverage {len(all_)}")
                # all_, cum_ = population_branch_coverage(
                #     tool.generated_inputs, subject.get_implementation()
                # )
                # print(f"Achieved branch coverage {len(all_)}")
                print("\n\n")


if __name__ == "__main__":
    exit(main())

    # Same Errors -> EvoGFuzz more Failing Inputs -> DownStream Applications
