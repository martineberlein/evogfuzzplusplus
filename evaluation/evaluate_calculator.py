import math
import string

from fuzzingbook.Grammars import Grammar, srange
from fuzzingbook.GrammarFuzzer import GrammarFuzzer

from evogfuzz.evogfuzz_class import EvoGFuzz
from evogfuzz.input import Input
from evogfuzz.oracle import OracleResult
from evogfuzz.report import MultipleFailureReport
from evogfuzz.execution_handler import SingleExecutionHandler

EXPR_GRAMMAR: Grammar = {
    "<start>":
        ["<expr>"],

    "<expr>":
        ["<term> + <expr>", "<term> - <expr>", "<term>"],

    "<term>":
        ["<factor> * <term>", "<factor> / <term>", "<factor>", "<function_name>(<expr>)"],

    "<factor>":
        ["+<factor>",
         "-<factor>",
         "(<expr>)",
         "<integer>.<integer>",
         "<integer>"],

    "<function_name>":
        [
            "<char>", "<char><function_name>"
        ],

    "<char>":
        [
        ] + srange(string.ascii_lowercase),

    "<integer>":
        ["<digit><integer>", "<digit>"],

    "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

def oracle(test_input: Input):
    try:
        eval(str(test_input), {"sqrt": math.sqrt, "cos": math.cos, "sin": math.sin, "tan": math.tan})
    except NameError:
        return OracleResult.UNDEF, NameError()
    except Exception as exp:
        return OracleResult.BUG, exp
    else:
        return OracleResult.NO_BUG

def grammar_fuzzer():
    fuzzer = GrammarFuzzer(EXPR_GRAMMAR, max_nonterminals=5)
    report = MultipleFailureReport(name="Grammar-Based Fuzzing")
    execution_handler = SingleExecutionHandler(oracle)

    test_inputs = set()
    for _ in range(10000):
        test_inputs.add(fuzzer.fuzz())

    execution_handler.label_strings(test_inputs, report)
    print(report)


def inputs_from_hell():

    prob_grammar = ProbabilisticGrammarMiner(EarleyParser(EXPR_GRAMMAR)).mine_probabilistic_grammar(
        inputs=["1 / 2", "sqrt(4)", "tan(1)", "sin(-13)", "1 - 1"]
    )

    fuzzer = ProbabilisticGrammarFuzzer(prob_grammar, max_nonterminals=5)
    report = MultipleFailureReport(name="Inputs-From-Hell Fuzzing")
    execution_handler = SingleExecutionHandler(oracle)

    test_inputs = set()
    for _ in range(10000):
        test_inputs.add(fuzzer.fuzz())

    execution_handler.label_strings(test_inputs, report)
    print(report)


if __name__ == "__main__":
    grammar_fuzzer()
    inputs_from_hell()


    evo = EvoGFuzz(
        grammar=EXPR_GRAMMAR,
        oracle=oracle,
        inputs=["1 / 2", "sqrt(4)", "tan(1)", "sin(-13)", "1 - 1"],
        iterations=300,
        transform_grammar=True
    )

    found_exceptions = evo.fuzz()

    report = evo.report
    print(report)