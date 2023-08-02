from typing import Dict, Set

from evogfuzz.input import Input

class Failure:

    def __init__(self, exception: Exception):
        self.exception =  exception
        self.message = str(exception)

    def __hash__(self):
        return hash(type(self.exception)) + hash(self.message)

    def __eq__(self, other):
        if not isinstance(other, Failure):
            return False
        return type(other.exception) == type(self.exception) and other.message == self.message

    def __repr__(self):
        return f"{type(self.exception).__name__}: {self.message}"

    def __str__(self):
        return self.__repr__()

class FailureReport:

    def __int__(self):
        self.failures: Dict[Failure, Set[Input]] = dict()

    def add_failure(self, exception: Exception, test_input: Input):






if __name__ == "__main__":
    f1 = Failure(NotImplementedError("zero division error"))
    f2 = Failure(NotImplementedError("zero division error"))
    f3 = Failure(NotImplementedError("float zero division error"))
    assert f1 == f2
    assert f1 != f3
    assert hash(f1) == hash(f2)
    assert hash(f1) != hash(f3)
