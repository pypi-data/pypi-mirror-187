import pandas as pd
import numpy as np
import sys

# class Topsis:
def topsis(data,weight,impact,result):
    if not sys.argv[1].endswith(".csv"):
        print("Error : Data file is not of .csv format")
        return  

    try:
        df = pd.read_csv(data)
    except FileNotFoundError:
        print("Error : csv file not found. Kindly ensure the file path is correct/file exists.")
        return   

    if weight.__contains__(',')==False:
        print("Error : Separate weights with ','")
        return

    if impact.__contains__(',')==False:
        print("Error : Separate impacts with ','")
        return    

    weights = weight.split(',')
    try:
        weights = list(map(float,weights))
    except ValueError:
        print("Error : Weight parameter contains non-integral value(s)")
        return

    impact = impact.split(',')
    for x in impact:
        if x != '+' and x != '-':
            print("Error : Impact must be contain either '+' or '-'")
            return

    if(len(df.columns) < 3):
        print("Error : Less Number of columns in input file")
        return

    df1 = df.drop('Fund Name', axis=1)
    rows = len(df1)
    columns = len(df1.iloc[0,:])

    if(len(weights)!=columns):
        print("Error : Incorrect number of weight values provided")
        return

    if(len(impact)!=columns):
        print("Error : Incorrect number of impact values provided")
        return

    #Calculating root of sum of squares for every column
    denominator = df1.apply(np.square).apply(np.sum,axis = 0).apply(np.sqrt)

    #Calculating weighted normalized decision matrix 
    for i in range(columns):
        for j in range(rows):
            df1.iat[j, i] = (df1.iloc[j, i] / denominator[i]) * weights[i]

    ideal_best = (df1.max().values)
    ideal_worst = (df1.min().values)
    for i in range(columns):
        if impact[i] == '-':
            ideal_best[i], ideal_worst[i] = ideal_worst[i], ideal_best[i]

    #Calculating Euclidean distance
    Topsis_Score = []
    for i in range(rows):
        Euclidean_p = 0
        Euclidean_n = 0
        for j in range(columns):
            Euclidean_p += pow((ideal_best[j] - df1.iloc[i, j]),2)
            Euclidean_n += pow((ideal_worst[j] - df1.iloc[i, j]),2)
            
        Euclidean_p = pow(Euclidean_p,0.5)
        Euclidean_n = pow(Euclidean_n,0.5)
        Topsis_Score.append(Euclidean_n/(Euclidean_p + Euclidean_n))

    df['Topsis Score'] = Topsis_Score
    df['Rank'] = (df['Topsis Score'].rank(method='max', ascending=False))
    df.to_csv(result)

data=sys.argv[1]
weight=sys.argv[2]
impact=sys.argv[3]
result=sys.argv[4]
if len(sys.argv)!=5:
    print("Error : Incorrect number of arguments passed!")

topsis(data,weight,impact,result)
# print(len(sys.argv))
