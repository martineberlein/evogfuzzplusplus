from typing import Dict, List, Tuple, Union
import matplotlib.pyplot as plt

from evogfuzz.types import GrammarType
from evogfuzz.type_defs import Grammar


def _initialize(grammar: Grammar) -> Dict[str, list]:
    """
    Creates a dictionary of grammar features.
    :param grammar: The input grammar
    :return: Dict
    """
    probabilities = dict()
    for rule in grammar:
        for child in grammar[rule]:
            feature = f"{rule}->{child[0]}"
            probabilities[feature] = []
    return probabilities


def parse_prob_grammars(grammar_list: List[Grammar]) -> Dict[str, List[float]]:
    """
    Takes a list of prob. grammars and returns a dictionary with the individuals grammar derivations (e.g.,
    <start>->"a") and the corresponding probabilities, comprised in a list.
    :param grammar_list: A list of probabilistic grammars.
    :return:
    """
    probabilities = _initialize(grammar_list[0])

    for grammar in grammar_list:
        for rule in grammar:
            for child in grammar[rule]:
                feature = f"{rule}->{child[0]}"
                prob_list = probabilities[feature]

                # Check for opts(prob="...") grammar extension
                assert isinstance(child, tuple), "Expected a probabilistic grammar"

                if child[1]["prob"] is None:
                    prob_list.append(1.0)
                else:
                    prob_list.append(child[1]["prob"])
                probabilities[feature] = prob_list

    return probabilities


def _mathlib_plot(x_values, grammar_list):
    f, ax = plt.subplots(1)

    feature_disp = ["<function>->cos", "<function>->sqrt", "<maybe_minus>->-"]

    for feature in feature_disp:
        ax.plot(x_values, grammar_list[feature])


def plot(grammar_list: Union[List[Tuple[Grammar, GrammarType, float]], List[Grammar]]):
    if isinstance(grammar_list[0], tuple):
        grammar_list = [grammar_tuple[0] for grammar_tuple in grammar_list]

    x_values = [i for i in range(len(grammar_list))]
    prob_dict = parse_prob_grammars(grammar_list)
    _mathlib_plot(x_values, prob_dict)


if __name__ == "__main__":
    g = {"<start>": [("a", {"prob": 1})]}
    x = [(g, GrammarType.LEARNED, 10.0)]

    plot(x)
