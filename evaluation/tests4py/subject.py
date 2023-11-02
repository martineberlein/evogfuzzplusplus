from typing import Optional, Dict, List, Type
from abc import ABC
from dataclasses import dataclass
from pathlib import Path

from tests4py import api
from tests4py.projects import Project

from evaluation.tests4py.tests4py_api import construct_oracle, DEFAULT_WORK_DIR, build_project
from evogfuzz_formalizations.tests4py import grammar_pysnooper


class EvaluationSubject(ABC):
    max_iteration: int = 10
    timeout: int = 3600
    log: bool = True

    def __init__(self, grammar: Dict, oracle, initial_inputs: List[str]):
        self.grammar = grammar
        self.oracle = oracle
        self.initial_inputs = initial_inputs

    def get_evaluation_config(self, default_param: Optional[Dict] = None) -> Dict:
        default = {
            "max_iterations": self.max_iteration,
            "timeout": self.timeout,
            "log": self.log,
            "grammar": self.grammar,
            "oracle": self.oracle,
            "initial_inputs": self.initial_inputs,
        }

        if default_param:
            default.update(default_param)

        return default


class Tests4PyEvaluationSubject(EvaluationSubject):

    def __init__(self, grammar: Dict, initial_inputs: List[str], project: Project, work_dir: Path= DEFAULT_WORK_DIR):
        oracle = construct_oracle(project=project, work_dir=work_dir)
        super().__init__(grammar, oracle, initial_inputs)
        self.project = project
        self.work_dir = work_dir
        self.setup()

    def setup(self) -> None:
        build_project(self.project, self.work_dir)


@dataclass
class Pysnooper2Tests4pyEvaluationSubject(Tests4PyEvaluationSubject):
    project: Project = api.pysnooper_2
    grammar = grammar_pysnooper
    initial_inputs = ["-d1\n-T\n"]

    def __post_init__(self):
        super().__init__(self.grammar, self.initial_inputs, self.project)


@dataclass
class Pysnooper3Tests4pyEvaluationSubject(Tests4PyEvaluationSubject):
    project: Project = api.pysnooper_3
    grammar = grammar_pysnooper
    initial_inputs = ["-d1\n-ptest\n"]

    def __post_init__(self):
        super().__init__(self.grammar, self.initial_inputs, self.project)


if __name__ == '__main__':
    subjects: List[Type[EvaluationSubject]] = [
        Pysnooper2Tests4pyEvaluationSubject,
        Pysnooper3Tests4pyEvaluationSubject,
    ]

    for subject in subjects:
        print(subject.__name__)
        subject = subject()
        param = subject.get_evaluation_config()
        print(param)

    # print(p.get_evaluation_config())
    # config = p.get_evaluation_config()
    # oracle = config.get("oracle")
    # initial_inputs = config.get("initial_inputs")
    # print(oracle(initial_inputs[0]))
