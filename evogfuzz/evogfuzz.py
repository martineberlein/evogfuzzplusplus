#!/usr/bin/env python3
from __future__ import print_function
from __future__ import division

import os
import optparse
from pathlib import Path
from datetime import datetime

import logging
from evogfuzz_class import Evogfuzz
from evogfuzzcode import fitness_function, subject_class

VERSION = "1.1"
COUNTING_GRAMMAR_START_RULE = "main_dummy_rule_hope_for_no_collisions"


class FunctionalEvoGFuzz(Evogfuzz):
    EVOGFUZZ_TYPE = "functional"

    def execution_function(self, samples_dir):
        exec_data = self.target.execute_samples_dir(samples_dir)
        return exec_data

    def determine_fitness(self, input_files, exec_data):
        return fitness_function.determine_fittest_individuals(self.working_dir, input_files, exec_data,
                                                              self.grammar_name, self.target.grammar.start_rule(),
                                                              self.parameter_lambda)


class NonFunctionalEvoGFuzz(Evogfuzz):
    EVOGFUZZ_TYPE = "non-functional"

    def execution_function(self, samples_dir):
        exec_data = self.target.non_func_exec_samples(samples_dir)
        return exec_data

    def determine_fitness(self, input_files, exec_data):
        return fitness_function.calculate_fitness_executionTime(input_files, exec_data)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s:  %(message)s"
    )

    # Parser Options
    parser = optparse.OptionParser()
    parser.add_option("-y", "--output", type="string", dest="output")
    parser.add_option("-z", "--target", type="string", dest="target")
    parser.add_option("-n", "--nonfunctional", dest="nonfunctional", help='Use non-functional EvoGFuzz.',
                      default=False, action="store_true")

    (options, args) = parser.parse_args()

    subject_driver = Path(options.target).absolute()
    subject = subject_class.load_driver(subject_driver)

    now = datetime.now()
    current_time = now.strftime("%H-%M-%S")

    output_dir = os.path.join(Path(options.output).absolute(), str(subject.subject()) + "-" + current_time)
    os.mkdir(output_dir, 0o755)

    if options.nonfunctional:
        logging.info("Non-Functional EvoGFuzz")
        evogfuzz = NonFunctionalEvoGFuzz(output_dir, subject)
    else:
        logging.info("Functional EvoGFuzz")
        evogfuzz = FunctionalEvoGFuzz(output_dir, subject)

    evogfuzz.execute()
