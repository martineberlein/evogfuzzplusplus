import string
import os

from fuzzingbook.Grammars import srange, Grammar


grammar_pysnooper: Grammar = {
    "<start>": ["<options>"],
    "<options>": [
        "<output><variables><depth><prefix><watch><custom_repr><overwrite><thread_info>"
    ],
    "<output>": ["-o\n", "-o<path>\n", ""],
    "<variables>": ["-v<variable_list>\n", ""],
    "<depth>": ["-d<int>\n", ""],
    "<prefix>": ["-p<str>\n", ""],
    "<watch>": ["-w<variable_list>\n", ""],
    "<custom_repr>": ["-c<predicate_list>\n", ""],
    "<overwrite>": ["-O\n", ""],
    "<thread_info>": ["-T\n", ""],
    "<path>": ["<location>", "<location>.<str>"],
    "<location>": ["<str>", os.path.join("<path>", "<str>")],
    "<variable_list>": ["<variable>", "<variable_list>,<variable>"],
    "<variable>": ["<name>", "<variable>.<name>"],
    "<name>": ["<letter><chars>"],
    "<chars>": ["", "<chars><char>"],
    "<letter>": srange(string.ascii_letters),
    "<digit>": srange(string.digits),
    "<char>": ["<letter>", "<digit>", "_"],
    "<int>": ["<nonzero><digits>", "0"],
    "<digits>": ["", "<digits><digit>"],
    "<nonzero>": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "<str>": ["<char><chars>"],
    "<predicate_list>": ["<predicate>", "<predicate_list>,<predicate>"],
    "<predicate>": ["<p_function>=<t_function>"],
    "<p_function>": ["int", "str", "float", "bool"],
    "<t_function>": ["repr", "str", "int"],
}
