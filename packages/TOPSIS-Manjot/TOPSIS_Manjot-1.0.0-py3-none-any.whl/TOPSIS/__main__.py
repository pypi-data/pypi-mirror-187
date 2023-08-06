import pandas as pd
import os
import sys
def main():
    if len(sys.argv) != 5:
        print("Not enough arguments")
        exit(1)
    else:
        dataset, temp_dataset = pd.read_csv(sys.argv[1]), pd.read_csv(sys.argv[1])
        nCol = len(temp_dataset.columns.values)
        for i in range(1, nCol):
            pd.to_numeric(dataset.iloc[:, i], errors='coerce')
            dataset.iloc[:, i].fillna(
                (dataset.iloc[:, i].mean()), inplace=True)
        try:
            weights = [int(i) for i in sys.argv[2].split(',')]
        except:
            exit(1)
        impact = sys.argv[3].split(',')
        for i in impact:
            if not (i == '+' or i == '-'):
                exit(1)
        temp_dataset = normal(temp_dataset, nCol, weights)
        p_sln, n_sln = vals_c(temp_dataset, nCol, impact)
        score = []
        for i in range(len(temp_dataset)):
            temp_p, temp_n = 0, 0
            for j in range(1, nCol):
                temp_p = temp_p + (p_sln[j-1] - temp_dataset.iloc[i, j])**2
                temp_n = temp_n + (n_sln[j-1] - temp_dataset.iloc[i, j])**2
            temp_p, temp_n = temp_p**0.5, temp_n**0.5
            score.append(temp_n/(temp_p + temp_n))
        dataset['Topsis Score'] = score
        dataset['Rank'] = (dataset['Topsis Score'].rank(
            method='max', ascending=False))
        dataset = dataset.astype({"Rank": int})
        dataset.to_csv(sys.argv[4], index=False)

def vals_c(df, nCol, impact):
    p_sln = (df.max().values)[1:]
    n_sln = (df.min().values)[1:]
    for i in range(1, nCol):
        if impact[i-1] == '-':
            p_sln[i-1], n_sln[i-1] = n_sln[i-1], p_sln[i-1]
    return p_sln, n_sln

def normal(df, nCol, weights):
    for i in range(1, nCol):
        temp = 0
        for j in range(len(df)):
            temp = temp + df.iloc[j, i]**2
        temp = temp**0.5
        for j in range(len(df)):
            df.iat[j, i] = (
                df.iloc[j, i] / temp)*weights[i-1]
    return df
