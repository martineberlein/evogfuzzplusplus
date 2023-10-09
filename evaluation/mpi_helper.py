import importlib.util
import sys
from typing import Union
from pathlib import Path

from fuzzingbook.Grammars import Grammar
import string

from evogfuzz.input import Input
from evogfuzz.oracle import OracleResult
from evogfuzz.oracle_construction import construct_oracle


grammar: Grammar = {
    '<start>': ["<input>"],
    "<input>": ["<first> <second>"],
    "<first>": ["<integer>"],
    "<second>": ["<integer>"],
    "<integer>": ["<onenine><maybe_digits>"],
    "<onenine>": [str(num) for num in range(1, 10)],
    "<digit>": list(string.digits),
    "<maybe_digits>": ["", "<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],
}


class TestSubject:
    def __init__(self, grammar=None, oracle=None, test_inputs=None):
        self.grammar = grammar or self.default_grammar()
        self.oracle = oracle or self.default_oracle()
        self.test_inputs = test_inputs or self.default_test_inputs()

    def default_grammar(self):
        return {}

    def default_oracle(self):
        return None

    def default_test_inputs(self):
        return []

    def to_dict(self):
        return {
            'grammar': self.grammar,
            'oracle': self.oracle,
            'inputs': self.test_inputs,
        }


class GCDTestSubject(TestSubject):
    def default_grammar(self):
        return grammar

    def default_oracle(self):
        error_def = {TimeoutError: OracleResult.UNDEF}
        return construct_oracle(ob.gcd, ref.gcd, error_def, default_oracle_result=OracleResult.BUG)

    def default_test_inputs(self):
        return ["10 2", "4 4"]


def load_module_dynamically(path: Union[str, Path], class_name: str, function_name: str):
    # Step 1: Convert file path to module name
    file_path = str(path)
    module_name = file_path.replace('/', '.').rstrip('.py')

    # Step 2: Load module dynamically
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    your_class = getattr(module, class_name)
    function = getattr(your_class(), function_name)
    return function


def get_gcd_subjects(err_def=None, default_oracle=None):
    subjects = []
    for i in range(1,11):
        result = load_module_dynamically(f'/Users/martineberlein/github/EvoGFuzzplusplus/evaluation/resources/mpi/problem_1_GCD/prog_{i}/buggy.py', 'Solution', 'gcd')
        error_def = err_def or {TimeoutError: OracleResult.UNDEF}
        def_oracle = default_oracle or OracleResult.BUG
        oracle = construct_oracle(result, ref.gcd, error_def, default_oracle_result=def_oracle, timeout=0.01)
        subjects.append(GCDTestSubject(oracle=oracle))
    return subjects