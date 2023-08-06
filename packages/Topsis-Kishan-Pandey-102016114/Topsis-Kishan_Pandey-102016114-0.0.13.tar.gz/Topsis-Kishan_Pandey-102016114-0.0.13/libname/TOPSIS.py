import pandas as pd
import numpy as np
import sys

def topsis(data, weights, impact):
    impact = np.array([1 if i=='+' else -1 for i in impact])
    # Normalize the data
    data = data / data.abs().sum()
    # Get the weighted data
    data = data * weights
    # Get the ideal and negative ideal solutions
    ideal = data.max()
    negative_ideal = data.min()
    # Get the relative closeness to the ideal solution
    relative_closeness = (impact*(data - negative_ideal) / (ideal - negative_ideal)).sum(axis=1)
    return relative_closeness

if __name__ == '__main__':
    # Read the dataset from a CSV file
    data1 = pd.read_excel(sys.argv[1])
    data1.to_csv("102016114-data.csv",index=False,header=True)
    data=pd.read_csv("102016114-data.csv")

    # Get the weights from the command line arguments
    weights = list(map(float, sys.argv[2].split(',')))
    # Get the impact from the command line arguments
    impact = sys.argv[3].split(',')
    # Find the relative closeness using TOPSIS
    d = pd.DataFrame(data.to_numpy())
    # Identify categorical columns
    cat_cols = d.select_dtypes(include=['object']).columns

    # Convert categorical columns to ordinal
    for col in cat_cols:
        d[col] = d[col].astype('category')
        d[col] = d[col].cat.codes

    if len(d.columns) < 3:
        print("Error: Number of columns must be greater than 2")
        sys.exit()
    if len(weights) != len(impact):
        print("Error: Number of weights and impacts should be equal")
        exit()
    if len(weights) != len(d.columns)-1:
        print("Error: Number of weights and columns should be equal")
        exit()
    if len(impact) != len(d.columns)-1:
        print("Error: Number of impacts and columns should be equal")
        exit()

    relative_closeness = topsis(d.iloc[:,1:], weights, impact)
    # Adding the relative closeness to the dataset
    data['TOPSIS_SCORE'] = relative_closeness
    # Get the rankings
    data['RANK'] = data['TOPSIS_SCORE'].rank(ascending=False)
    # write the data to the CSV file
    data.to_csv(sys.argv[4],index=False)
    print("TOPSIS scores and rankings have been added to the CSV file.")





