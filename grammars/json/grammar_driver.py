#!/usr/bin/env python3

from pathlib import Path
import os
import shutil


class Grammar:

    def grammar_name(self):
        return "json_noregex"

    def seed_location(self):
        return Path(__file__).parent / "seeds"

    def seed_files(self):
        yield Path(__file__).parent / "seeds" / "5038.json"
        yield Path(__file__).parent / "seeds" / "5363.json"
        yield Path(__file__).parent / "seeds" / "6478.json"
        yield Path(__file__).parent / "seeds" / "1390.json"
        yield Path(__file__).parent / "seeds" / "2202.json"
        yield Path(__file__).parent / "seeds" / "5363.json"

    def bnf_location(self):
        return False

    def file_extension(self):
        return "json"

    def create_countin_grammar(self):
        return False

    def grammar_setup(self, copy_directory):
        grammar_files = Path(__file__).parent / "antlrParser"

        src_files = os.listdir(grammar_files)
        for file_name in src_files:
            full_file_name = os.path.join(grammar_files, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, copy_directory)

    def start_rule(self):
        return "start"


if __name__ == "__main__":
    grammar = Grammar()
    iterator = grammar.seed_files()

    for i in iterator:
        print(i)
