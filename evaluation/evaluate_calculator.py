import math
import string

from fuzzingbook.Grammars import Grammar, srange

from evogfuzz.input import Input
from evogfuzz.oracle import OracleResult
from tools import GrammarBasedEvaluationFuzzer, InputsFromHellEvaluationFuzzer, EvoGFuzzEvaluationTool,ISLaGrammarEvaluationFuzzer
from subject import EvaluationSubject
from mpi_helper import population_coverage, population_branch_coverage

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
    "<function_name>": ["<char>", "<char><function_name>", "sqrt", "tan", "sin", "cos"],
    "<char>": [] + srange(string.ascii_lowercase),
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
        return OracleResult.UNDEF, NameError()
    except Exception as exp:
        return OracleResult.BUG, exp
    else:
        return OracleResult.NO_BUG


class CalculatorSubject(EvaluationSubject):
    name = "Calculator"

    @classmethod
    def build(cls):
        return cls(EXPR_GRAMMAR, oracle, initial_inputs)


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
        print(f"Generated {len(tool.generated_inputs)} inputs.")
