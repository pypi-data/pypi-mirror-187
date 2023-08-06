import pandas as pd  # Library; helps in faster data analysis, data cleaning, and data pre-processing.
from os import path # This module is used for merging, normalizing and retrieving path names
import sys # This module is used to obtain the list of arguments
import math # This module provides us different mathematical functions

######### VALIDATION : Function (1) #########
def checkInputFile(file):
    # Check if the file exists
    if not (path.exists(file)):  
        print("Error: Input file doesn't exist")
        exit(0)

    # Check if file is in csv format
    if not file.endswith('.csv'): 
        print("Error: Format of input file should be csv")
        exit(0)

    # Check if inputFile is opening
    try:
        inputFile = pd.read_csv(file)
    except Exception:
        print("Error: Can't open input file" )
        exit(0)

    # Check tha file has >= 3 columns
    dim = inputFile.shape # gives dimensions
    if not dim[1] >= 3:  
        print(f"Error: Input file should have at least 3 columns")
        exit(0)

    # Check that values in rows of all columns except first column 
    # are either int or float 
    # So, loop through column and then rows
    k = 0
    for i in inputFile.columns: # .columns gives list of columns (names)
        k = k + 1
        for j in inputFile.index: # .index provides row labels
            if k != 1:
                val = isinstance(inputFile[i][j], int)
                val1 = isinstance(inputFile[i][j], float)
                if not val and not val1: 
                    print(f'Value is not numeric in {k} column')
                    exit(0)
    return 1 # Means file is in correct format 

######### VALIDATION : Function (2) #########
def check_result_file(resultFile):
    # Check that file is of csv format
    if not resultFile.endswith('.csv'): 
        print("Error: Format of result file should be csv")
        exit(0)
    return 1

######### VALIDATION : Function (3) #########
def check_weights(file, str_weight):
    inputFile = pd.read_csv(file) # Read csv file
    dim = inputFile.shape # gives dimensions
    weights = []
    split_weights_str = str_weight.split(',')
    # Check format of weights
    for split_weights_str_obj in split_weights_str :
        split_weights_str_obj_ = 0
        for split_weights_str_obj_char in split_weights_str_obj:
            if not split_weights_str_obj_char.isnumeric():
                if split_weights_str_obj_ >= 1 or  split_weights_str_obj_char != '.':
                    print("Weights are not provided in correct format")
                    exit(0)
                else:
                    split_weights_str_obj_ = split_weights_str_obj_ + 1
        weights.append(float(split_weights_str_obj))
    
    # Check that no. of weights == no. of columns - 1 of Input File 
    if len(weights) != (dim[1] - 1):
        print(f"Error: No. of weights should be same as no. of columns-1 in {file}")
        exit(0)
    return weights

######### VALIDATION : Function (4) #########
def check_impacts(file, str_impact):
    input_file = pd.read_csv(file) # Read csv file
    dim = input_file.shape # Gives dimensions
    impacts = str_impact.split(',')
    # Check that characters in impact are '+' or '-'
    for i in impacts:
        if i not in {'+', '-'}:
            print(f"Only + or - are allowed not {i}")
            exit(0)

    # Check that no. of impacts == no. of columns - 1 of Input File 
    if len(impacts) != (dim[1] - 1):
        print(f"Columns in {file} and Impacts shouls be Equal in No.")
        exit(0)
    return impacts

######### TOPSIS Algorithm : Function (1) #########
def matrixInputAndNormalise(data_file):
    df = pd.read_csv(data_file) # Read data from csv file to data frame
    columns = list(df.columns) # Gives list of column names
    columns.remove(columns[0])  # We need to normalise all columns except 1st so, remove it from list
    # Loop through columns and then rows
    for col in columns:
        root_sum_square = 0

        for row in df.index: # Gives row labels
            root_sum_square = root_sum_square + (df[col][row]) * (df[col][row])
        root_sum_square = math.sqrt(root_sum_square) # Find root sum square

        for row in df.index:
            df.at[row, col] = (df[col][row]) / root_sum_square # Division

    return df 

######### TOPSIS Algorithm : Function (2) #########
def matrixNormalizedAndWeighted(matrix, weights):
    matrixWeighted = matrix
    columns = list(matrixWeighted.columns) # Gives list of column names
    columns.remove(columns[0]) # We need to multiply with weight all columns except 1st so, remove it from list
    k = 0  # to iterate weights
    # Loop through columns and then rows
    for col in columns:
        for row in matrixWeighted.index:
            matrixWeighted.at[row, col] = weights[k] * matrixWeighted[col][row]
        k = k + 1
    return matrixWeighted

######### TOPSIS Algorithm : Function (3) #########
def matrixFindBestAndWorst(matrix, impacts):
    columns = list(matrix.columns)
    columns.remove(columns[0])
    best = []
    worst = []
    k = 0  # to iterate impacts
    # Loop through columns and then rows
    for col in columns:
        if impacts[k] == '+':
            best.append(max(matrix[col]))
            worst.append(min(matrix[col]))
        else:
            best.append(min(matrix[col]))
            worst.append(max(matrix[col]))
        k = k + 1
    return (best, worst)

######### TOPSIS Algorithm : Function (4) #########
def matrixFindEuclideanDistance(matrix, best, worst):
    columns = list(matrix.columns)
    columns.remove(columns[0])
    sPlus = []
    sMinus = []
    for row in matrix.index:
        ideal_best_sum = 0
        ideal_worst_sum = 0
        k = 0
        for col in columns:
            best_diff = best[k] - matrix[col][row]
            worst_diff = worst[k] - matrix[col][row]
            ideal_best_sum = ideal_best_sum + ( best_diff ** 2 )
            ideal_worst_sum = ideal_worst_sum + ( worst_diff **2 )
            k = k + 1
        ideal_best_sum = math.sqrt(ideal_best_sum)
        ideal_worst_sum = math.sqrt(ideal_worst_sum)
        sPlus.append(ideal_best_sum)
        sMinus.append(ideal_worst_sum)
    return (sPlus, sMinus)

######### TOPSIS Algorithm : Function (5) #########
def matrixFindScoreAndFinalRanking(file, sPlus, sMinus):
    frame = pd.read_csv(file)
    TopsisScore = []
    
    for i in range(len(sPlus)):
        score = sPlus[i] + sMinus[i]
        score = sMinus[i] / score
        TopsisScore.append(score)

    frame['Topsis Score'] = TopsisScore
    ranks = pd.Series(TopsisScore)
    ranks = ranks.rank(ascending=False, method='min')
    frame['Rank'] = ranks
    frame['Rank'] = frame['Rank'].astype('int')
    return frame


def main():
    ## Check that in command line, no. of arguments provided are 5 (i.e. 4 parameters)
    if len(sys.argv) < 5 :
        print(f'Provide 4 parameters in this format: python 102017187.py data.csv \"1,1,1,2" "+,+,-,+\" result.csv')
        exit(0)
    if len(sys.argv) > 5 :
        print('Error: cannot pass more than 4 parameters')
        exit(0)

    # Read the arguments
    input_file_str = sys.argv[1]
    weights_str = sys.argv[2]
    impacts_str = sys.argv[3]
    result_file_str = sys.argv[4]

    # Validating input through various functions
    if checkInputFile(input_file_str):
        print(f"{input_file_str} is in correct format :)")


    Weights = check_weights(input_file_str,weights_str)
    if Weights:
        print(f"{weights_str} is in correct format :)")

    Impacts = check_impacts(input_file_str,impacts_str)
    if Impacts:
        print(f"{impacts_str} in correct format :)")

    if check_result_file(result_file_str):
        print(f"{result_file_str} in correct format :)")

    print(f"Generating Results and saving to {result_file_str} :)")

    # TOPSIS Algorithm (Task splitted into 5 functions)
    # (1)
    Matrix = matrixInputAndNormalise(input_file_str)
    # (2)
    Matrix_X_Weighted = matrixNormalizedAndWeighted(Matrix, Weights)
    # (3)
    (Best, Worst) = matrixFindBestAndWorst(Matrix_X_Weighted, Impacts)
    # (4)
    (SPlus, SMinus) = matrixFindEuclideanDistance(Matrix_X_Weighted, Best, Worst)
    # (5)
    MatrixFinal = matrixFindScoreAndFinalRanking(input_file_str, SPlus, SMinus)
    print('--------Final Matrix-------------')
    print(MatrixFinal)
    # Put data in csv file
    MatrixFinal.to_csv(result_file_str, index=False)

if __name__ == "__main__":
    main()