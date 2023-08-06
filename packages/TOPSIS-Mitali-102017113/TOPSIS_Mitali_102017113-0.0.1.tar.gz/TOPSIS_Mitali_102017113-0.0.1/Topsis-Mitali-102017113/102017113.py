import sys
import pandas as pd
import numpy as np
import math

def topsis():
    try:
        if(len(sys.argv)!=5):
            raise
    except:
        print("Incorrect number of parameters")
        exit(0)

    try:
        dataframe=pd.read_csv(sys.argv[1])
    except FileNotFoundError:
        print("File not found")
        exit(0)

    weight = list(sys.argv[2].split(","))
    impact = list(sys.argv[3].split(","))
    ncol = len(dataframe.columns)

    try:
        if ncol<3:
            raise
    except:
        print("No of columns are less than 3.")
        exit(0)

    try:
        if len(impact) != (ncol-1):
            raise
    except:
        print("No of impacts!=columns.")
        exit(0)
    try:
        if len(weight) != (ncol-1):
            raise
    except:
        print("No of weights!=columns.")
        exit(0)

    try:
        if set(impact) != {'+', '-'}:
            raise
    except:
        print("Impacts should be either '+' or '-'.")
        exit(0)

    for index,row in dataframe.iterrows():
        try:
            float(row['P1'])
            float(row['P2'])
            float(row['P3'])
            float(row['P4'])
            float(row['P5'])
        except:
            dataframe.drop(index,inplace=True)

    dataframe["P1"] = pd.to_numeric(dataframe["P1"], downcast="float")
    dataframe["P2"] = pd.to_numeric(dataframe["P2"], downcast="float")
    dataframe["P3"] = pd.to_numeric(dataframe["P3"], downcast="float")
    dataframe["P4"] = pd.to_numeric(dataframe["P4"], downcast="float")
    dataframe["P5"] = pd.to_numeric(dataframe["P5"], downcast="float")
    df1 = dataframe.copy(deep=True)

    #normalize
    for i in range(1, ncol):
        temp = 0
        for j in range(len(dataframe)):
            temp = temp + math.pow(dataframe.iloc[j, i],2)
        temp = math.sqrt(temp)
        for j in range(len(dataframe)):
            dataframe.iat[j, i] = (float(dataframe.iloc[j, i])) / float(temp)*float(weight[i-2])

    #calculate v_pos, v_neg
        v_pos = (dataframe.max().values)[1:]
        v_neg = (dataframe.min().values)[1:]
        for i in range(1, ncol):
            if impact[i-2] == '-':
                v_pos[i-1], v_neg[i-1] = v_neg[i-1], v_pos[i-1]

    score = []
    pp = []
    nn = []

    for i in range(len(dataframe)):
        temp_p, temp_n = 0, 0
        for j in range(1, ncol):
            temp_p = temp_p + math.pow((v_pos[j-1] - dataframe.iloc[i, j]),2)
            temp_n = temp_n + (v_neg[j-1] - dataframe.iloc[i, j])**2
        temp_p, temp_n = math.sqrt(temp_p), math.sqrt(temp_n)
        score.append(temp_n/(temp_p + temp_n))
        nn.append(temp_n)
        pp.append(temp_p)


    df1['Topsis Score'] = score
    df1['Rank'] = (df1['Topsis Score'].rank(method='max', ascending=False))
    df1 = df1.astype({"Rank": int})
    df1.to_csv(sys.argv[4],index=False)


# topsis()