import string
import math
from fuzzingbook.Grammars import Grammar
from fuzzingbook.Parser import DerivationTree


GRAMMAR: Grammar = {
    "<start>": ["<arith_expr>"],
    "<arith_expr>": ["<function>(<number>)"],
    "<function>": ["sqrt", "sin", "cos", "tan"],
    "<number>": ["<maybe_minus><onenine><maybe_digits><maybe_frac>"],
    "<maybe_minus>": ["", "-"],
    "<onenine>": [str(num) for num in range(1, 10)],
    "<digit>": list(string.digits),
    "<maybe_digits>": ["", "<digits>"],
    "<digits>": ["<digit>", "<digit><digits>"],
    "<maybe_frac>": ["", ".<digits>"]
}


INITIAL_INPUTS = ['cos(10)', 'sqrt(28367)', 'tan(-12)', 'sqrt(3)']


def _arith_eval(inp: DerivationTree) -> float:
    return eval(str(inp), {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan})


def prop(inp: DerivationTree) -> bool:
    """
    Evaluation function, that returns 'True' when the calculator fails.
    :param inp:
    :return:
    """
    try:
        _arith_eval(inp)
        return False
    except ValueError:
        return True
