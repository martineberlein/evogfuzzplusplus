from abc import ABC, abstractmethod
from typing import Dict, Set, Union
from collections import defaultdict

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


class Report(ABC):

    def __init__(self):
        self.failures: Dict[Failure, Set[Input]] = defaultdict(set)

    @abstractmethod
    def get_failures(self):
        raise NotImplementedError


class FailureReport(Report):

    def add_failure(self, failure: Union[Exception, Failure], test_input: Input):
        if isinstance(failure, Exception):
            failure = Failure(
                failure
            )

        self.failures[failure].add(test_input)

    def get_failures(self):
        return self.failures
