import pandas as pd
import os
import sys
import numpy as np

def main():
    if len(sys.argv) != 5:
        print("ERROR In Number Of Parameters: Enter 5 Parameters Only")
        print("USAGE : python <program.py> <InputDataFile> <Weights> <Impacts> <ResultFileName>")
        exit(1)

    # File Not Found error
    elif not os.path.isfile(sys.argv[1]):
        print(f"ERROR : {sys.argv[1]} Does not Exist!")
        exit(1)

    # File extension not csv 
    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print(f"ERROR : {sys.argv[1]} Is Not in CSV Format!")
        exit(1)
        
    else:
        ds= pd.read_csv(sys.argv[1])
        temp_ds=ds.copy()

        # less then 3 columns in input dataset
        if len(temp_ds.axes[1]) < 3:
            print("ERROR In Input file : File has less then 3 columns")
            exit(1)

        # Handeling non-numeric value
        for i in range(1, len(temp_ds.axes[1])):
            pd.to_numeric(ds.iloc[:, i], errors='coerce')
            ds.iloc[:, i].fillna((ds.iloc[:, i].mean()), inplace=True)

        # Handling errors of weighted and impact arrays
        try:
            weights = [int(i) for i in sys.argv[2].split(',')]
        except:
            print("ERROR In Weights : Check Input Again")
            exit(1)
        impact = sys.argv[3].split(',')
        for i in impact:
            if not (i == '+' or i == '-'):
                print("ERROR In Impact : Check Input Again")
                exit(1)

        # Checking number of column,weights and impacts is same or not
        if (len(temp_ds.axes[1]) != len(weights)+1 or len(temp_ds.axes[1]) != len(impact)+1):
            print("ERROR : Number of Weights, Number of impacts And Number of Columns Are Not Same!!")
            exit(1)

        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("ERROR : Output file extension is wrong")
            exit(1)
            
        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])

        Topsis(temp_ds, ds, weights, impact)

def Topsis(temp_ds, ds, weights, impact):
    # Normalizing the Data
    for i in range(1, len(ds.axes[1])):
        temp = 0
        for j in range(len(temp_ds)):
            temp = temp + temp_ds.iloc[j, i]**2
        temp = np.sqrt(temp)
        for j in range(len(temp_ds)):
            temp_ds.iat[j, i] = (temp_ds.iloc[j, i] / temp)*weights[i-1]

    # Calculating positive and negative values
    p_val = (temp_ds.max().values)[1:]
    n_val = (temp_ds.min().values)[1:]
    for i in range(1, len(ds.axes[1])):
        if impact[i-1] == '-':
            p_val[i-1], n_val[i-1] = n_val[i-1], p_val[i-1]

    # Calculating topsis score
    score = []
    for i in range(len(temp_ds)):
        temp_p = 0
        temp_n = 0
        for j in range(1, len(ds.axes[1])):
            temp_p = temp_p + np.square(p_val[j-1] - temp_ds.iloc[i, j])
            temp_n = temp_n + np.square(n_val[j-1] - temp_ds.iloc[i, j])
        temp_p, temp_n = np.sqrt(temp_p), np.sqrt(temp_n)
        score.append(temp_n/(temp_p + temp_n))
    ds['Topsis Score'] = score

    # calculating the rank according to topsis score
    ds['Rank'] = (ds['Topsis Score'].rank(method='max', ascending=False))
    ds = ds.astype({"Rank": int})

    # Writing the csv
    ds.to_csv(sys.argv[4], index=False)

if __name__ == "__main__":
    main()