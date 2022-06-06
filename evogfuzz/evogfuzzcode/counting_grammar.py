import os
import subprocess
import glob
from shutil import copyfile

'''
    Backlog: 
    
    Path to Tribble is absolute --> change

'''


class CountingGrammar:
    def __init__(self, working_dir, grammar_path, grammar_name):
        self.working_dir = working_dir
        self.grammar_path = grammar_path
        self.grammar_name = grammar_name
        self.path_to_new_grammar = os.path.join(working_dir, "grammar", "antlrParser")

    def setup_counting_grammar(self):
        print("Creating Counting Grammar")
        path_to_grammar = os.path.join(self.working_dir, "grammar", "countingGrammar")
        os.mkdir(path_to_grammar, 0o755)

        output_counting_grammar = os.path.join(path_to_grammar, self.grammar_name+".g4")
        self.create_counting_grammar(output_counting_grammar)

    def create_counting_grammar(self, output_counting_grammar):
        f = open(output_counting_grammar, "w")
        header = "countingGrammar"
        f.write(header)

        subprocess.call(["java", "-jar", "./tools/countingGrammar.jar", self.grammar_path], stdout=f)

        copyfile(output_counting_grammar, os.path.join(self.path_to_new_grammar, self.grammar_name + ".g4"))
        self.compile_counting_grammar()

    def compile_counting_grammar(self):
        print("Creating ANTLR Parser")
        subprocess.call(["java", "org.antlr.v4.Tool",
                         os.path.join(self.path_to_new_grammar, self.grammar_name + ".g4")])

        java_files = glob.glob(self.path_to_new_grammar + "/*.java")
        arguments = ["javac"] + java_files
        subprocess.call(arguments)
