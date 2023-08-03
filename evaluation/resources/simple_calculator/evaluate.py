import sys

from calc.calculator import main

if __name__ == "__main__":
    assert len(sys.argv) == 2
    arg = sys.argv[1]
    #arg = "sin(1)"
    result = main(arg)
    # result = term.evaluate()
    print(result)
