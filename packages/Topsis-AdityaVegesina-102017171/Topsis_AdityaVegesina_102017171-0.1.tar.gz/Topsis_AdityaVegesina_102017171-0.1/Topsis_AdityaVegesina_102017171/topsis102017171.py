import os
import sys
import numpy as np
import pandas as pd

def validateData(file, weights, impacts):
    ip = pd.read_csv(file)
    if ip.shape[1] < 3:
        print("Input file must contain at least 3 columns")
        sys.exit(1)

    try:
        weights = np.array(weights, dtype=float)
        impacts = np.array(impacts)
    except Exception as e:
        print(e)
        print("Invalid weights/impacts")
        sys.exit(1)

    try:
        if len(weights) != ip.shape[1] - 1 or len(impacts) != ip.shape[1] - 1:
            print("Invalid no. of weights/impacts")
            sys.exit(1)
    except:
        print("weights/impacts, should be separated by commas")
        sys.exit(1)

    for col in ip.columns[1:]:
        if not pd.api.types.is_numeric_dtype(ip[col]):
            print("non-numeric value shouldnt be present in the column")
            sys.exit(1)

#Checking the impacts
    if not all([impact in ["+", "-"] for impact in impacts]):
        print(" impacts must be either +/-")
        sys.exit(1)

#Checking the weights
    if not all([weight > 0 for weight in weights]):
        print(" weights must be positive integers")
        sys.exit(1)

    return ip, weights, impacts





def topsis(matrix, weights, impact):
    

    nmatrix = matrix.drop(matrix.columns[0], axis=1)

    #Change the impacts to numerical values
    impact = np.where(impact == "+", 1, -1)

    
    nmatrix = nmatrix / np.sqrt(np.sum(nmatrix**2, axis=0))

    weighted_matrix = nmatrix * weights

    f_best = np.amax(weighted_matrix * impact, axis=0).abs()

    f_worst = np.amin(weighted_matrix * impact, axis=0).abs()

    best = np.sqrt(np.sum((weighted_matrix -f_best) ** 2, axis=1))

    worst = np.sqrt(np.sum((weighted_matrix -f_worst) ** 2, axis=1))
    
    performance = worst / (best + worst)
    rank = performance.rank(ascending=False).astype(int)

    matrix["Performance"] = performance

    matrix["Rank"] = rank

    return matrix



def commandLineInput():
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
        df, w, s = validateData(file_path, w, s)
        res = topsis(df, w, s)
        res.to_csv(output_file, index=False)
        print()
        print(res)
        print()
        print("Output saved to",output_file)
        print()


if __name__ == "__main__":
    commandLineInput()