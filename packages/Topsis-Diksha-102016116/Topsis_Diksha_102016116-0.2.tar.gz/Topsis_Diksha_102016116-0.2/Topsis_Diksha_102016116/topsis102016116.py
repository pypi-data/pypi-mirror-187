import os
import sys
import numpy as np
import pandas as pd

def validate_data(file, weights, impacts):


    ans = pd.read_csv(file)
    # Input file must have at least 3 columns
    if ans.shape[1] < 3:
        print("Invalid input file, must have at least 3 columns")
        sys.exit(1)

    # Check if weights and impacts are valid
    try:
        weights = np.array(weights, dtype=float)
        impacts = np.array(impacts)
    except Exception as e:
        print(e)
        print("Invalid weights or impacts")
        sys.exit(1)

    # Check for correct number of weights and impacts and if they're separated by commas
    try:
        if len(weights) != ans.shape[1] - 1 or len(impacts) != ans.shape[1] - 1:
            print("Invalid number of weights or impacts")
            sys.exit(1)
    except:
        print("weights or impacts, must be separated by commas")
        sys.exit(1)

    for col in ans.columns[1:]:
        if not pd.api.types.is_numeric_dtype(ans[col]):
            print(" all columns must be numeric")
            sys.exit(1)

    # Impacts must be either + or -
    if not all([impact in ["+", "-"] for impact in impacts]):
        print(" impacts must be either + or -")
        sys.exit(1)

    # Weights must be positive
    if not all([weight > 0 for weight in weights]):
        print(" weights must be positive")
        sys.exit(1)

    return ans, weights, impacts





def topsis(matrix, weights, impact):
    

    norm_matrix = matrix.drop(matrix.columns[0], axis=1)

    # Convert impact to 1 or -1
    impact = np.where(impact == "+", 1, -1)

    
    norm_matrix = norm_matrix / np.sqrt(np.sum(norm_matrix**2, axis=0))

    # Calculate the weighted decision matrix
    weighted_matrix = norm_matrix * weights

    # Calculate the ideal and negative-ideal solutions after multiplying with the impact vector
    f_best = np.amax(weighted_matrix * impact, axis=0).abs()
    f_worst = np.amin(weighted_matrix * impact, axis=0).abs()

    best = np.sqrt(np.sum((weighted_matrix -f_best) ** 2, axis=1))
    worst = np.sqrt(np.sum((weighted_matrix -f_worst) ** 2, axis=1))

    # Calculate performance score
    performance = worst / (best + worst)

    # Calculate rank in descending order
    rank = performance.rank(ascending=False).astype(int)

    # Add performance score and rank to the decision matrix
    matrix["Performance"] = performance
    matrix["Rank"] = rank

    return matrix



def cli_output():
    if len(sys.argv) != 5:
        print('Wrong Number of args')
        print('Input should be like - \n '
              'python [package name] [path of csv as string] [list of weights as string] [list of sign as string][output file path]')
    else:
        file_path = sys.argv[1]
        try:
            if os.path.exists(file_path):
                print('Path exist')
        except OSError as err:
            print(err.reason)
            exit(1)

        df = pd.read_csv(file_path, header=None)
        df = df.iloc[1:, :]
        df = df.iloc[:, 1:]
       
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]
        output_file = sys.argv[4]
        w = arg2.split(",")
        # w = list(map(float, w))
        s = arg3.split(",")
        #s = list(map(int, s))
        df, w, s = validate_data(file_path, w, s)
        res = topsis(df, w, s)
        res.to_csv(output_file, index=False)
        print()
        print(res)
        print()
        print("Output saved to",output_file)
        print()


if __name__ == "__main__":
    cli_output()