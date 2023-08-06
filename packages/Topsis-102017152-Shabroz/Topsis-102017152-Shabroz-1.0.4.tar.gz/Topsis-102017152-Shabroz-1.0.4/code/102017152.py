import pandas as pd
import numpy as np
import logging
import sys

def normalize(df, row, col):
    for j in range(col):
        sq = np.sqrt(sum(df.iloc[:, j]**2))
        for i in range(row):
            df.iloc[i, j] = df.iloc[i, j]/sq
    return df

#normalize(df , df.shape[0] , df.shape[1])
#print(df)

def weighted(df, weight, row, col):
    for j in range(col):
        for i in range(row):
            df.iloc[i,j] = df.iloc[i,j]*weight[j]
    return df

#weight=[1,1,1,1,1]
#weighted(df,weight , df.shape[0] , df.shape[1])

def calc_ideal_best_worst(sign, df, row,col):
    ideal_worst = []
    ideal_best = []
    for i in range(1,col):
        if sign[i] == 1:
            ideal_worst.append(min(df.iloc[:, i]))
            ideal_best.append(max(df.iloc[:, i]))
        else:
            ideal_worst.append(max(df.iloc[:, i]))
            ideal_best.append(min(df.iloc[:, i]))
    return (ideal_worst, ideal_best)

def euclidean_distance(df, ideal_worst, ideal_best, row,col):
    sp=[]
    sn=[]
    for i in range (row) :
        sneg = 0
        spos = 0
        for j in range(1,col):
            sneg += (df.iloc[i,j] - ideal_worst)**2
            spos += (df.iloc[i,j] - ideal_best)**2
            #print(sneg)
        sn.append(sum(sneg) ** 0.5)
        sp.append(sum(spos)** 0.5)
    sn = np.array(sn)
    sp = np.array(sp)
    return (sn,sp)


def performance_score(distance_best, distance_worst, row , col):
    score = []
    score = distance_worst/(distance_best + distance_worst)
    return score

def topsis(input, weight, sign ,output):
    print("in toposis")
    try:
        df = input
    except FileNotFoundError:
        logging.error("Input file provided not found")
        return
    newdf=df.drop('Fund Name', axis=1)
    print(newdf)
    row=newdf.shape[0]
    col=newdf.shape[1]
    if ',' not in weight:
        logging.error("Array weights should be separated by ','")
        return
    weights = weight.split(',')
    try:
        weights = list(map(int, weights))
    except ValueError:
        logging.error("Weights has non integral value")
        return
    if ',' not in sign:
        logging.error("Array impacts should be separated by ','")
        return
    impact = sign.split(',')
    for x in impact:
        if x != '+' and x != '-':
            logging.error("Impact must contain only '+' or '-'")
            return
    if(col<3):
        logging.error("Less Number of columns in Input File")
        return
    for i in range(row):
        rows = list(newdf.iloc[i])
        for j in range(1,col):
            try:
                rows[j] = pd.to_numeric(rows[j])
            except ValueError:
                logging.warning(f"Non numeric value encountered in input.csv at {i}th row and {j}th coln")
    if (col != len(weights) or col != len(impact)):
        logging.error("Length of inputs not match.")
        return

    newdf = normalize(newdf , row , col)
    newdf=weighted(newdf ,weights,row,col)
    (ideal_worst, ideal_best) = calc_ideal_best_worst(impact, newdf,row , col)
    (distance_worst, distance_best) = euclidean_distance(newdf, ideal_worst, ideal_best,row , col)
    score = performance_score(distance_best, distance_worst, row , col)
    df['Topsis Score'] =score
    df['Rank']=(df['Topsis Score'].rank(method='max',ascending=False)).astype('int64')
    pd.DataFrame(df).to_csv(output)
    print(newdf)
    print(df)

def main():
     filename = sys.argv[1]
     weight = sys.argv[2]
     sign = sys.argv[3]
     output = sys.argv[4]
     df=pd.read_csv(filename)
     topsis(df ,weight , sign, output)

if __name__ == "__main__":
    main()
