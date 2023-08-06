import pandas as pd
import os
import sys

def main():
    # total number of arguments
    if len(sys.argv) != 5:
        print("USAGE : python topsis.py input_file.csv '1,1,1,2,1' '+,+,-,+,+' result.csv ")
        exit(1)

    # File Not Found error
    elif not os.path.isfile(sys.argv[1]):
        print(f"ERROR : {sys.argv[1]} Don't exist!!")
        exit(1)

    # File extension not csv
    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print(f"ERROR : {sys.argv[1]} is not csv!!")
        exit(1)

    else:
        dataset = pd.read_csv(sys.argv[1])
        temp_dataset = pd.read_csv(sys.argv[1])
        numcol = len(temp_dataset.columns.values)

        # less than 3 columns in input dataset
        if numcol < 3:
            print("ERROR : Input file have less then 3 columns")
            exit(1)

        # Handling non-numeric value
        for i in range(1, numcol):
            pd.to_numeric(dataset.iloc[:, i], errors='coerce')
            dataset.iloc[:, i].fillna(
                (dataset.iloc[:, i].mean()), inplace=True)

        # Handling errors of weighted and impact arrays
        try:
            weights = [int(i) for i in sys.argv[2].split(',')]
        except:
            print("ERROR : In weights array please check again")
            exit(1)
        impact = sys.argv[3].split(',')
        for i in impact:
            if not (i == '+' or i == '-'):
                print("ERROR : In impact array please check again")
                exit(1)

        # Checking number of column,weights and impacts is same or not
        if numcol != len(weights)+1 or numcol != len(impact)+1:
            print("length of weights", len(weights))
            print("length of impacts", len(impact))
            print("length of col", numcol)
            print(
                "ERROR : Number of weights, number of impacts and number of columns not same")
            exit(1)

        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("ERROR : Output file extension is wrong")
            exit(1)
        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])
        # print(" No error found\n\n Applying Topsis Algorithm...\n")
        topsis_pipy(temp_dataset, dataset, weights, impact)


def Normalize(temp_dataset, weights):

    numcol = len(temp_dataset.columns.values)
    for i in range(1, numcol):
        temp = 0
        for j in range(len(temp_dataset)):
            temp = temp + temp_dataset.iloc[j, i]**2
        temp = temp**0.5
        for j in range(len(temp_dataset)):
            temp_dataset.iat[j, i] = (
                temp_dataset.iloc[j, i] / temp)*weights[i-1]
    return temp_dataset


def Calc_Values(temp_dataset, impact):

    numcol = len(temp_dataset.columns.values)
    p_sln = (temp_dataset.max().values)[1:]
    n_sln = (temp_dataset.min().values)[1:]
    for i in range(1, numcol):
        if impact[i-1] == '-':
            p_sln[i-1], n_sln[i-1] = n_sln[i-1], p_sln[i-1]
    return p_sln, n_sln


def topsis_pipy(temp_dataset, dataset, weights, impact):

    numcol = len(temp_dataset.columns.values)
    temp_dataset = Normalize(temp_dataset, weights)
    p_sln, n_sln = Calc_Values(temp_dataset, impact)

    score = []
    for i in range(len(temp_dataset)):
        temp_p, temp_n = 0, 0
        for j in range(1, numcol):
            temp_p = temp_p + (p_sln[j-1] - temp_dataset.iloc[i, j])**2
            temp_n = temp_n + (n_sln[j-1] - temp_dataset.iloc[i, j])**2
        temp_p, temp_n = temp_p**0.5, temp_n**0.5
        score.append(temp_n/(temp_p + temp_n))
    dataset['Topsis Score'] = score

    # calculating the rank according to topsis score
    dataset['Rank'] = (dataset['Topsis Score'].rank(
        method='max', ascending=False))
    dataset = dataset.astype({"Rank": int})

    # Writing the csv
    dataset.to_csv(sys.argv[4], index=False)

if __name__ == "__main__":
    inputFileName = sys.argv[1]
    weights = sys.argv[2]
    impact = sys.argv[3]
    outputFileName = sys.argv[4]
    main()
