from math import inf
import numbers
import sys
import numpy as np
import pandas as pd

def normaliseData(data):
    root_sum_square= [0] * (data.shape[1])

    for i in range(1, data.shape[1]):
        sum=0
        for j in range(0, len(data.iloc[:,i])):
            sum+= pow(data.iloc[j,i] ,2)

        root_sum_square[i]= np.sqrt(sum)

    norm = data.copy()
    for i in range(1, norm.shape[1]):
        for j in range(0, len(norm.iloc[:,i])):
            norm.iloc[j,i]/= root_sum_square[i]

    print("\nNormalised data\n",norm)
    return norm

def assignWeights(norm, weights):
    for i in range(1, norm.shape[1]):
        for j in range(0, len(norm.iloc[:,i])):
            norm.iloc[j,i]*= weights[i-1]

    print("\nAfter assigning weights\n",norm)
    return norm


def calculateVJs(norm, impacts):
    vjpos= [0] * (norm.shape[1]-1)
    vjneg= [0] * (norm.shape[1]-1)

    for i in range(1, norm.shape[1]):
        if(impacts[i-1] == '+'):
            vjpos[i-1]= -inf
            vjneg[i-1]= inf
            
            for j in range(0, len(norm.iloc[:,i])):
                vjpos[i-1]= max(vjpos[i-1], norm.iloc[j,i])
                vjneg[i-1]= min(vjneg[i-1], norm.iloc[j,i])

        else:
            vjpos[i-1]= inf
            vjneg[i-1]= -inf
            
            for j in range(0, len(norm.iloc[:,i])):
                vjpos[i-1]= min(vjpos[i-1], norm.iloc[j,i])
                vjneg[i-1]= max(vjneg[i-1], norm.iloc[j,i])


    print("\nvjpos: ",vjpos)
    print("vjneg: ",vjneg)
    return vjpos, vjneg


def calculateSIs(norm, vjpos, vjneg):
    #euclidean distance
    sipos= [0] * (norm.shape[0])
    sineg= [0] * (norm.shape[0])

    for i in range(0, norm.shape[0]):
        sum=0
        sum2=0
        for j in range(1, norm.shape[1]):
            sum+= pow(norm.iloc[i,j] -vjpos[j-1] ,2)
            sum2+= pow(norm.iloc[i,j] -vjneg[j-1] ,2)

        sipos[i]= np.sqrt(sum)
        sineg[i]= np.sqrt(sum2)
    

    print("\nsipos: ",sipos)
    print("\nsineg: ", sineg)
    return sipos, sineg


def topsis(data, weights, impacts, result):

    print("Original data\n", data)

    norm = normaliseData(data)
    norm= assignWeights(norm, weights)
    vjpos, vjneg= calculateVJs(norm, impacts)
    sipos, sineg= calculateSIs(norm, vjpos, vjneg)

    for i in range(0, data.shape[0]):
        data.loc[i,"Topsis Score"]=  sineg[i] / (sipos[i] + sineg[i])
    
    data["Rank"] = data["Topsis Score"].rank(method ='max')

    print("\n\n Dataset with Topsis Scores and rank\n")
    print(data)
    
    print(f"Saving to {result}")
    data.to_csv(result, index= False)



def is_numeric(n):
    for i in range(0,len(n)-1):
        if isinstance(n[i], numbers.Real) == False :
            return False
    return True


def errorHandling(data, weights, impacts, result):
    #error handling
    if(data.endswith('.csv') == False) :
        sys.exit("Only csv files permitted\n")
    
        
    try:
        data = pd.read_csv(data)
    except FileNotFoundError:
        print("File not Found: Wrong file or file path")
    else:

        col = data.shape[1]
        if(col < 3):
            sys.exit("input file must contain 3 or more columns\n")

        for i in range(1 , col):
            if(is_numeric(data.iloc[:,i]) == False):
                sys.exit("Data type should be numeric")


        if(weights.__contains__(',') == False):
            sys.exit("Weights must be separated by comma\n") 
   
        weights= weights.split(",")
        if(len(weights) != col-1):
            sys.exit(f"Specify {col-1} weights\n")


        if(impacts.__contains__(',') == False):
            sys.exit("Impacts must be separated by comma\n") 
                 
        impacts =impacts.split(",")
        if(len(impacts) != col-1):
            sys.exit(f"Specify {col-1} impacts\n")
        
        if set(impacts) != {'+', '-'}:
            sys.exit("Only '+', '-' impacts are allowed\n")

        if(result.endswith('.csv') == False) :
            sys.exit("Only csv files permitted\n")

        return data, weights, impacts


def main():
    n = len(sys.argv)
    if(n!=5):
        print("Incorrect number of arguments\n")
        return


    data= sys.argv[1]
    weights= sys.argv[2]
    impacts= sys.argv[3]
    result= sys.argv[4]

    data, weights, impacts= errorHandling(data,  weights, impacts, result)    

    weights = [eval(i) for i in weights]
 
    topsis(data, weights, impacts, result)

if __name__ == "__main__":
    main()
