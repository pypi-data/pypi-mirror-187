# Multiple Criteria Decision Making ( MCDM ) using TOPSIS

from math import inf
import numbers
import sys
import numpy as np
import pandas as pd

def vectorNormalization(inputFileName):

    #calculate root of sum of squares
    root_sum_square= [0] * (inputFileName.shape[1])

    for i in range(1, inputFileName.shape[1]):
        sum=0
        for j in range(0, len(inputFileName.iloc[:,i])):
            sum+= pow(inputFileName.iloc[j,i] ,2)

        root_sum_square[i]= np.sqrt(sum)

    norm = inputFileName.copy()

    #Find Normalized Decision Metric
    # Divide every column value its Root of sum of squares
    # value in every cell is known as Normalized Performance Value
    for i in range(1, norm.shape[1]):
        for j in range(0, len(norm.iloc[:,i])):
            norm.iloc[j,i]/= root_sum_square[i]

    print("\nNormalised Decision Metrix:\n",norm)
    return norm

def WeightAssignment(norm, Weights):
    # calculate weight * Normalized performance value
    for i in range(1, norm.shape[1]):
        for j in range(0, len(norm.iloc[:,i])):
            norm.iloc[j,i]*= Weights[i-1]

    print("\nWeighted Normalized Decision Matrix:\n",norm)
    return norm


def calculateVJs(norm, Impacts):
    # calculate ideal best value and ideal worst value
    # -ve means : min is best
    # +ve means : max is best
    vjpos= [0] * (norm.shape[1]-1)
    vjneg= [0] * (norm.shape[1]-1)

    for i in range(1, norm.shape[1]):
        if(Impacts[i-1] == '+'):
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
    # Calculate Euclidean distance from ideal best value and ideal worst value
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


def topsis(inputFileName,  Weights, Impacts, resultFileName):

    print("Original data\n", inputFileName)

    norm = vectorNormalization(inputFileName)
    norm= WeightAssignment(norm, Weights)
    vjpos, vjneg= calculateVJs(norm, Impacts)
    sipos, sineg= calculateSIs(norm, vjpos, vjneg)


    # Calculate Performance score

    for i in range(0, inputFileName.shape[0]):
        inputFileName.loc[i,"Topsis Score"]=  sineg[i] / (sipos[i] + sineg[i])
    
    inputFileName["Rank"] = inputFileName["Topsis Score"].rank(method ='max')

    print("\n\n Dataset with Topsis Scores and rank\n")
    print(inputFileName)
    
    print(f"Saving to {resultFileName}")
    inputFileName.to_csv(resultFileName, index= False)



def is_numeric(n):
    for i in range(0,len(n)-1):
        if isinstance(n[i], numbers.Real) == False :
            return False
    return True


def checkInputs(inputFileName,  Weights, Impacts, resultFileName):
    
    # inputFileName must be csv file
    if(inputFileName.endswith('.csv') == False) :
        sys.exit("Only csv files permitted\n")
    
    # Handling of "File not Found" exception
    try:
        data = pd.read_csv(inputFileName)
    except FileNotFoundError:
        print("File not Found")
    else:
        #Input file must contain three or more columns
        col = data.shape[1]
        if(col < 3):
            sys.exit("input file must contain 3 or more columns\n")


        # From 2nd to last  columns must contain numeric values only 
        for i in range(1 , col):
            if(is_numeric(data.iloc[:,i]) == False):
                sys.exit("Data type should be numeric")

        # Impacts and Weights must be separated by ','
        # Number of Weights , numbers of impacts and number of columns 
        if(Weights.__contains__(',') == False):
            sys.exit("Weights must be separated by comma\n") 
   
        Weights= Weights.split(",")
        if(len(Weights) != col-1):
            sys.exit(f"Specify {col-1} weights\n")


        if(Impacts.__contains__(',') == False):
            sys.exit("Impacts must be separated by comma\n") 
                 
        Impacts =Impacts.split(",")
        if(len(Impacts) != col-1):
            sys.exit(f"Specify {col-1} impacts\n")
        

        # Impacts must be either +ve or -ve 
        if set(Impacts) != {'+', '-'}:
            sys.exit("Only '+', '-' impacts are allowed\n")

        if(resultFileName.endswith('.csv') == False) :
            sys.exit("Only csv files permitted\n")

        return data, Weights, Impacts


def main():
    # Checking Correct number of argumnets 
    # i.e inputFileName , Weights , Impacts , resultFileName
    n = len(sys.argv)
    if(n!=5):
        print("Incorrect number of arguments\n")
        return


    inputFileName = sys.argv[1]
    Weights = sys.argv[2]
    Impacts = sys.argv[3]
    resultFileName = sys.argv[4]

    # show appropriate message for wrong inputs
    inputFileName,  Weights, Impacts= checkInputs( inputFileName,  Weights, Impacts, resultFileName)    

    Weights = [eval(i) for i in Weights]
 
    topsis(inputFileName,  Weights, Impacts, resultFileName)

if __name__ == "__main__":
    main()