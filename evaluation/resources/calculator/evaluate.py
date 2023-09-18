import sys

from expr.parse import parse

if __name__ == "__main__":
    assert len(sys.argv) == 2
    arg = sys.argv[1]
    term = parse(arg)
    result = term.evaluate()
    print(result)
