
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import sys 
import os.path
import numpy as np
from pandas.api.types import is_numeric_dtype


def normalize(matrix):
    norm = np.linalg.norm(matrix, axis = 0)
    matrix = np.divide(matrix,norm)
    return matrix


def apply_weights(matrix, weights):
    matrix = np.multiply(matrix,weights)
    return matrix



def find_topsis_score(matrix,impacts):
	rows,cols = np.shape(matrix)
	ideal_best = []
	ideal_worst = []
	for j in range(cols):
		if(impacts[j]==1):
			ideal_best.append(np.max(matrix[:,j]))
			ideal_worst.append(np.min(matrix[:,j]))
		else:
			ideal_best.append(np.min(matrix[:,j]))
			ideal_worst.append(np.max(matrix[:,j]))
	ideal_best = np.array(ideal_best)
	ideal_worst = np.array(ideal_worst)
	positive_score = np.linalg.norm(matrix - ideal_best, axis=1)
	negative_score = np.linalg.norm(matrix - ideal_worst, axis=1)
	topsis_score = np.divide(negative_score, np.add(negative_score ,positive_score))
	return topsis_score


def find_ranks(topsis_score):
	temp = -np.sort(-topsis_score)
	rank = [np.where(temp==x)[0][0]+1 for x in topsis_score]
	return rank

def main():
    
    if len(sys.argv)!=5:
        print("No. Of Arguments Needed = 5")
        sys.exit(1)


    if(os.path.exists(sys.argv[1])==False):
        print("File Doesn't Exist")
        sys.exit(1)


    file=pd.read_csv(sys.argv[1])
    if len(file.columns)<3:
        print("No of Columns Required -> Atleast 3")
        sys.exit(1)



    for j in range(1,len(file.columns)):
        if(is_numeric_dtype(file.iloc[:,j])==False):
            print("One or More Column Doesn't have all numeric values")
            sys.exit(1)


    weights_string = sys.argv[2] 
    impacts_string = sys.argv[3]



    weights_temp=weights_string.split(",")
    if len(weights_temp)!=len(file.columns)-1:
        print("Weights not seperated by ,")
        sys.exit(1)



    impacts_temp=impacts_string.split(",")
    if len(impacts_temp)!=len(file.columns)-1:
        print("Impacts not seperated by ,")
        exit(1)


    impacts = impacts_string.split(",")
    for i in range(len(impacts)):
        if(impacts[i]=='+'):
            impacts[i]=1
        elif(impacts[i]=='-'):
            impacts[i]=-1
        else:
            print('Invalid Impacts String')
            sys.exit(1)
    impacts=np.array(impacts)



    weights = weights_string.split(',')
    try:
        weights = [float(i) for i in weights]
        weights = np.array(weights)
    except:
            print("Invalid Weights")
            sys.exit(1)


    if((len(impacts)==len(weights) and len(impacts)==(len(file.columns)-1))==False):
        print("No. of weights = No. of impacts = No. of columns (2 to last) not satisfied")
        sys.exit(1)
        
    df = file.iloc[:,1:]
    df = np.array(df)


    matrix = normalize(df)
    matrix = apply_weights(matrix, weights)
    topsis_score = find_topsis_score(matrix, impacts)
    ranks = find_ranks(topsis_score)


    file['Topsis_score'] = topsis_score
    file['Ranks'] = ranks
    file.to_csv(sys.argv[4], index = False)

if __name__=='__main__':
    main()

