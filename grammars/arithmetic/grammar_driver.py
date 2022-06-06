#!/usr/bin/env python3

from pathlib import Path


class Grammar:

    def seed_files(self):
        yield Path(__file__).parent / "seeds" / "seed_1.txt"
        yield Path(__file__).parent / "seeds" / "seed_2.txt"

    def bnf_location(self):
        return Path(__file__).parent / "arithmetic.bnf"

    def file_extension(self):
        return "txt"

    def __create_countin_grammar(self):
        return True


if __name__ == "__main__":
    grammar = Grammar()
    iterator = grammar.seed_files()

    for i in iterator:
        print(i)
