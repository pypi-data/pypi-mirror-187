import pandas as pd
import sys
import math
import numpy as np
import time

def topsis():
    if len(sys.argv)!= 5:
        print("Error: Provide correct input format <InputDataFile> <Weights> <Impacts> <ResultFileName>")
        quit()
    if not sys.argv[1].lower().endswith('.csv') or not sys.argv[4].lower().endswith('.csv'):
        print("Error: input and output file format should be .csv")
        quit()
    if(len(sys.argv[2]) != len(sys.argv[3])):
        print("Error: Number of weights and number of impacts passed dont match")
        quit()
    i=0
    while i<len(sys.argv[3]):
        if sys.argv[3][i] not in ["+","-"]:
            print("Error: The impacts should be either '+'/'-'")
            quit()
        i+=2
    try:
        df = pd.read_csv(sys.argv[1])
        dataset = pd.read_csv(sys.arg[1])
    except:
        print("Error: Cannot find the file")
        quit()

    df = pd.read_csv(sys.argv[1])
    dataframe = np.array(df.values.tolist())
    dataframe = dataframe[:,1:] # dropping first column
    weights = sys.argv[2]
    rows, col = dataframe.shape
    for i in range(col):
        temp=0
        for ele in dataframe[:,i]:
            temp= temp + math.pow(float(ele),2)
        temp = temp**0.5
        for k in range (rows):
            dataframe[k][i]=(float(dataframe[k][i])/temp)*float(weights[i])
   

              ## this becomes WEIGHTED NORMALIZED MATRIX

    impacts=sys.argv[3]
    ideal_best = []
    ideal_worst = []
    for i in range(col):
        if impacts[i] == "+":
            ideal_best.append(max(dataframe[:,i]))
            ideal_worst.append(min(dataframe[:,i]))
        elif impacts[i] == "-":
            ideal_best.append(min(dataframe[:,i]))
            ideal_worst.append(max(dataframe[:,i]))

    #score_positive = []
    #score_negeitive = []
    Performance_score = []
    for i in range(rows):
        pscore = 0
        nscore = 0
        for j in range(col):
            pscore+=math.pow(float(dataframe[i][j])-float(ideal_best[j]),2)
            nscore += math.pow(float(dataframe[i][j]) - float(ideal_worst[j]), 2)
        pscore = pscore**0.5 #euclidean distance from ideal best 
        nscore = nscore**0.5 #euclidean distance from idela worst
        Performance_score.append(nscore/(pscore + nscore))
    
    dataset['Topsis Score'] = Performance_score
    ## we got our performance score
    dataset['Rank'] = (dataset['Topsis Score'].rank(method='max', ascending=False))
    dataset = dataset.astype({"Rank": int})
    dataset.to_csv(sys.argv[4], index=False)
   
    print("Success!")


if __name__ == '__main__':
    topsis()

