import sys
import pandas as pd

def normalize(data):
    #"""Function to normalize the data by column"""
    min_values = data.min(axis=0)
    max_values = data.max(axis=0)
    normalized_data = (data - min_values) / (max_values - min_values)
    return normalized_data

def calculate_topsis(data, weights, impacts):
    #"""Function to calculate the Topsis score and rank"""
    # Normalize the data
    normalized_data = normalize(data)
    # Multiply the normalized data with the weights
    weighted_data = normalized_data * weights
    # Apply the impacts
    for i in range(weighted_data.shape[1]):
        if impacts[i] == '-':
            weighted_data.iloc[:, i] = weighted_data.iloc[:, i] * -1
    # Calculate the positive and negative ideal solutions
    positive_ideal = weighted_data.max(axis=0)
    negative_ideal = weighted_data.min(axis=0)
    # Calculate the Topsis score
    topsis_score = (weighted_data - positive_ideal).pow(2).sum(axis=1) + (weighted_data - negative_ideal).pow(2).sum(axis=1)
    topsis_score = topsis_score.pow(0.5)
    # Calculate the Topsis rank
    topsis_rank = topsis_score.rank(method='min', ascending=False)
    # Add the Topsis score and rank columns to the data
    data['Topsis Score'] = topsis_score
    data['Rank'] = topsis_rank
    return data

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Error: Incorrect number of parameters. Usage:python program.py InputDataFile Weights Impacts ResultFileName")
        sys.exit()
    input_file = sys.argv[1]
    weights = [float(i) for i in sys.argv[2].split(',')]
    impacts = sys.argv[3].split(',')
    result_file = sys.argv[4]
    try:
        data = pd.read_csv(input_file)
        data = data.apply(pd.to_numeric, errors='coerce')
        data = data.drop(columns=["Fund Name"])
        data = (data - data.min()) / (data.max() - data.min())
    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found")
        sys.exit()
    if len(weights) != data.shape[1]:
        print("Error: Number of weights must be same as number of columns in the input file")
        sys.exit()
    if len(impacts) != data.shape[1]:
        print("Error: Number of impacts must be same as number of columns in the input file")
        sys.exit()
    for impact in impacts:
        if impact != '+' and impact != '-':
            print("Error: Impacts must be either + or -")
            sys.exit()
    result = calculate_topsis(data, weights, impacts)
    result.to_csv(result_file, index=False)
    print(f"Result has been written to {result_file}")

