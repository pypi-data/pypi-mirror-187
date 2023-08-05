# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 18:42:56 2023

@author: Brahmjot Kaur
"""

import pandas as pd
import sys
import os


def main():
    # Correct number of parameters (inputFileName, Weights, Impacts, resultFileName).
    if len(sys.argv) != 5:
        print("Error in number of parameters")
        print("Correct Usage is: python 101556.py 101556-data.csv “1,1,1,2” “+,+,-,+” 101556-result.csv")
        exit(1)

    # File Not Found 
    elif not os.path.isfile(sys.argv[1]):
        print(f"ERROR : {sys.argv[1]} File Not Found")
        exit(1)

    # File extension not csv
    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print(f" {sys.argv[1]} is not a csv file")
        exit(1)

    else:
        dataset, temp_dataset = pd.read_csv(
            sys.argv[1]), pd.read_csv(sys.argv[1])
        noCol = len(temp_dataset.columns.values)

        # Input file must contain three or more columns
        if noCol < 3:
            print("Input file must contain three or more columns")
            exit(1)

        # Handeling non-numeric value
        for i in range(1, noCol):
            pd.to_numeric(dataset.iloc[:, i], errors='coerce')
            dataset.iloc[:, i].fillna(
                (dataset.iloc[:, i].mean()), inplace=True)

        # Impacts must be either +ve or -ve.
        # Impacts and weights must be separated by ‘,’ (comma).
        try:
            weights = [int(i) for i in sys.argv[2].split(',')]
        except:
            print("Impacts and weights must be separated by ‘,’ (comma).")
            exit(1)
        impact = sys.argv[3].split(',')
        for i in impact:
            if not (i == '+' or i == '-'):
                print("Impacts must be either +ve or -ve.")
                exit(1)

        # Checking number of column,weights and impacts is same or not
        if noCol != len(weights)+1 or noCol != len(impact)+1:
            print(
                "Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same.")
            exit(1)

        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("ERROR : Output file extension is wrong")
            exit(1)
        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])
        
        topsis_packet(temp_dataset, dataset, noCol, weights, impact)


def Normalization(temp_dataset, noCol, weights):
    for i in range(1, noCol):
        temp = 0
        for j in range(len(temp_dataset)):
            temp = temp + temp_dataset.iloc[j, i]**2
        temp = temp**0.5
        for j in range(len(temp_dataset)):
            temp_dataset.iat[j, i] = (
                temp_dataset.iloc[j, i] / temp)*weights[i-1]
    return temp_dataset


def Calculate_Values(temp_dataset, noCol, impact):
    pos_sol = (temp_dataset.max().values)[1:]
    neg_sol = (temp_dataset.min().values)[1:]
    for i in range(1, noCol):
        if impact[i-1] == '-':
            pos_sol[i-1], neg_sol[i-1] = neg_sol[i-1], pos_sol[i-1]
    return pos_sol, neg_sol


def topsis_packet(temp_dataset, dataset, noCol, weights, impact):
    temp_dataset = Normalization(temp_dataset, noCol, weights)
    pos_sol, neg_sol = Calculate_Values(temp_dataset, noCol, impact)

    score = []
    for i in range(len(temp_dataset)):
        temp_p, temp_n = 0, 0
        for j in range(1, noCol):
            temp_p = temp_p + (pos_sol[j-1] - temp_dataset.iloc[i, j])**2
            temp_n = temp_n + (neg_sol[j-1] - temp_dataset.iloc[i, j])**2
        temp_p, temp_n = temp_p**0.5, temp_n**0.5
        score.append(temp_n/(temp_p + temp_n))
    dataset['Topsis Score'] = score

    # calculating the rank according to topsis score
    dataset['Rank'] = (dataset['Topsis Score'].rank(
        method='max', ascending=False))
    dataset = dataset.astype({"Rank": int})

    # Writing in the result csv
    dataset.to_csv(sys.argv[4], index=False)

if __name__ == "__main__":
    main()