import sys
import os
import pandas as pd
import numpy as np


def main():
    # Number of arguments
    n = len(sys.argv)
    # If number of arguments is not equal to 5
    if n != 5:
        print("ERROR: Invalid number of arguments")
        exit()

    # If file does not exist
    if not os.path.exists(sys.argv[1]):
        print("ERROR: {} does not exist".format(sys.argv[1]))
        exit()

    # Error if file is not csv
    if not sys.argv[1].endswith(".csv"):
        print("ERROR: {} is not a csv file".format(sys.argv[1]))
        exit()

    # Error if file has no data
    if pd.read_csv(sys.argv[1]).empty:
        print("ERROR: File has no data")
        exit()

    # Error if weights are not given
    if sys.argv[2] == "":
        print("ERROR: Weights not given")
        exit()

    # Error if weights are not equal to number of columns
    if len(sys.argv[2].split(",")) != len(pd.read_csv(sys.argv[1]).columns) - 1:
        print("ERROR: Number of weights not equal to number of columns")
        exit()

    # Error if weights are not separated by comma
    try:
        weights = [int(i) for i in sys.argv[2].split(",")]
    except ValueError:
        print("ERROR: Weights are not provided in the correct format")
        exit()

    # Error if impacts are not given
    if sys.argv[3] == "":
        print("ERROR: Impacts not given")
        exit()

    # Error if impacts are not separated by comma
    try:
        impact = [i for i in sys.argv[3].split(",")]
    except ValueError:
        print("ERROR: Impacts are not provided in the correct format")
        exit()

    # Error if impacts are not equal to number of columns
    if len(sys.argv[3].split(",")) != len(pd.read_csv(sys.argv[1]).columns) - 1:
        print("ERROR: Number of impacts not equal to number of columns")
        exit()

    # Error if impacts are not + or -
    if not all(i in ["+", "-"] for i in sys.argv[3].split(",")):
        print("ERROR: Impacts are not + or -")
        exit()

    # Error if Result file is not given
    if sys.argv[4] == "":
        print("ERROR: Result file not given")
        exit()

    # Error if result file is not csv
    if not sys.argv[4].endswith(".csv"):
        print("ERROR: {} is not a csv file".format(sys.argv[4]))
        exit()

    data = pd.read_csv(sys.argv[1])

    # Error If number of columns is less than 3
    if len(data.columns)-1 <= 3:
        print("ERROR: Number of columns is less than 3")
        exit()

    # 2nd column of input file has non numeric values then encode it
    for i in range(1, len(data.columns)-1):
        pd.to_numeric(data.iloc[:, i], errors="coerce")
        data.iloc[:, i].fillna((data.iloc[:, i].mode()), inplace=True)

    # Read data from csv file
    topsis(data, sys.argv[4], weights, sys.argv[3].split(","))


def topsis(data, result_file, weights, impact):
    new_data = normalisation(data, weights)
    best_solution = ideal_best_solution(new_data, impact)
    worst_solution = ideal_worst_solution(new_data, impact)
    scores = calc_score(
        new_data, best_solution, worst_solution)
    new_data["Topsis Score"] = scores
    new_data["Rank"] = new_data["Topsis Score"].rank(
        method="max", ascending=False)
    new_data = new_data.astype({"Rank": int})
    new_data.to_csv(result_file, index=False)


def calc_score(data, best_solution, worst_solution):
    # Euclidean distance
    scores = []
    for i in range(len(data)):
        pos_euclidean_distance = 0
        neg_euclidean_distance = 0
        for j in range(1, data.columns.values.size):
            pos_euclidean_distance += (best_solution[j-1] - data.iloc[i, j])**2
            neg_euclidean_distance += (
                worst_solution[j-1] - data.iloc[i, j])**2
        pos_euclidean_distance, neg_euclidean_distance = pos_euclidean_distance**0.5, neg_euclidean_distance**0.5
        score = (neg_euclidean_distance /
                 (pos_euclidean_distance + neg_euclidean_distance))
        scores.append(score)

    return scores


def ideal_best_solution(data, impact):
    # Ideal best solution
    ideal_solution_data = []
    for i in range(1, len(data.columns.values)):
        if impact[i-1] == "+":
            ideal_solution_data.append(max(data.iloc[:, i]))
        else:
            ideal_solution_data.append(min(data.iloc[:, i]))
    ideal_solution_data = np.array(ideal_solution_data)
    return ideal_solution_data


def ideal_worst_solution(data, impact):
    # Ideal worst solution
    ideal_solution_data = []
    for i in range(1, len(data.columns.values)):
        if impact[i-1] == "+":
            ideal_solution_data.append(min(data.iloc[:, i]))
        else:
            ideal_solution_data.append(max(data.iloc[:, i]))
    ideal_solution_data = np.array(ideal_solution_data)
    return ideal_solution_data


def normalisation(data, weights):
    # Normalisation
    normalised_data = data.copy()
    for i in range(1, len(data.columns.values)):
        column_sum_of_squares = 0

        for j in range(0, len(data)):
            column_sum_of_squares += data.iloc[j, i]*data.iloc[j, i]

        column_sum_of_squares = column_sum_of_squares**0.5

        for k in range(0, len(data)):
            normalised_data.iat[k, i] = (
                data.iloc[k, i]/column_sum_of_squares)*weights[i-1]

    return normalised_data


if __name__ == "__main__":
    main()
