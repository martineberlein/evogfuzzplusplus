from evogfuzz_formalizations.calculator import prop, grammar_alhazen as grammar, initial_inputs
from evogfuzz import EvoGFuzz

import logging


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s:  %(message)s"
    )

    evo = EvoGFuzz(grammar=grammar, oracle=prop, inputs=initial_inputs)

    bugs = evo.fuzz()
    for inp in bugs:
        print(inp, inp.oracle)

