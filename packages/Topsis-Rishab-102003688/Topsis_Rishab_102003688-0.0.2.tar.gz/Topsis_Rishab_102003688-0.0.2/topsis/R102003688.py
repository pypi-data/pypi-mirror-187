
# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys


def topsis(data, weights, impacts, output):

    # df = pd.read_csv(data)
    df = data
    # %%
    # sum of squares of values in each column
    for i in df["P1"]:
        print(i)

    # %%
    # find sum of square of values in each column
    t = df.columns[1:]
    print(t)
    for i in t:
        col_sum_square = [x ** 2 for x in df[i]]
        # modifying each value in column by dividing it by square root of sum of squares of values in that column
        df[i] = df[i].apply(lambda x: x / (sum(col_sum_square) ** 0.5))
        print(df[i])

    # %%
    print(weights)
    print(impacts)
    df

    # %%
    # modifying each column by multiplying it by its weight
    for i in range(len(df.columns[1:])):
        df[df.columns[i + 1]] = df[df.columns[i + 1]
                                   ].apply(lambda x: x * weights[i])
    df

    # %%
    ideal_best_array = []
    ideal_worst_array = []

    for k in range(len(df)):
        ideal_best_array.append([])
        ideal_worst_array.append([])

    for i in range(len(df.columns[1:])):
        if impacts[i] == "-":
            ideal_best = df[df.columns[i + 1]].min()
            ideal_worst = df[df.columns[i + 1]].max()
        else:
            ideal_best = df[df.columns[i + 1]].max()
            ideal_worst = df[df.columns[i + 1]].min()

        for j in range(len(df)):
            ideal_best_array[j].append(
                (df[df.columns[i + 1]][j] - ideal_best)**2)
            ideal_worst_array[j].append(
                (df[df.columns[i + 1]][j] - ideal_worst)**2)

    print(ideal_best_array)
    print(len(ideal_best_array))

    # %%
    # making a new column in dataframe for storing distance from ideal best and ideal worst
    df["ideal_best"] = ""
    df["ideal_worst"] = ""
    for i in range(len(df)):
        df["ideal_best"][i] = sum(ideal_best_array[i]) ** 0.5
        df["ideal_worst"][i] = sum(ideal_worst_array[i]) ** 0.5

    df["performance_score"] = df["ideal_worst"] / \
        (df["ideal_best"] + df["ideal_worst"])
    df

    # %%
    # ranking the performance score
    df["rank"] = df["performance_score"].rank(ascending=False)

    # export excel file
    df.to_csv(output, index=False)


if __name__ == "__main__":
    # Arguments not equal to 5
    # print("Checking for Errors...\n")
    if len(sys.argv) != 5:
        print("ERROR : NUMBER OF PARAMETERS")
        print("USAGE : python topsis.py inputfile.csv '1,1,1,1' '+,+,-,+' result.csv ")
        exit(1)

    # File Not Found error
    elif not os.path.isfile(sys.argv[1]):
        print(f"ERROR : {sys.argv[1]} Don't exist!!")
        exit(1)

    # File extension not csv
    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print(f"ERROR : {sys.argv[1]} is not csv!!")
        exit(1)

    else:
        dataset = pd.read_csv(sys.argv[1])
        nCol = len(dataset.columns.values)

        # less then 3 columns in input dataset
        if nCol < 3:
            print("ERROR : Input file have less then 3 columns")
            exit(1)

        # Handeling non-numeric value
        for i in range(1, nCol):
            pd.to_numeric(dataset.iloc[:, i], errors='coerce')
            dataset.iloc[:, i].fillna(
                (dataset.iloc[:, i].mean()), inplace=True)

        # Handling errors of weighted and impact arrays
        try:
            weights = [float(i) for i in sys.argv[2].split(',')]
        except:
            print("ERROR : In weights array please check again")
            exit(1)
        impact = sys.argv[3].split(',')
        for i in impact:
            if not (i == '+' or i == '-'):
                print("ERROR : In impact array please check again")
                exit(1)

        # Checking number of column,weights and impacts is same or not
        if nCol != len(weights)+1 or nCol != len(impact)+1:
            print(
                "ERROR : Number of weights, number of impacts and number of columns not same")
            exit(1)

        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("ERROR : Output file extension is wrong")
            exit(1)
        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])
        # print(" No error found\n\n Applying Topsis Algorithm...\n")

    topsis(dataset, weights, impact, sys.argv[4])
