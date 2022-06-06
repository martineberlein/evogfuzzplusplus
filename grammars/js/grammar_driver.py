#!/usr/bin/env python3

from pathlib import Path
import shutil
import os
import glob


class Grammar:

    def grammar_name(self):
        return "JavaScript"

    def seed_location(self):
        return Path(__file__).parent / "seeds"

    def seed_files(self):
        input_files = getAllfiles(str(Path(__file__).parent / "seeds"), self.file_extension())
        return input_files

    def bnf_location(self):
        return False

    def file_extension(self):
        return "js"

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
        return "program"


def getAllfiles(fileLocation, extension):
    files = "*." + extension

    iter_files = fileLocation + "/" + files
    itemlist = glob.glob(iter_files)
    return itemlist


if __name__ == "__main__":
    grammar = Grammar()
    iterator = grammar.seed_files()

    for i in iterator:
        print(i)
