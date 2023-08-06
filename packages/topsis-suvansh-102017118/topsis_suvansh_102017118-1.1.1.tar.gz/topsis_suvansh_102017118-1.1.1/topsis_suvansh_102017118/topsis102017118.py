import pandas as pd
import numpy as np
import sys

def validate_data(input_file, weights, impacts):

    try:
        matrix = pd.read_csv(input_file)
    except:
        print("Error: Invalid input file")
        sys.exit(1)

    if matrix.shape[1] < 3:
        print("Error: Invalid input file, must have at least 3 columns")
        sys.exit(1)

    try:
        weights = np.array(weights, dtype=float)
        impacts = np.array(impacts)
    except Exception as e:
        print(e)
        print("Error: Invalid weights or impacts")
        sys.exit(1)

    try:
        if len(weights) != matrix.shape[1] - 1 or len(impacts) != matrix.shape[1] - 1:
            print("Error: Invalid number of weights or impacts")
            sys.exit(1)
    except:
        print("Error: Invalid weights or impacts, must be separated by commas")
        sys.exit(1)

    for col in matrix.columns[1:]:
        if not pd.api.types.is_numeric_dtype(matrix[col]):
            print("Error: Invalid input file, all columns must be numeric")
            sys.exit(1)

    if not all([impact in ["+", "-"] for impact in impacts]):
        print("Error: Invalid impacts, must be either + or -")
        sys.exit(1)

    if not all([weight > 0 for weight in weights]):
        print("Error: Invalid weights, must be positive")
        sys.exit(1)

    return matrix, weights, impacts
def topsis(matrix, weights, impact):

    raw_matrix = matrix.drop(matrix.columns[0], axis=1)
    impact = np.where(impact == "+", 1, -1)
    raw_matrix = raw_matrix / np.sqrt(np.sum(raw_matrix**2, axis=0))
    weighted_matrix = raw_matrix * weights
    ideal_best = np.amax(weighted_matrix * impact, axis=0).abs()
    ideal_worst = np.amin(weighted_matrix * impact, axis=0).abs()
    Si_best = np.sqrt(np.sum((weighted_matrix - ideal_best) ** 2, axis=1))
    Si_worst = np.sqrt(np.sum((weighted_matrix - ideal_worst) ** 2, axis=1))
    performance_score = Si_worst / (Si_best + Si_worst)
    rank = performance_score.rank(ascending=False).astype(int)
    matrix["Performance Score"] = performance_score
    matrix["Rank"] = rank

    return matrix

def start():
    if len(sys.argv) != 5:
        print("Error: Invalid number of arguments")
        sys.exit(1)
    input_file = sys.argv[1]
    weights = sys.argv[2].split(",")
    impacts = sys.argv[3].split(",")
    output_file = sys.argv[4]
    matrix, weights, impacts = validate_data(input_file, weights, impacts)
    result = topsis(matrix, weights, impacts)
    result.to_csv(output_file, index=False)

    print("Output saved to", output_file)

if __name__ == "__main__":
    start()
