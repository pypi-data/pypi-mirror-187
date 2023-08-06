from os import path
from tabulate import tabulate
import pandas as pd
import sys
import math as m
import csv


def topsis(file, weight, imp, resFile):
    dtset = pd.read_csv(file)

    dtset.dropna(inplace=True)

    d = dtset.iloc[0:, 1:].values

    mat = pd.DataFrame(d)

    sumSquares = []
    for col in range(0, len(mat.columns)):
        X = mat.iloc[0:, [col]].values
        sum = 0
        for value in X:
            sum = sum + m.pow(value, 2)
        sumSquares.append(m.sqrt(sum))

    j = 0
    while (j < len(mat.columns)):
        for i in range(0, len(mat)):
            mat[j][i] = mat[j][i]/sumSquares[j]
        j = j+1

    k = 0
    while (k < len(mat.columns)):
        for i in range(0, len(mat)):
            mat[k][i] = mat[k][i]*weight[k]
        k = k+1

    bestVal = []
    worstVal = []

    for col in range(0, len(mat.columns)):
        Y = mat.iloc[0:, [col]].values

        if imp[col] == "-":
            maxValue = max(Y)
            minValue = min(Y)
            bestVal.append(minValue[0])
            worstVal.append(maxValue[0])
        if imp[col] == "+":
            maxValue = max(Y)
            minValue = min(Y)
            bestVal.append(maxValue[0])
            worstVal.append(minValue[0])

    SiPlus = []
    SiMinus = []

    for row in range(0, len(mat)):
        tmp = 0
        t2 = 0
        wrow = mat.iloc[row, 0:].values
        for value in range(0, len(wrow)):
            tmp = tmp + (m.pow(wrow[value] - bestVal[value], 2))
            t2 = t2 + (m.pow(wrow[value] - worstVal[value], 2))
        SiPlus.append(m.sqrt(tmp))
        SiMinus.append(m.sqrt(t2))

    Pi = []

    for row in range(0, len(mat)):
        Pi.append(SiMinus[row]/(SiPlus[row] + SiMinus[row]))

    Rank = []
    sortedPi = sorted(Pi, reverse=True)

    for row in range(0, len(mat)):
        for i in range(0, len(sortedPi)):
            if Pi[row] == sortedPi[i]:
                Rank.append(i+1)

    col1 = dtset.iloc[:, [0]].values
    mat.insert(0, dtset.columns[0], col1)
    mat['Topsis Score'] = Pi
    mat['Rank'] = Rank

    newColNames = []
    for name in dtset.columns:
        newColNames.append(name)
    newColNames.append('Topsis Score')
    newColNames.append('Rank')
    mat.columns = newColNames

    mat.to_csv(resFile)

    print(tabulate(mat, headers=mat.columns))


def main():
    if len(sys.argv) == 5:
        file = sys.argv[1].lower()
        weight = sys.argv[2].split(",")
        for i in range(0, len(weight)):
            weight[i] = int(weight[i])
        imp = sys.argv[3].split(",")
        for impact in imp:
            if impact != "+" and impact != "-":
                print("Impact must have only + or - values")
                return
        resFile = sys.argv[-1].lower()
        if ".csv" not in resFile:
            print("RESULT FILENAME SHOULD CONTAIN '.csv'")
            return
        if path.exists(file):
            if len(weight) != len(imp):
                print("INPUT ERROR, NUMBER OF WEIGHTS AND IMPACTS SHOULD BE EQUAL")
                return
        else:
            print("INPUT FILE DOES NOT EXISTS ! CHECK YOUR INPUT")
            return
        with open(file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            if len(header) < 3:
                print("Error: Input file must contain at least three columns.")
                return
            else:
                for row in reader:
                    numeric_columns = len(row)-1
                    for i in range(1, len(row)):
                        try:
                            float(row[i])
                        except ValueError:
                            print(
                                "Error: All columns from 2nd column onwards must be numeric in nature ")
                            return
                if (numeric_columns != len(weight) or numeric_columns != len(imp)):
                    print(
                        "The size of weight array, impact array and number of numeric coluns must all be same ")
                    return
    else:
        print("REQUIRED NUMBER OF ARGUMENTS ARE NOT PROVIDED !")
        print("SAMPLE INPUT : python <script_name> <input_data_file_name> <weight> <imp> <result_file_name>")
        return
    topsis(file, weight, imp, resFile)


if __name__ == '__main__':
    main()
