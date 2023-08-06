import sys
import numpy as np
import pandas as pd
import math

def main():
    print(topsis("102003299_data.csv","2,2,3,3,4","-,+,-,+,-","result.csv"))

def topsis(dataset,weight,impact,result):

    data = pd.read_csv(dataset)
    weights = weight
    weights = list(map(int,weights.split(",")))
    impacts = impact
    impacts = list(impacts.split(","))

    output_file = result

    df=data.drop("Fund Name",axis=1,inplace=False)
    df=np.copy(df)

    row_size = len(df)
    col_size = len(df[0])
    col_size

    normalised_data = np.copy(df)
    squared_sum = np.zeros(col_size)
    normalised_data


    for i in range(row_size):
        for j in range(col_size):
            squared_sum[j]+=df[i, j]**2


    for i in range(row_size):
        for j in range(col_size):
            normalised_data[i,j]=df[i,j]/(pow(squared_sum[j],0.5))


    weight_data=np.copy(normalised_data)

    for i in range(row_size):
        for j in range(col_size):
            weight_data[i,j]=weight_data[i,j]*weights[j]


    worst_case = np.zeros(col_size)
    best_case = np.zeros(col_size)


    for i in range(col_size):
        if impacts[i]=="+":
            best_case[i] = max(weight_data[:,i])
            worst_case[i] = min(weight_data[:,i])
        else :
            best_case[i] = min(weight_data[:,i])
            worst_case[i] = max(weight_data[:,i])


    spositive = np.zeros(row_size)
    snegative = np.zeros(row_size)


    for i in range(row_size):
        temppos=0
        tempneg=0
        for j in range(col_size):
            temppos+= (weight_data[i][j]-best_case[j])**2
            tempneg+= (weight_data[i][j]-worst_case[j])**2

        spositive[i]=pow(temppos,0.5)
        snegative[i]=pow(tempneg,0.5)


    performance = np.zeros(row_size)
    performance = snegative/(snegative+spositive)


    rank = (-performance).argsort().argsort()
    rank=rank+1
    rank=rank.reshape(row_size,1)


    data["Topsis Rank"] = rank

    return data

if __name__ == "__main__":
    main()