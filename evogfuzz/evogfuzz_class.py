#!/usr/bin/env python3
import os
import tempfile
import subprocess
from pathlib import Path
import pandas
import logging

from evogfuzzcode.counting_grammar import CountingGrammar
from evogfuzzcode.selector import Selector
from evogfuzzcode.grammar_mutator import Mutator
import evogfuzzcode.helper as helper

COUNTING_GRAMMAR_START_RULE = "main_dummy_rule_hope_for_no_collisions"


class Evogfuzz:

    def __init__(self, working_dir, target):
        self.working_dir = working_dir
        self.target = target
        self.__iteration = 0
        self.__max_iterations = 100000
        self.__number_individuals = 100
        self.parameter_lambda = 2
        self.__elitism_rate = 5
        self.__tournament_size = 10
        self.__tournament_number = 10
        self.grammar_name = target.grammar.grammar_name()
        self.__all_data = None
        self.__avg_prev_data = 0

    def execute(self):
        logging.info("Executing EVOGFUZZ for {}".format(self.target.subject()))
        self.initialize()
        while self.__do_more_iterations():
            logging.info("Starting ITERATION {}".format(self.__iteration))
            self.__loop()
            self.__iteration = self.__iteration + 1

    def __loop(self):
        # generate input files
        self.__generate_input_files()
        # execute input files
        exec_data = self.__execute_input_files()
        # determine fitness of individuals
        fitness = self.__determine_fitness(exec_data)
        # select fittest individuals
        fittest_individuals = self.__select_fittest_individuals(fitness)
        # learn new probabilistic grammar
        self.__learn_new_grammar(fittest_individuals)
        # mutate grammar
        self.__check_mutation(fittest_individuals)
        # collect new data
        self.__add_new_data(exec_data, fitness, fittest_individuals)
        # display stats
        # self.__show_stats()

    def __generate_input_files(self):
        current_generation_directory = "run-" + str(self.__iteration)
        grammar_name = "bnfGrammar-" + str(self.__iteration) + ".bnf"
        current_generation_path = os.path.join(self.working_dir, "test-cases", current_generation_directory)

        logging.info("Generating new Input Samples...")
        dev_null = open(os.devnull, 'w')
        subprocess.call(["java", "-Xss1g", "-Xms256m", "-Xmx4g", "-jar", "./inputGenerator/tribble.jar", "generate",
                         "--suffix=." + self.target.grammar.file_extension(),
                         "--mode=15-25-probabilistic-100", "--out-dir=" + current_generation_path + "/samples",
                         "--grammar-file=" + current_generation_path + "/" + str(grammar_name)], stdout=dev_null,
                        stderr=dev_null)

    def __execute_input_files(self):
        logging.info("Executing new Input Samples...")

        input_files_directory = "run-" + str(self.__iteration) + "/samples"
        sample_dir = os.path.join(self.working_dir, "test-cases", input_files_directory)

        return self.execution_function(sample_dir)

    def execution_function(self, samples_dir):
        raise AssertionError("Overwrite in subclass.")

    def __determine_fitness(self, exec_data):
        # Get all input files from the current generation
        input_files = helper.getAllfiles(
            os.path.join(self.working_dir, "test-cases", "run-" + str(self.__iteration), "samples"),
            self.target.grammar.file_extension())

        return self.determine_fitness(input_files, exec_data)

    def determine_fitness(self, input_files, exec_data):
        raise AssertionError("Overwrite in subclass.")

    def __select_fittest_individuals(self, fitness):
        # --> Should not be initialized her!!
        selector = Selector(self.working_dir, self.grammar_name, "n" + self.target.grammar.start_rule(),
                            self.parameter_lambda, self.__tournament_number)

        fittest_individuals = selector.tournament_selection(fitness)
        return fittest_individuals

    def __learn_new_grammar(self, fittest_individuals):

        # If specified append a base file
        # This process is explicitly not necessary and is for debugging purposes only
        # if options.baseFile:
        #    fittest_individuals.append(os.path.join(os.get cwd(), "bnf", "base", "base." + fileExtension))

        list_fittest_individuals = []
        for x in fittest_individuals['file']:
            list_fittest_individuals.append(Path(os.path.join(self.working_dir, "test-cases",
                                                              "run-" + str(self.__iteration), "samples", x)).absolute())

        next_generation = self.__iteration + 1
        new_grammar_name = "bnfGrammar-" + str(next_generation) + ".bnf"
        next_generation_directory = "run-" + str(next_generation)
        os.mkdir(os.path.join(self.working_dir, "test-cases", next_generation_directory), 0o755)
        self.__create_probabilistic_grammar(list_fittest_individuals, new_grammar_name,
                                            os.path.join(self.working_dir, "test-cases", next_generation_directory))

    def __check_mutation(self, fittest_individuals):
        if fittest_individuals['fitness'].mean() <= (self.__avg_prev_data*1.025):
            self.__mutate_grammar()

    def __mutate_grammar(self):
        if self.__iteration > 0:
            mutator = Mutator(self.working_dir)
            mutator.mutate(self.__iteration)

    def __do_more_iterations(self):
        if self.__iteration >= self.__max_iterations:
            return False
        return True

    def initialize(self):
        initial_generation_directory = "run-0"
        self.__setup_working_dir()

        if self.target.grammar.create_countin_grammar():
            self.__initialize_counting_grammar()
        else:
            output_dir = str(os.path.join(self.working_dir, "grammar", "antlrParser"))
            self.target.grammar.grammar_setup(output_dir)

        os.mkdir(os.path.join(self.working_dir, "test-cases", initial_generation_directory), 0o755)
        new_grammar_name = "bnfGrammar-0" + ".bnf"
        # initial_input_files = helper.getAllfiles(self.target., self.target.grammar.file_extension())
        initial_input_files = self.target.grammar.seed_files()

        new_dir = os.path.join(self.working_dir, "test-cases", initial_generation_directory)

        self.__create_probabilistic_grammar(initial_input_files, new_grammar_name, new_dir)

    def __initialize_counting_grammar(self):
        counting_grammar = CountingGrammar(self.working_dir, self.target.grammar.bnf_location(), self.grammar_name)
        counting_grammar.setup_counting_grammar()

    def __setup_working_dir(self):
        os.mkdir(os.path.join(self.working_dir, "test-cases"), 0o755)
        os.mkdir(os.path.join(self.working_dir, "grammar"), 0o755)
        os.mkdir(os.path.join(self.working_dir, "grammar", "antlrParser"), 0o755)

    def __create_probabilistic_grammar(self, seeds, grammar_name, directory):
        logging.info("Learning new probabilistic grammar...")
        main_directory = os.getcwd()

        dev_null = open(os.devnull, 'w')
        os.chdir(os.path.join(self.working_dir, "grammar", "antlrParser"))
        with open(os.path.join(directory, grammar_name), "w") as outputGrammar,\
                tempfile.NamedTemporaryFile(mode="w") as tempSampleFile:
            for file in seeds:
                with open(file, "r") as f:
                    tempSampleFile.writelines(f.readlines())
                    f.close()

            tempSampleFile.seek(0)

            subprocess.call(["java", "org.antlr.v4.gui.TestRig", self.grammar_name, COUNTING_GRAMMAR_START_RULE],
                            stdin=tempSampleFile, stdout=outputGrammar, stderr=dev_null)

        outputGrammar.close()
        tempSampleFile.close()
        os.chdir(main_directory)

    def __add_new_data(self, exec_data, fitness, fittest_individuals):
        joined_data = exec_data.set_index("file") \
            .join(fitness.set_index("file"), how='outer') \
            .reset_index()

        joined_data['Iteration'] = self.__iteration

        # All fitness data
        fitness_csv = Path(self.working_dir) / "fitness.csv"
        self.__write_to_csv(joined_data, fitness_csv)

        # Best fitness data
        fitness_csv = Path(self.working_dir) / "fitness_best.csv"
        self.__write_to_csv(fittest_individuals.sort_values(by='fitness', ascending=False).head(1), fitness_csv)

        # All data
        if self.__all_data is None:
            self.__all_data = joined_data
        else:
            self.__all_data = pandas.concat([self.__all_data, joined_data], sort=False)

        # Avg fitness of best individuals (Used for Mutation Phase)
        self.__avg_prev_data = fittest_individuals['fitness'].mean()

    def __write_to_log(self, data):
        fitness_log = Path(self.working_dir).parent / "fitness.log"
        with open(fitness_log, 'a+') as log:
            log.write(" ".join(data.to_csv(index=False)))
            log.write("\n")
            log.flush()

    def __write_to_csv(self, data, csv):
        data.to_csv(str(csv), mode='a', header=False)

    def __finalize_data(self):
        raise AssertionError("TODO")
        # --> csv Export
