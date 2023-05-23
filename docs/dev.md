# EvoGFuzz

To use EvoGFuzz you need three things:
- a program under test (your subject you want to _fuzz_)
- a grammar - the input format specification of your program, and
- an oracle - a function that defines whenever a failure occurred

## Program Under Test

```python3
from evogfuzz.input import Input
from evogfuzz.oracle import OracleResult

def oracle(inp: Input) -> OracleResult:
    def your_program(test_input: str):
        # Run your Program with the input
        raise NotImplementedError
    
    try:
        your_program(str(inp))
        # If you program does not raise an Exception everything seems fine
        return OracleResult.NO_BUG
    except NotImplementedError as e:
        return OracleResult.BUG
    return OracleResult.UNDEF
```

## Defining a Grammar

```python3
from fuzzingbook.Grammars import Grammar, is_valid_grammar

grammar: Grammar = {
    "<start>": ["<number>"],
    "<number>": [str(i) for i in range(0, 10)]
}

assert is_valid_grammar(grammar)
```