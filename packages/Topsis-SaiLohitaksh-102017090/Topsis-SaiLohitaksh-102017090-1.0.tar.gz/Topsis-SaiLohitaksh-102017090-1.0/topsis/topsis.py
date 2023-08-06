import sys
import numpy as np
import pandas as pd

def topsis(weights, impacts, data):
    m, n = np.shape(data)
    data = data[:, 1:]
    weights = np.array(weights) / sum(weights)
    impacts = np.array([1 if i == '+' else -1 for i in impacts])
    data = data * weights
    data = data * impacts
    positive_ideal = np.amax(data, axis=0)
    negative_ideal = np.amin(data, axis=0)
    ci = np.sqrt(np.sum((data - positive_ideal) ** 2, axis=1)) + np.sqrt(np.sum((data - negative_ideal) ** 2, axis=1))
    mcdm = np.column_stack((data[:,0], ci, np.argsort(ci)[::-1]+1))
    return mcdm

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Error: Incorrect number of parameters. Usage: python program.py InputDataFile Weights Impacts ResultFileName")
        sys.exit()

    input_file = sys.argv[1]
    weights = [float(i) for i in sys.argv[2].split(',')]
    impacts = sys.argv[3].split(',')
    result_file = sys.argv[4]

    try:
        data = pd.read_csv(input_file)
        data = data.apply(pd.to_numeric, errors='coerce')
        data = data.values.tolist()
    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found")
        sys.exit()

    if len(weights) != len(data[0])-1:
        print("Error: Number of weights must be same as number of columns in the input file")
        sys.exit()

    if len(impacts) != len(data[0])-1:
        print("Error: Number of impacts must be same as number of columns in the input file")
        sys.exit()

    for impact in impacts:
        if impact != '+' and impact != '-':
            print("Error: Impacts must be either + or -")
            sys.exit()
    data = np.array(data)

    result = topsis(weights, impacts, data)

    result_df = pd.DataFrame(result, columns = ['Object/Variable','Topsis Score','Rank'])
    result_df.to_csv(result_file, index=False)
    print(f"Result has been written to {result_file}")


