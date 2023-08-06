from detect_delimiter import detect
import scipy.stats as ss
import pandas as pd
import numpy as np
import sys


def topsis_102003483():
    topsis_args = sys.argv
    
    try:
        input_csv_file = topsis_args[1]
        weight = topsis_args[2]
        impact = topsis_args[3]
        output_csv_file = topsis_args[4]
    
    except IndexError:
        print('Input all the required parameters')
    
    try:
        df_topsis = pd.read_csv(input_csv_file)
    except FileNotFoundError:
        print('Incorrect File Path. Check again')
    
    if df_topsis.shape[1]<3:
        print('Input File should contain at least 3 Columns')
        exit()
        
    num_col_post1 = df_topsis.iloc[:,1:].shape[1]
    num_col_numeric = df_topsis.select_dtypes(include='number').shape[1]
    if num_col_numeric < num_col_post1:
        print('All the columns except first should contain only numeric values')
        exit()
        
    if(detect(impact)!=',' or detect(weight)!=','):
        print('Use \',\' as your delimiter')
    
    weight = list(map(float, weight.split(',')))
    impact = impact.split(',')
    
    if num_col_numeric!=len(weight) or num_col_numeric!=len(impact):
        print('Number of Weights and Impacts should be equal to number of input features')
    
    if any(element not in ['+','-'] for element in impact):
        print('Weights can only be \'+\' or \'-\'')
    
    #Pandas Dataframe to Numpy Matrix
    mat = df_topsis.iloc[:,1:].to_numpy()
    
    #Divide every feature value by its root of sum of squares
    mat = mat / np.sqrt(np.sum(np.square(mat), axis=0))
    
    #Calculate Weight * Normalized Performance Value
    mat = np.multiply(mat, np.array(weight))
    
    #Ideal Best
    best_ideal = list()
    for i in range(len(impact)):
        if impact[i]=='+':
            best_ideal.append(max(mat[:,i]))
        else:
            best_ideal.append(min(mat[:,i]))
    
    #Ideal Worst
    worst_ideal = list()
    for i in range(len(impact)):
        if impact[i]=='+':
            worst_ideal.append(min(mat[:,i]))
        else:
            worst_ideal.append(max(mat[:,i]))
            
    #Euclidean Distance between all points from Ideal Best and Ideal Worst row-wise
    best_ideal_euclidean = list()
    for i in range(df_topsis.shape[0]):
        best_ideal_euclidean.append(np.sqrt(np.sum(np.square(mat[i,:]-best_ideal))))
        
    worst_ideal_euclidean = list()
    for i in range(df_topsis.shape[0]):
        worst_ideal_euclidean.append(np.sqrt(np.sum(np.square(mat[i,:]-worst_ideal))))
        
    #Performance Score
    performance = np.array(worst_ideal_euclidean) / (np.array(best_ideal_euclidean) + np.array(worst_ideal_euclidean))
    
    #Topsis Rank
    df_topsis['Topsis Score'] = performance
    rank = len(performance) - ss.rankdata(performance).astype(int) + 1
    df_topsis['Rank'] = rank
    
    df_topsis.to_csv(output_csv_file, index=False)
    
    return 
    
topsis_102003483()
