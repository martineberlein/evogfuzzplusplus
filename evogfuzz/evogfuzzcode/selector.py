#!/usr/bin/env python3
import logging

import pandas


class Selector:

    def __init__(self, working_dir, grammar_name, grammar_starting_rule, parameter_lambda, tournament_number):
        self.__working_dir = working_dir
        self.__grammar_name = grammar_name
        self.__grammar_starting_rule = grammar_starting_rule
        self.__lambda = parameter_lambda
        self.__tournament_number = tournament_number

    '''
    This function determines the fittest individuals by running tournaments.
    A list of the fittest individual of each tournament is returned. 
    '''

    def tournament_selection(self, fitness):
        fittest_individuals = []
        fitness.sample(frac=1)

        # Running tournaments
        for i in range(self.__tournament_number):
            current_tournament = fitness.head(10)
            fitness = fitness[10:]
            fittest = current_tournament.sort_values(by='fitness', ascending=False).head(1)
            fittest_individuals.append(fittest)

        fittest_individuals = pandas.concat(fittest_individuals)
        fittest_individuals_sorted = fittest_individuals.sort_values(by='fitness', ascending=False)

        logging.info("TOP 10 Individuals (Tournament Selection)")
        print(fittest_individuals_sorted)

        return fittest_individuals_sorted
