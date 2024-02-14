from debugging_framework.tools import GrammarBasedEvaluationFuzzer, InputsFromHellEvaluationFuzzer, ISLaGrammarEvaluationFuzzer
#EvoGFuzzEvaluationTool muss noch ins framework implementiert werden
from evaluate_calculator import EXPR_GRAMMAR as calc_grammar, oracle as calc_oracle, initial_inputs as calc_initial_inputs



if __name__ == "__main__":
    tools = [
        GrammarBasedEvaluationFuzzer,
        InputsFromHellEvaluationFuzzer,
        ISLaGrammarEvaluationFuzzer,
        EvoGFuzzEvaluationTool
    ]

    subjects = [
        ("Calculator", calc_grammar, calc_oracle, calc_initial_inputs)
    ]

    for subject in subjects:
        name, *param = subject
        # VLOGGER.info(f"Evaluating Subject {name}")
        for evaluation_tool in tools:
            tool = evaluation_tool(*param)
            print(tool.run(), end="\n\n")
