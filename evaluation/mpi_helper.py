import importlib.util
import sys
from typing import Union, Type, List, Callable, Dict, Tuple, Set
from pathlib import Path
from abc import ABC
import string
from fuzzingbook.Coverage import Coverage, Location, BranchCoverage

from fuzzingbook.Grammars import Grammar
from evogfuzz.oracle import OracleResult
from evogfuzz.oracle_construction import construct_oracle


class TestSubject:
    def __init__(self, grammar=None, oracle=None, test_inputs=None):
        self.grammar = grammar or self.default_grammar
        self.oracle = oracle or self.default_oracle()
        self.test_inputs = test_inputs or self.default_test_inputs

    default_grammar = {}
    default_test_inputs = []

    def default_oracle(self):
        raise ValueError("Default Oracle not implemented")

    def to_dict(self):
        return {
            "grammar": self.grammar,
            "oracle": self.oracle,
            "initial_inputs": self.test_inputs,
        }


class MPITestSubject(TestSubject, ABC):
    base_path: str
    implementation_class_name: str = "Solution"
    implementation_function_name: str

    def __init__(self, oracle, bug_id):
        super().__init__(oracle=oracle)
        self.bug_id = bug_id

    @classmethod
    def ground_truth(cls) -> Callable:
        solution_file_path = cls.base_path / Path("reference1.py")
        return load_module_dynamically(
            solution_file_path,
            cls.implementation_class_name,
            cls.implementation_function_name,
        )

    def get_implementation(self) -> Callable:
        imp_file_path = self.base_path / Path(f"prog_{self.bug_id}/buggy.py")

        func = load_module_dynamically(
            imp_file_path,
            self.implementation_class_name,
            self.implementation_function_name,
        )

        def harness_function(inp: str):
            param = list(map(int, str(inp).strip().split()))
            return func(*param)

        return harness_function


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


class MPITestSubjectFactory:
    def __init__(self, test_subject_type: Type[MPITestSubject]):
        self.test_subject_type = test_subject_type

    def build(
        self,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
    ) -> List[MPITestSubject]:
        subjects = []
        for i in range(1, 11):
            buggy_file_path = self.test_subject_type.base_path / Path(
                f"prog_{i}/buggy.py"
            )
            loaded_function = load_module_dynamically(
                buggy_file_path,
                self.test_subject_type.implementation_class_name,
                self.test_subject_type.implementation_function_name,
            )
            error_def = err_def or {TimeoutError: OracleResult.UNDEF}
            def_oracle = default_oracle or OracleResult.BUG
            oracle = construct_oracle(
                loaded_function,
                self.test_subject_type.ground_truth(),
                error_def,
                default_oracle_result=def_oracle,
                timeout=0.01,
            )
            subjects.append(self.test_subject_type(oracle=oracle, bug_id=i))
        return subjects


def load_module_dynamically(
    path: Union[str, Path], class_name: str, function_name: str
):
    # Step 1: Convert file path to module name
    file_path = str(path.absolute())
    module_name = file_path.replace("/", ".").rstrip(".py")

    # Step 2: Load module dynamically
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    your_class = getattr(module, class_name)
    function = getattr(your_class(), function_name)

    return function


def population_coverage(
    population: List[Tuple[int, int]], function: Callable
) -> Tuple[Set[Location], List[int]]:
    cumulative_coverage: List[int] = []
    all_coverage: Set[Location] = set()

    for s in population:
        with Coverage() as cov:
            try:
                function(s)
            except:
                pass
        filtered_set = {
            (func, line)
            for (func, line) in cov.coverage()
            if "derivation_tree" not in func and "input" not in func
        }
        all_coverage |= filtered_set
        cumulative_coverage.append(len(all_coverage))

    return all_coverage, cumulative_coverage


def population_branch_coverage(
    population: List[Tuple[int, int]], function: Callable
) -> Tuple[Set[Location], List[int]]:
    cumulative_coverage: List[int] = []
    all_coverage: Set[Location] = set()

    for s in population:
        with BranchCoverage() as cov:
            try:
                function(s)
            except:
                pass
        filtered_set = {
            (x, y)
            for (x, y) in cov.coverage()
            if "derivation_tree" not in x[0] and y[0] and "input" not in x[0] and y[0]
        }
        all_coverage |= filtered_set
        cumulative_coverage.append(len(all_coverage))

    return all_coverage, cumulative_coverage


def main():
    subjects = MPITestSubjectFactory(MiddleTestSubject).build()
    for subject in subjects:
        param = subject.to_dict()
        orc = subject.get_implementation()
        print(population_coverage(param.get("initial_inputs"), orc))


if __name__ == "__main__":
    main()
