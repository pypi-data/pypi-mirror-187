import pandas as pd
from tabulate import tabulate
import os
import sys


def Calc_Values(t_filedata, numCol, imp):
    positiveValue = (t_filedata.max().values)[1:]
    negativeValue = (t_filedata.min().values)[1:]
    for i in range(1, numCol):
        if imp[i-1] == '-':
            positiveValue[i-1], negativeValue[i-1] = negativeValue[i-1], positiveValue[i-1]
    return positiveValue, negativeValue

def Normalize(t_filedata, numCol, wt):
    # normalizing the dataset for decrease the biasing in dataset
    for i in range(1, numCol):
        t = 0
        for j in range(len(t_filedata)):
            t = t + t_filedata.iloc[j, i]**2
        t = t**0.5
        for j in range(len(t_filedata)):
            t_filedata.iat[j, i] = (t_filedata.iloc[j, i] / t)*wt[i-1]
    return t_filedata

def topsis_pipy(t_filedata, filedata, numCol, wt, imp):
    # normalizing the array
    t_filedata = Normalize(t_filedata, numCol, wt)

    # Calculating positive and negative values
    positiveValue, negativeValue = Calc_Values(t_filedata, numCol, imp)

    # calculating topsis score and round to 4 decimal places
    score = []
    for i in range(len(t_filedata)):
        S_positive, S_negative = 0, 0
        for j in range(1, numCol):
            S_positive = S_positive + (positiveValue[j-1] - t_filedata.iloc[i, j])**2
            S_negative = S_negative + (negativeValue[j-1] - t_filedata.iloc[i, j])**2
        S_positive, S_negative = S_positive*0.5, S_negative*0.5
        score.append(round(S_negative/(S_positive + S_negative),4))
    filedata['Topsis Score'] = score

    # calculating the rank according to topsis score value
    filedata['Rank'] = (filedata['Topsis Score'].rank(
        method='max', ascending=False))
    filedata = filedata.astype({"Rank": int})

    # Writing into the output csv file
    filedata.to_csv(sys.argv[4], index=False)


def main():
    # Check the number of arguments
    if len(sys.argv) != 5:
        print("ERROR : Number of Command Line Arguments are not equal to 5")
        exit(1)

    # Check file found or not
    elif not os.path.isfile(sys.argv[1]):
        print(f"ERROR : {sys.argv[1]} Doesn't exist!!")
        exit(1)

    # Check the File extension
    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print(f"ERROR : {sys.argv[1]} is not csv!!")
        exit(1)

    else:
        filedata = pd.read_csv(sys.argv[1]) 
        t_filedata = pd.read_csv(sys.argv[1])
        numCol = len(t_filedata.columns.values)

        # if columns in the input data set is less than 3
        if numCol < 3:
            print("ERROR : Input file have less then 3 columns")
            exit(1)

        # Check for Handling non-numeric values
        for i in range(1, numCol):
            pd.to_numeric(filedata.iloc[:, i], errors='coerce')
            filedata.iloc[:, i].fillna((filedata.iloc[:, i].mean()), inplace=True)

        # Handling errors of weighted and imp arrays
        try:
            wt = [int(i) for i in sys.argv[2].split(',')]
        except:
            print("ERROR : Found in Weight array")
            exit(1)
        imp = sys.argv[3].split(',')
        for i in imp:
            if not (i == '+' or i == '-'):
                print("ERROR : Found in Impact array")
                exit(1)

        # Checking number of column,wt and imps is same or not
        if numCol != len(wt)+1 or numCol != len(imp)+1:
            print(
                "ERROR : Number of wt, number of imps and number of columns not same")
            exit(1)

        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("ERROR : Output file extension is wrong")
            exit(1)
        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])
        topsis_pipy(t_filedata, filedata, numCol, wt, imp)


if __name__ == "__main__":
    main()