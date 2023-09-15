from typing import Optional, Dict
from abc import ABC, abstractmethod

class EvaluationSubject(ABC):
    def __init__(self, grammar, oracle, initial_inputs):
        self.grammar = grammar
        self.oracle = oracle
        self.initial_inputs = initial_inputs

    @staticmethod
    def default_param():
        return {"max_iterations": 10, "timeout": 3600, "log": True}

    def get_evaluation_config(self, default_param: Optional[Dict]=None):
        param = self.default_param().copy()
        if default_param:
            param = default_param
        param.update(
            {
                "grammar": self.grammar,
                "oracle": self.oracle,
                "initial_inputs": self.initial_inputs,
            }
        )
        return param

    @classmethod
    def build(cls) -> 'EvaluationSubject':
        raise NotImplementedError
