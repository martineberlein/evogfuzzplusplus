import math
import string

from debugging_framework.types import Grammar
from debugging_framework.oracle import OracleResult
from debugging_framework.tools import GrammarBasedEvaluationFuzzer, InputsFromHellEvaluationFuzzer, ISLaGrammarEvaluationFuzzer
#kam ursprünglich aus tools.py in diesem folder EvoGFuzzEvaluationTool ist noch nicht im debugging_framework -> wird aber gerade implementiert


from evogfuzz.input import Input

EXPR_GRAMMAR: Grammar = {
    "<start>": ["<expr>"],
    "<expr>": ["<term> + <expr>", "<term> - <expr>", "<term>"],
    "<term>": [
        "<factor> * <term>",
        "<factor> / <term>",
        "<factor>",
        "<function_name>(<expr>)",
    ],
    "<factor>": [
        "+<factor>",
        "-<factor>",
        "(<expr>)",
        "<integer>.<integer>",
        "<integer>",
    ],
    "<function_name>": ["<char>", "<char><function_name>"],
    "<char>": [c for c in string.ascii_lowercase],
    "<integer>": ["<digit><integer>", "<digit>"],
    "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
}

initial_inputs = ["1 / 2", "sqrt(4)", "tan(1)", "sin(-13)", "1 - 1"]

def oracle(test_input: Input):
    try:
        eval(
            str(test_input),
            {"sqrt": math.sqrt, "cos": math.cos, "sin": math.sin, "tan": math.tan},
        )
    except NameError:
        return OracleResult.UNDEFINED, NameError()
    except Exception as exp:
        return OracleResult.FAILING, exp
    else:
        return OracleResult.PASSING


if __name__ == "__main__":
    tools = [
        GrammarBasedEvaluationFuzzer,
        InputsFromHellEvaluationFuzzer,
        ISLaGrammarEvaluationFuzzer,
        EvoGFuzzEvaluationTool
    ]

    param = [EXPR_GRAMMAR, oracle, initial_inputs]

    for evaluation_tool in tools:
        tool = evaluation_tool(*param)
        print(tool.run(), end="\n\n")
