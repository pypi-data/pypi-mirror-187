import pandas as pd
import numpy as np
import sys 
from sklearn.preprocessing import StandardScaler,MinMaxScaler
import codecs

# check for correct number of command line arguments
def checkSysArgs():
    
    if len(sys.argv) <2:
        print("Please provide an input file. Proper usage: python TOPSIS-Jayati-102003082 <input_csv> <weights> <impacts> <output_csv>")
        return False
    if len(sys.argv) >5:
        
        print("Ignoring extra args. Proper usage: python TOPSIS-Jayati-102003082 <input_csv> <weights> <impacts> <output_csv>")
        return False
    
    if not sys.argv[1].endswith(".csv"):   # check that input file is a csv
            print("Error: Input file must be in csv format.")
            sys.exit()
    
    return True

def checkInputCSV():
     input_file=None
     try:
        
        input_file = pd.read_csv(sys.argv[1],lineterminator='\n',sep=',',encoding='utf-8',engine='python',error_bad_lines=False)
     except FileNotFoundError:
        print(f"Error: {sys.argv[1]} not found.")
        return False
     
     #Checking number of columns 
     if(input_file.shape[1]<3):
        print("Error: Input file must have atleast 3 columns")
        return False
    
    
     return True

# function to calculate TOPSIS technique
def topsis_validate(data, weights, impacts):
    data_to_use=data.iloc[:,data.columns != 'Fund Name']
    # normalize the data
    mm=MinMaxScaler()
    data_norm = mm.fit_transform(data_to_use)
    #data_norm = data_to_use / np.linalg.norm(data_to_use, axis=0)
    
    # create weight matrix
    weight_matrix = np.array(weights)
    
    # create impact matrix
    impact_matrix = np.array(impacts)
    
    # calculate weighted normalized data
    weighted_norm_data = data_norm.dot(weight_matrix)
    
    # calculate ideal solution (positive and negative)
    positive_ideal = np.max(weighted_norm_data, axis=0)
    negative_ideal = np.min(weighted_norm_data, axis=0)
    
    # calculate the distance from positive and negative ideal solutions
    positive_dist = np.sqrt(np.sum((weighted_norm_data - positive_ideal)**2, axis=0))
    negative_dist = np.sqrt(np.sum((weighted_norm_data - negative_ideal)**2, axis=0))
    
    # calculate relative closeness
    relative_closeness = negative_dist / (positive_dist + negative_dist)
    
    # create a dataframe to store results

    data["topsis_score"] = np.sqrt(np.sum((data_to_use - positive_ideal)**2, axis=1))
    data["topsis_rank"] = data["topsis_score"].rank(ascending=False)
    data=data.sort_values(by=['topsis_rank'] , ascending=True)

    return data
 
def outputFile(results):
    
    results.to_csv(sys.argv[4], index=False, header=True)


#main 

if __name__ == '__main__':
    if(not checkSysArgs()):
        sys.exit(0)

    #Checking for correct string values for weights and impacts
    try:
        weights = np.array([float(x) for x in sys.argv[2].split(",")])
    except ValueError:
        print("Error: Invalid format for weights. Must be a string of comma-separated positive numeric values.")
        sys.exit()
    # check that impacts are in correct format
    if not all(x in ["+", "-"] for x in sys.argv[3].split(",")):
        print("Error: Invalid format for impacts. Must be a string of comma-separated + or - symbols.")
        sys.exit()
    
    input_file = pd.read_csv(sys.argv[1],sep=',',encoding='utf-8',engine='python',error_bad_lines=False)
    
    
    results = topsis_validate(input_file, pd.Series(sys.argv[2].split(',')).astype(int), pd.Series(sys.argv[3].split(',')))
    
    outputFile(results)



    
    
    
    
    








