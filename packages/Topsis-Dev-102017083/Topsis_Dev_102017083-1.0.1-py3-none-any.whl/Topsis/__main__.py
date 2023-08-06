from math import inf
import numbers
import sys
import numpy as np
import pandas as pd

def is_numeric(n):
    for i in range(0,len(n)-1):
        if isinstance(n[i], numbers.Real) == False :
            return False
    return True


def errorHandling(inputdata, weight, impact, Result):
    #exit if file is not in csv format
    if(inputdata.endswith('.csv') == False) :
        sys.exit("input csv files only\n")
    
    #handling file not found error    
    try:
        inputdata = pd.read_csv(inputdata)
    except FileNotFoundError:
        print("File  is not Found-- Wrong file")
    else:
        #exit if no. of columns are less than 3 
        col = inputdata.shape[1]
        if(col < 3):
            sys.exit("file must contain atleast 3 columns\n")
        # error if datatype is not numeric from 1st column onwards
        for i in range(1 , col):
            if(is_numeric(inputdata.iloc[:,i]) == False):
                sys.exit("Data type is not numeric numeric")

        # error if input weights and impacts are not separated by comma or specified number is incorrect
        if(weight.__contains__(',') == False):
            sys.exit("Weights must be separated by comma\n") 
   
        weight= weight.split(",")
        if(len(weight) != col-1):
            sys.exit(f"Mention {col-1} weights\n")


        if(impact.__contains__(',') == False):
            sys.exit("Impacts must be separated by comma\n") 
                 
        impact =impact.split(",")
        if(len(impact) != col-1):
            sys.exit(f"Mention {col-1} impacts\n")
        # check if impacts obtained are = or - only
        if set(impact) != {'+', '-'}:
            sys.exit("Only '+'or '-' impacts values are valid\n")
        # check if result file obtained is in csv format
        if(Result.endswith('.csv') == False) :
            sys.exit("input csv files only\n")

        return inputdata, weight, impact




def normaliseData(inputdata):
    root_sum_square= [0] * (inputdata.shape[1])

    for i in range(1, inputdata.shape[1]):
        sum=0
        for j in range(0, len(inputdata.iloc[:,i])):
            sum+= pow(inputdata.iloc[j,i] ,2)

        root_sum_square[i]= np.sqrt(sum)

    normal = inputdata.copy()
    for i in range(1, normal.shape[1]):
        for j in range(0, len(normal.iloc[:,i])):
            normal.iloc[j,i]/= root_sum_square[i]

    
    return normal

def assignWeights(norm, weights):
    for i in range(1, norm.shape[1]):
        for j in range(0, len(norm.iloc[:,i])):
            norm.iloc[j,i]*= weights[i-1]

    
    return norm


def calculateVJ(normal, impact):
    vjpositive= [0] * (normal.shape[1]-1)
    vjnegative= [0] * (normal.shape[1]-1)

    for i in range(1, normal.shape[1]):
        if(impact[i-1] == '+'):
            vjpositive[i-1]= -inf
            vjnegative[i-1]= inf
            
            for j in range(0, len(normal.iloc[:,i])):
                vjpositive[i-1]= max(vjpositive[i-1], normal.iloc[j,i])
                vjnegative[i-1]= min(vjnegative[i-1], normal.iloc[j,i])

        else:
            vjpositive[i-1]= inf
            vjnegative[i-1]= -inf
            
            for j in range(0, len(normal.iloc[:,i])):
                vjpositive[i-1]= min(vjpositive[i-1], normal.iloc[j,i])
                vjnegative[i-1]= max(vjnegative[i-1], normal.iloc[j,i])


    
    return vjpositive, vjnegative


def calculateSI(normal, vjpositive, vjnegative):
    #euclidean distance
    sipositive= [0] * (normal.shape[0])
    sinegative= [0] * (normal.shape[0])

    for i in range(0, normal.shape[0]):
        sum1=0
        sum2=0
        for j in range(1, normal.shape[1]):
            sum1+= pow(normal.iloc[i,j] -vjpositive[j-1] ,2)
            sum2+= pow(normal.iloc[i,j] -vjnegative[j-1] ,2)

        sipositive[i]= np.sqrt(sum1)
        sinegative[i]= np.sqrt(sum2)
    

    
    return sipositive, sinegative


def topsis(inputdata, weight, impact, Result):

    

    normal = normaliseData(inputdata)
    normal= assignWeights(normal, weight)
    vjpositive, vjnegative= calculateVJ(normal, impact)
    sipositive, sinegative= calculateSI(normal, vjpositive, vjnegative)

    for i in range(0, inputdata.shape[0]):
        inputdata.loc[i,"Topsis Score"]=  sinegative[i] / (sipositive[i] + sinegative[i])
    
    inputdata["Rank"] = inputdata["Topsis Score"].rank(method ='max')

    
    inputdata.to_csv(Result, index= False)




def main():
    #return if no.of arguments!= no.of columns
    n = len(sys.argv)
    if(n!=5):
        print("Incorrect number of arguments\n")
        return


    inputdata= sys.argv[1]
    weight= sys.argv[2]
    impact= sys.argv[3]
    Result= sys.argv[4]

    inputdata, weight, impact= errorHandling(inputdata,  weight, impact, Result)    

    weight = [eval(i) for i in weight]
    topsis(inputdata, weight, impact, Result)

if __name__ == "__main__":
    main()
