#!/usr/bin/env python3

import os
from pathlib import Path
import re
import pandas
import subprocess

'''
This function is used to determine the fittest individuals by ranking all input files according to a 
fitness function.
Tournaments are held to select the fittest individuals from each tournament. 
These input files are then used to learn the new probabilistic grammar.
'''


def determine_fittest_individuals(working_dir, input_files, exec_data, grammar_name, start_rule, lambda_value):
    main_directory = os.getcwd()
    os.chdir(os.path.join(working_dir, "grammar", "antlrParser"))

    FNULL = open(os.devnull, 'w')
    # Using ANTLR to determine the derivation tree of an input file
    process = subprocess.Popen(["java", "org.antlr.v4.gui.TestRig", grammar_name,
                                "main_dummy_rule_hope_for_no_collisions", "-tree"] + input_files,
                               stdout=subprocess.PIPE, stderr=FNULL)

    os.chdir(main_directory)
    antlr_output = process.communicate()[0]
    # print(antlr_output)
    individual_derivation_trees = re.findall(r'main_dummy_rule_hope_for_no_collisions.+?' +
                                             str("n" + start_rule), str(antlr_output))

    # Adding last derivation tree manually
    last_tree = str(antlr_output).split('(main_dummy_rule_hope_for_no_collisions')[100]
    individual_derivation_trees.append(last_tree)
    return calculate_fitness(individual_derivation_trees, input_files, lambda_value, exec_data)


'''def determine_fittest_individuals_old(working_dir, current_iteration, exec_data, file_extension, grammar_name,
                                  start_rule, lambda_value):
    main_directory = os.getcwd()
    os.chdir(os.path.join(working_dir, "grammar", "antlrParser"))

    input_files.sort()

    # Using ANTLR to determine the derivation tree of an input file
    process = subprocess.Popen(["java", "org.antlr.v4.gui.TestRig", grammar_name,
                                "main_dummy_rule_hope_for_no_collisions", "-tree"] + input_files,
                               stdout=subprocess.PIPE)

    os.chdir(main_directory)
    antlr_output = process.communicate()[0]
    # print(antlr_output)
    individual_derivation_trees = re.findall(r'main_dummy_rule_hope_for_no_collisions.+?' +
                                             str(start_rule), str(antlr_output))

    # Adding last derivation tree manually
    last_tree = str(antlr_output).split('(main_dummy_rule_hope_for_no_collisions')[100]
    individual_derivation_trees.append(last_tree)

    return calculate_fitness(individual_derivation_trees, input_files, lambda_value, exec_data)
    '''


'''
This function calculates the fitness of all individuals. 
A detailed description of the fitness function can be found in our paper.
This process is designed so the fitness function can be replaced easily.
The fitness function returns the input files as well as their fitness. 
'''


def calculate_fitness(individual_derivation_trees, input_files, lambda_value, exec_data):

    fitness_data = []
    i = 0
    for tree in individual_derivation_trees:
        size = os.stat(input_files[i]).st_size
        # Check for empty files
        if size != 0:
            expansions = tree.count(' (')
            ratio = (lambda_value * expansions) / size

            fitness = ratio * expansions
        else:
            fitness = 0

        fitness_data.append({
            "file": Path(input_files[i]).name,
            "fitness": fitness
        })
        i += 1
    df = pandas.DataFrame.from_records(fitness_data)
    # df.sort_values(by='fitness', ascending=False)
    # print(df.sort_values(by='fitness', ascending=False))
    return df


def calculate_fitness_executionTime(input_files, exec_data):
    fitness_data = []

    for file in input_files:
        size = os.stat(file).st_size
        exec_time = exec_data.loc[exec_data['file'] == Path(file).name]
        # Check for empty files
        if size != 0:
            # fitness = float(exec_time['exec_time'].values[0]) / size
            fitness = float(exec_time['exec_time'].values[0])
        else:
            fitness = 0

        fitness_data.append({
            "file": Path(file).name,
            "size": size,
            # "exec_time": exec_time['exec_time'].values[0],
            "fitness": fitness
        })

    df = pandas.DataFrame.from_records(fitness_data)
    # df.sort_values(by='fitness', ascending=False)
    # print(df.sort_values(by='fitness', ascending=False))
    return df


if __name__ == "__main__":
    exec_data_test = []
    input_file = list()
    input_file.append(
        "/Users/martineberlein/Documents/01_Uni/06_paperEMSE/git/evogfuzz-extension/grammars/js/seeds/closure.2808.js")
    input_file.append(
        "/Users/martineberlein/Documents/01_Uni/06_paperEMSE/git/evogfuzz-extension/grammars/js/seeds/ArrowFunctions.js")
    exec_data_test.append({
            "file": "closure.2808.js",
            "exec_time": 0.00012
        })
    exec_data_test.append({
        "file": "ArrowFunctions.js",
        "exec_time": 0.10
    })
    df_test = pandas.DataFrame.from_records(exec_data_test)

    fitness_test = calculate_fitness_executionTime(input_file, df_test)
    print(fitness_test)
