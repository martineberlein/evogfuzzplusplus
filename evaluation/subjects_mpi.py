from typing import Type, List, Callable, Dict
from pathlib import Path
from abc import ABC
import string

from fuzzingbook.Grammars import Grammar
from evogfuzz.oracle import OracleResult
from evogfuzz.oracle_construction import construct_oracle

from subjects import TestSubject, TestSubjectFactory, load_function_from_class


class MPITestSubject(TestSubject, ABC):
    base_path: str
    implementation_class_name: str = "Solution"
    implementation_function_name: str

    def __init__(self, oracle, bug_id):
        super().__init__(oracle=oracle)
        self.bug_id = bug_id

    @classmethod
    def harness_function(cls, input_str: str):
        param = list(map(int, str(input_str).strip().split()))
        return param

    @classmethod
    def ground_truth(cls) -> Callable:
        solution_file_path = cls.base_path / Path("reference1.py")
        return load_function_from_class(
            solution_file_path,
            cls.implementation_class_name,
            cls.implementation_function_name,
        )

    def get_implementation(self) -> Callable:
        imp_file_path = self.base_path / Path(f"prog_{self.bug_id}/buggy.py")

        return load_function_from_class(
            imp_file_path,
            self.implementation_class_name,
            self.implementation_function_name,
        )


class GCDTestSubject(MPITestSubject):
    base_path = Path("./resources/mpi/problem_1_GCD")
    implementation_function_name = "gcd"
    default_grammar: Grammar = {
        "<start>": ["<input>"],
        "<input>": ["<first> <second>"],
        "<first>": ["<integer>"],
        "<second>": ["<integer>"],
        "<integer>": ["<one_nine><maybe_digits>"],
        "<one_nine>": [str(num) for num in range(1, 10)],
        "<digit>": list(string.digits),
        "<maybe_digits>": ["", "<digits>"],
        "<digits>": ["<digit>", "<digit><digits>"],
    }
    default_test_inputs = ["10 2", "4 4"]


class SquareRootTestSubject(MPITestSubject):
    base_path = Path("./resources/mpi/problem_10_Square-root")
    implementation_function_name = "floorSqrt"
    default_grammar: Grammar = {
        "<start>": ["<input>"],
        "<input>": ["<integer>"],
        "<integer>": ["<one_nine><maybe_digits>", "0"],
        "<one_nine>": [str(num) for num in range(1, 10)],
        "<digit>": list(string.digits),
        "<maybe_digits>": ["", "<digits>"],
        "<digits>": ["<digit>", "<digit><digits>"],
    }
    default_test_inputs = ["4", "5"]


class MiddleTestSubject(MPITestSubject):
    base_path = Path("./resources/mpi/problem_7_Middle-of-Three")
    implementation_function_name = "middle"
    default_grammar: Grammar = {
        "<start>": ["<input>"],
        "<input>": ["<first> <second> <third>"],
        "<first>": ["<integer>"],
        "<second>": ["<integer>"],
        "<third>": ["<integer>"],
        "<integer>": ["<one_nine><maybe_digits>"],
        "<one_nine>": [str(num) for num in range(1, 10)],
        "<digit>": list(string.digits),
        "<maybe_digits>": ["", "<digits>"],
        "<digits>": ["<digit>", "<digit><digits>"],
    }
    default_test_inputs = ["978 518 300", "162 934 200"]


class MPITestSubjectFactory(TestSubjectFactory):
    def __init__(self, test_subject_type: Type[MPITestSubject]):
        self.test_subject_type = test_subject_type

    def build(
        self,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
    ) -> List[MPITestSubject]:
        subjects = []

        for i in range(1, 11):
            subject_path = self.test_subject_type.base_path / Path(
                f"prog_{i}/buggy.py"
            )

            try:
                subject = self._build_subject(subject_path, i, err_def, default_oracle)
                subjects.append(subject)
            except Exception as e:
                print(f"Subject {subject_path} could not be built.")

        return subjects


    def _build_subject(
        self,
        subject_path,
        bug_id,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
    ) -> MPITestSubject:

        reference = self.test_subject_type.ground_truth()

        loaded_function = load_function_from_class(
            subject_path,
            self.test_subject_type.implementation_class_name,
            self.test_subject_type.implementation_function_name,
        )

        error_def = err_def or {TimeoutError: OracleResult.UNDEF}
        def_oracle = default_oracle or OracleResult.BUG

        oracle = construct_oracle(
            loaded_function,
            reference,
            error_def,
            default_oracle_result=def_oracle,
            timeout=0.01,
            harness_function=self.test_subject_type.harness_function
        )
        subject = self.test_subject_type(oracle=oracle, bug_id=bug_id)
        return subject


def main():
    subjects = MPITestSubjectFactory(MiddleTestSubject).build()
    for subject in subjects:
        print(subject.ground_truth()(1, 4 ,3))
        param = subject.to_dict()
        implementation = subject.get_implementation()
        print(implementation(1, 4, 3))
        print(subject.oracle("1 4 3"))
        oracle = param.get("oracle")
        for inp in param.get("initial_inputs"):
            print(inp, oracle(inp))


if __name__ == "__main__":
    main()
