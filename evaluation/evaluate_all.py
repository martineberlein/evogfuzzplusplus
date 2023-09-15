from typing import List, Type

from subject import EvaluationSubject
from tools import Tool, GrammarBasedEvaluationFuzzer, InputsFromHellEvaluationFuzzer, EvoGFuzzEvaluationTool,ISLaGrammarEvaluationFuzzer
from evaluate_calculator import CalculatorSubject


if __name__ == "__main__":

    subjects: List[Type[EvaluationSubject]] = [
        CalculatorSubject,
    ]

    tools: List[Type[Tool]] = [
        #GrammarBasedEvaluationFuzzer,
        InputsFromHellEvaluationFuzzer,
        #ISLaGrammarEvaluationFuzzer,
        EvoGFuzzEvaluationTool
    ]

    default_param = {"max_iterations": 100, "timeout": 3600, "log": True}

    results = dict()
    for subject in subjects:
        param = (subject.
                 build().
                 get_evaluation_config(default_param)
                 )

        for tool in tools:
            tool = tool(**param)
            print(tool.run(), end="\n\n")