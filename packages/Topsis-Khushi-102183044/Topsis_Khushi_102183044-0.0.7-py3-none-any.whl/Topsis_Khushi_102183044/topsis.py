# Importing the required packages
import sys
import pandas as pd
import os
import math as m

# Function to check whether weights and impacts are comma separated or not
def checkFormat(w):
    for i in range(1, len(w), 2):
        if w[i] == ',':
            continue
        else:
            return False
    return True

def checkConstraints():

    # Checking the number of arguments provided in the command
    if len(sys.argv) == 5:

        # Parsing the input file name
        inputFileName = sys.argv[1]

        # Parsing and Splitting the weights into integer from string format
        weights = sys.argv[2]
        weights = weights.split(',') if checkFormat(weights) == True else None

        if weights != None:
            for i in range(0, len(weights)):
                weights[i] = int(weights[i])
        else:
            print("Weights are not comma separated!")
            
        # Parsing and Splitting the impact symbols ('+' or '-')
        impacts = sys.argv[3]
        impacts = impacts.split(',') if checkFormat(impacts) == True else None

        count = 0
        if impacts != None:
            for i in range(0, len(impacts)):
                if(impacts[i]=='+' or impacts[i]=='-'):
                    count = count+1
            if count==len(impacts):
                pass
            else:
                print("Impacts must be +ve or -ve!")
                return
        else:
            print("Impacts are not comma separated!")
            return

        # Parsing the result file name
        resultFileName = sys.argv[4]

        # Checking if the input file exists or not
        if os.path.exists(inputFileName):
            # If the length of weights and impacts is equal then calculate the 
            # performance score using topsis mathematical function
            if len(weights)==len(impacts):
                topsis(inputFileName, weights, impacts, resultFileName)
            else:
                print("Number of weights and impacts should be same!")
        else:
            print("Input file does not exist!")
    else:
        print("Wrong number of arguments provided!")
        return

# Checking the conditions applied on dataset
def conditionsOnDataset(dataset, weights, impacts):
    # Checking the number of columns in the dataset
    if len(dataset.columns)>=3:
        pass
    else:
        print("Less number of columns in input file!")
        exit()

    # The number of columns, weights and impacts should be equal
    if len(dataset.columns)-1==len(weights)==len(impacts):
        pass
    else:
        print("Number of columns, weights and impacts should be equal!")    
        exit()

    # The datatype of all the columns should be numeric
    for i in range(1, len(dataset.columns)):
        if pd.api.types.is_numeric_dtype(dataset.iloc[:,i]):
            pass
        else:
            print("Columns are not in numeric datatype!")
            exit()

def topsis(inputFileName, weights, impacts, resultFileName):

    # Reading the input csv file
    dataset = pd.read_csv(inputFileName)

    # Checking the conditions on the dataset
    conditionsOnDataset(dataset, weights, impacts)

    # Dropping and NULL values
    dataset.dropna(inplace = True)

    # Dropping categorical values and using only numerical values
    df = dataset.iloc[0:,1:].values

    # Converting the dataset into a matrix
    mat = pd.DataFrame(df)

    # Calculating root of sum of square for each column
    rootOfSumOfSquares = []
    for col in range(0, len(mat.columns)):
        sum = 0
        colValues = mat.iloc[0:,[col]].values
        for val in colValues:
            sum = sum + m.pow(val,2)
        rootOfSumOfSquares.append(m.sqrt(sum))
    
    # Dividing every matrix value with its corresponding column rootOfSumOfSquares value to get Normalized Performance Value
    k = 0
    while(k<len(mat.columns)):
        for j in range(0,len(mat)):
            mat[k][j] = mat[k][j]/rootOfSumOfSquares[k]
        k = k+1

    # Multiplying each of the matrix value with its corresponding column weight to get Weighted Normalized Decision Matrix
    k = 0
    while(k<len(mat.columns)):
        for j in range(0,len(mat)):
            mat[k][j] = mat[k][j]*weights[k]
        k = k+1

    # Finding the ideal best and worst values for each column according to the impact of that column
    idealBestValue = []
    idealWorstValue = []
    for col in range(0, len(mat.columns)):
        colValues = mat.iloc[0:,[col]].values

        if impacts[col]=='+':
            maxVal = max(colValues)
            minVal = min(colValues)
            idealBestValue.append(maxVal)
            idealWorstValue.append(minVal)

        if impacts[col]=='-':
            maxVal = max(colValues)
            minVal = min(colValues)
            idealBestValue.append(minVal)
            idealWorstValue.append(maxVal)

    # Calculating the Euclidean Distance from ideal best and ideal worst values for each row     
    SiPlus = []
    SiMinus = []
    for row in range(0, len(mat)):
        rowValues = mat.iloc[row, 0:].values
        temp1 = 0
        temp2 = 0
        for val in range(0, len(rowValues)):
            temp1 = temp1 + m.pow(rowValues[val]-idealBestValue[val],2)
            temp2 = temp2 + m.pow(rowValues[val]-idealWorstValue[val],2)
        SiPlus.append(m.sqrt(temp1))
        SiMinus.append(m.sqrt(temp2))

    # Calculating the Performance Score for each row
    Pi = []
    for row in range(0, len(mat)):
        Pi.append(SiMinus[row]/(SiMinus[row]+SiPlus[row]))

    # Assigning Rank
    Rank = []
    sortPi = sorted(Pi, reverse=True)
    for row in range(0, len(mat)):
        for i in range(0, len(sortPi)):
            if Pi[row] == sortPi[i]:
                Rank.append(i+1)

    # Appending the new columns to original matrix
    col1 = dataset.iloc[:,[0]].values
    mat.insert(0, dataset.columns[0], col1)
    mat['TOPSIS Score'] = Pi
    mat['Rank'] = Rank

    # Saving the new matrix to the final result csv file
    mat.to_csv(resultFileName)

def main():
    checkConstraints()

if __name__ == "__main__":
    main()