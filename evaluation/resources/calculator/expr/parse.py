from typing import List

# noinspection PyUnresolvedReferences
from .arithmetic import (
    Constant,
    Term,
    Add,
    Neg,
    Sub,
    Mul,
    Div,
)


def parse(s: str):
    s = s.replace("(", " ( ")
    s = s.replace(")", " ) ")
    while "  " in s:
        s = s.replace("  ", " ")
    s = s.strip()
    tokens = list(reversed(s.split(" ")))
    assert tokens
    term = parse_add_sub(tokens)
    assert not tokens
    return term


def parse_terminal(tokens) -> Term:
    token = tokens.pop(0)
    if token.isnumeric():
        return Constant(int(token))
    elif token == ")":
        term = parse_add_sub(tokens)
        token = tokens.pop(0)
        assert token == "("
        return term
    else:
        assert False


def parse_neg(tokens) -> Term:
    term = parse_terminal(tokens)
    if tokens and tokens[0] in "~":
        tokens.pop(0)
        return Neg(term)
    else:
        return term


def parse_mul_div(tokens: List[str]) -> Term:
    term = parse_neg(tokens)
    if tokens and tokens[0] in "*/":
        token = tokens.pop(0)
        if token == "*":
            return Mul(parse_mul_div(tokens), term)
        else:
            return Div(parse_mul_div(tokens), term)
    else:
        return term


def parse_add_sub(tokens: List[str]) -> Term:
    term = parse_mul_div(tokens)
    if tokens and tokens[0] in "+-":
        token = tokens.pop(0)
        if token == "+":
            return Add(parse_add_sub(tokens), term)
        else:
            return Sub(parse_add_sub(tokens), term)
    else:
        return term
