from tabulate import tabulate
from os import path
import pandas as pd
import math as m
import sys

def topsis(filename, weights, impacts, resultFileName):
    dataset = pd.read_csv(filename)

    dataset.dropna(inplace = True)

    d = dataset.iloc[0:,1:].values

    matrix = pd.DataFrame(d)

    sumOfSquares = []
    for col in range(0, len(matrix.columns)):
        X = matrix.iloc[0:,[col]].values
        sum = 0
        for value in X:
            sum = sum + m.pow(value, 2)
        sumOfSquares.append(m.sqrt(sum))

    j = 0
    while(j < len(matrix.columns)):
        for i in range(0, len(matrix)):
            matrix[j][i] = matrix[j][i]/sumOfSquares[j] 
        j = j+1

    k = 0
    while(k < len(matrix.columns)):
        for i in range(0, len(matrix)):
            matrix[k][i] = matrix[k][i]*weights[k] 
        k = k+1

    bestValue = []
    worstValue = []

    for col in range(0, len(matrix.columns)):
        Y = matrix.iloc[0:,[col]].values
        
        if impacts[col] == "+" :
            # print("+")
            maxValue = max(Y)
            minValue = min(Y)
            bestValue.append(maxValue[0])
            worstValue.append(minValue[0])

        if impacts[col] == "-" :
            # print("-")
            maxValue = max(Y)
            minValue = min(Y)
            bestValue.append(minValue[0])
            worstValue.append(maxValue[0])

    SiPlus = []
    SiMinus = []

    for row in range(0, len(matrix)):
        temp = 0
        temp2 = 0
        wholeRow = matrix.iloc[row, 0:].values
        for value in range(0, len(wholeRow)):
            temp = temp + (m.pow(wholeRow[value] - bestValue[value], 2))
            temp2 = temp2 + (m.pow(wholeRow[value] - worstValue[value], 2))
        SiPlus.append(m.sqrt(temp))
        SiMinus.append(m.sqrt(temp2))

    Pi = []

    for row in range(0, len(matrix)):
        Pi.append(SiMinus[row]/(SiPlus[row] + SiMinus[row]))

    Rank = []
    sortedPi = sorted(Pi, reverse = True)

    for row in range(0, len(matrix)):
        for i in range(0, len(sortedPi)):
            if Pi[row] == sortedPi[i]:
                Rank.append(i+1)

    col1 = dataset.iloc[:,[0]].values
    matrix.insert(0, dataset.columns[0], col1)
    matrix['Topsis Score'] = Pi
    matrix['Rank'] = Rank

    newColNames = []
    for name in dataset.columns:
        newColNames.append(name)
    newColNames.append('Topsis Score')
    newColNames.append('Rank')
    matrix.columns = newColNames

    matrix.to_csv(resultFileName)

    print(tabulate(matrix, headers = matrix.columns))

def checkRequirements() :
    if len(sys.argv) == 5 :
        # filename
        filename = sys.argv[1].lower()
        print(filename)
        # weights
        weights = sys.argv[2].split(",")
        for i in range(0, len(weights)):
            weights[i] = int(weights[i])
        # impacts
        impacts = sys.argv[3].split(",")
        # resultFileName
        resultFileName = sys.argv[-1].lower()
        print (resultFileName)
        if ".csv" not in resultFileName:
            print("Result filename should contain '.csv'")
            return
        if path.exists(filename) :
            if len(weights) == len(impacts) :
                topsis(filename, weights, impacts, resultFileName)
            else :
                print("Input error, number of weights and impacts should be equal!")
                return
        else :
            print("Input file deosn't ecist! Check your input")
            return
    else :
        print("Required number of arguements aren't provided !")
        print("Sample input : python <script_name> <input_data_file_name> <weights> <impacts> <result_file_name>")
        return

checkRequirements()