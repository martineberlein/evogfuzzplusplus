from typing import List, Type

from subject import EvaluationSubject
from tools import Tool, GrammarBasedEvaluationFuzzer, InputsFromHellEvaluationFuzzer, EvoGFuzzEvaluationTool,ISLaGrammarEvaluationFuzzer
from evaluate_calculator import CalculatorSubject
from subject import Pysnooper2Tests4pyEvaluationSubject


if __name__ == "__main__":

    subjects: List[Type[EvaluationSubject]] = [
        Pysnooper2Tests4pyEvaluationSubject,
    ]

    tools: List[Type[Tool]] = [
        #GrammarBasedEvaluationFuzzer,
        InputsFromHellEvaluationFuzzer,
        #ISLaGrammarEvaluationFuzzer,
        EvoGFuzzEvaluationTool
    ]

    default_param = {"max_iterations": 20, "timeout": 3600, "log": True, "max_nonterminals": 5, "max_generated_inputs": 10000}

    results = dict()
    for subject in subjects:
        print(subject.__name__)
        subject = subject()
        param = subject.get_evaluation_config(default_param)

        print(param)
        for tool in tools:
            tool = tool(**param)
            print(tool.run(), end="\n\n")