import importlib.util
import sys
from typing import Union, List, Callable, Tuple, Set
from pathlib import Path
from abc import ABC, abstractmethod

from fuzzingbook.Coverage import Coverage, Location, BranchCoverage


class TestSubject(ABC):
    name: str
    id: int

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


class TestSubjectFactory(ABC):
    @abstractmethod
    def build(self) -> List[TestSubject]:
        raise NotImplementedError


def load_module_dynamically(path: Union[str, Path]):
    # Step 1: Convert file path to module name
    file_path = str(path.absolute())
    module_name = file_path.replace("/", ".").rstrip(".py")

    # Step 2: Load module dynamically
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return module


def load_object_dynamically(path: Union[str, Path], object_name: str):
    module = load_module_dynamically(path)
    return getattr(module, object_name)


def load_function_from_class(
    path: Union[str, Path], class_name: str, function_name: str
):
    class_ = load_object_dynamically(path, class_name)
    function = getattr(class_(), function_name)

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
