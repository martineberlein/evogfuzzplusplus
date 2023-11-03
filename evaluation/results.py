from typing import List, Tuple
import pandas as pd
from itertools import product


def initialize_dataframe(
    subject_names: List[Tuple[str, int]], tool_names: List[str], number_of_runs
):
    # Initialize the DataFrame
    columns = pd.MultiIndex.from_tuples(subject_names, names=["Subject", "ID"])
    index = pd.MultiIndex.from_product(
        [range(1, number_of_runs + 1), tool_names], names=["Run", "Approach"]
    )
    results_df = pd.DataFrame(index=index, columns=columns).fillna({})
    return results_df


def main():
    r = initialize_dataframe(
        [("GCD", 1), ("GCD", 2), ("Middle", 1)], ["EvoGFuzz", "InputsFromHell"], 15
    )
    r.at[(1, "EvoGFuzz"), ("GCD", 1)] = {"Error": 1, "Error_2": 3}
    r.at[(1, "InputsFromHell"), ("GCD", 1)] = {"Error": 2}
    print(r)


if __name__ == "__main__":
    # from itertools import product
    # subject_names = ["GCD", "Middle"]
    # implementations = [i for i in range(1, 11)]
    # subject_index =  list(product(subject_names, implementations))
    # print(subject_index)
    main()
