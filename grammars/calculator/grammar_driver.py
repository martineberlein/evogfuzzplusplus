#!/usr/bin/env python3

from pathlib import Path


class Grammar:

    def grammar_name(self):
        return "calculator"

    def seed_files(self):
        yield Path(__file__).parent / "seeds" / "seed_1.txt"
        yield Path(__file__).parent / "seeds" / "seed_2.txt"
        yield Path(__file__).parent / "seeds" / "seed_3.txt"
        yield Path(__file__).parent / "seeds" / "seed_4.txt"

    def bnf_location(self):
        return Path(__file__).parent / "calculator.bnf"

    def file_extension(self):
        return "txt"

    def create_countin_grammar(self):
        return True

    def start_rule(self):
        return "start"


if __name__ == "__main__":
    grammar = Grammar()
    iterator = grammar.seed_files()

    for i in iterator:
        print(i)
