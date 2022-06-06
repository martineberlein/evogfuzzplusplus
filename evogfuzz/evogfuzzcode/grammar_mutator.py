
import os
import random
from random import randrange
import logging

'''
This function is used to mutate a selected grammar rule.
During each generation one production rule is randomly chosen.
The mutation is applied to the probabilities of the individual alternatives of a grammar rule. These probabilities
are set to random numbers between 0 (exclusive) and 1. Furthermore the probabilities are normalized so that the sum of
all alternatives is equal to 1.
'''


class Mutator:

    def __init__(self, working_dir):
        self.__working_dir = working_dir

    def mutate(self, current_generation):
        logging.info("Mutating grammar...")
        next_generation = current_generation + 1

        line_number = 0
        production_rule = ""
        string_before = ""
        string_after = ""

        # Remove all empty lines between the production rules of the prob. grammar
        self.__remove_empty_lines(os.path.join(self.__working_dir, "test-cases", "run-" + str(next_generation)) +
                                  "/bnfGrammar-" + str(next_generation) + ".bnf")

        with open(os.path.join(self.__working_dir, "test-cases", "run-" + str(next_generation)) + "/bnfGrammar-" +
                  str(next_generation) + ".bnf") as f:
            lines = f.readlines()
            f.seek(0)
            # Count line numbers
            for line in f:
                if line.strip():
                    line_number += 1

            f.seek(0)

            # Select a random production rule that will be mutated.
            # The production rule must have at least two alternatives
            terminator = 0
            random_rule = -1
            while terminator == 0:
                random_rule = randrange(1, line_number)
                if "@@" in lines[random_rule]:
                    terminator = 1

            logging.info("Mutating Production Rule {}...".format(random_rule))

            # Separate the chosen rule from the rest of the grammar
            for i in range(line_number):
                if i < random_rule:
                    string_before += f.readlines()[i]
                    f.seek(0)
                elif i > random_rule:
                    string_after += f.readlines()[i]
                    f.seek(0)
                else:
                    production_rule = f.readlines()[i]
                    f.seek(0)

            alternatives = self.__split_rule(production_rule)

        # Set new probabilities for the production rule
        new_probabilities = self.__derive_new_probabilities(len(alternatives) // 2)
        count = 0

        new_line = [0] * len(alternatives)
        new_production_rule = ""

        # Combine the probabilities with the alternatives
        # This has to be conforming to the semantics of the grammar file
        for i in range(len(alternatives)):
            if i % 2 == 0:
                new_line[i] = str(alternatives[i]) + " @@ "
                new_production_rule += str(alternatives[i]) + " @@ "
            else:
                if i == len(alternatives) - 1:
                    new_production_rule += str(new_probabilities[count]) + ";\n"
                else:
                    new_production_rule += str(new_probabilities[count]) + " |"
                    count += 1

        # New mutated grammar
        mutated_grammar = string_before + new_production_rule + string_after

        with open(os.path.join(self.__working_dir, "test-cases", "run-" + str(next_generation)) + "/bnfGrammar-" +
                  str(next_generation) + ".bnf", "w") as f:
            f.write(mutated_grammar)
            f.close()

        print("--------------------------------------------------------------------------------")

    '''
    This function is used to produce the random normalized probabilities for a mutated grammar rule.
    '''
    def __derive_new_probabilities(self, n):
        new_probabilities = [0] * n
        probabilities_sum = 0

        for i in range(n):
            new_probabilities[i] = random.randint(1, 100)
            probabilities_sum += new_probabilities[i]

        # Normalize all probabilities
        for i in range(n):
            new_probabilities[i] = new_probabilities[i] / probabilities_sum

        return new_probabilities

    '''
    This function removes all empty lines in a given grammar file.
    The idea is that each line in a grammar file corresponds to a production rule.
    '''
    def __remove_empty_lines(self, filename):

        if not os.path.isfile(filename):
            print("{} does not exist ".format(filename))
            return
        with open(filename) as file:
            lines = file.readlines()

        with open(filename, 'w') as file:
            lines = filter(lambda x: x.strip(), lines)
            file.writelines(lines)

    '''
    This function splits a production rule into its individual alternatives
    separated by a '@@'.
    '''
    def __split_rule(self, production_rule):
        original_rule = production_rule
        alternatives = []
        i = 0
        while i == 0:
            temp = original_rule.split('@@', 1)
            alternatives.append(temp[0])
            if "@@" in temp[1]:
                temp = temp[1].split(" | ", 1)
                alternatives.append(temp[0])
                original_rule = temp[1]
            else:
                i = 1
                alternatives.append(temp[1])

        return alternatives
