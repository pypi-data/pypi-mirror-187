import numpy as np
import pandas as pd
import sys
import scipy.stats as ss
from detect_delimiter import detect


def topsis_calc():
    inp_arg = sys.argv
    
    try:
        input_file = inp_arg[1]
        weights = inp_arg[2]
        impacts = inp_arg[3]
        result_file = inp_arg[4]
    
    except IndexError:
        print('Number of input paramters provided are incomplete.')
    
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print('File does not exist on this path')
    
    if df.shape[1]<3:
        print('Input file have less than 3 columns. Try Again')
        exit()
        
    numberOfColafter1 = df.iloc[:,1:].shape[1]
    numeric_col = df.select_dtypes(include='number').shape[1]
    if numeric_col < numberOfColafter1:
        print('Starting from 2nd to the last columns do not have numeric values')
        exit()
        
    if(detect(impacts)!=',' or detect(weights)!=','):
        print('Use \',\' as your delimiter')
    
    weights = list(map(float, weights.split(',')))
    impacts = impacts.split(',')
    
    if numeric_col!=len(weights) or numeric_col!=len(impacts):
        print('Please make sure that number of weights and impacts is equal to number of feature columns')
    
    if any(element not in ['+','-'] for element in impacts):
        print('Weights should be either \'+\' or \'-\'')
    
    num = df.iloc[:,1:].to_numpy()
    
    num = num / np.sqrt(np.sum(np.square(num), axis=0))
    
    num = np.multiply(num, np.array(weights))
    
    id_best = list()
    for i in range(len(impacts)):
        if impacts[i]=='+':
            id_best.append(max(num[:,i]))
        else:
            id_best.append(min(num[:,i]))
    
    worst_ideal = list()
    for i in range(len(impacts)):
        if impacts[i]=='+':
            worst_ideal.append(min(num[:,i]))
        else:
            worst_ideal.append(max(num[:,i]))
            
    euclidean_best = list()
    for i in range(df.shape[0]):
        euclidean_best.append(np.sqrt(np.sum(np.square(num[i,:]-id_best))))
        
    euclidean_worst_ideal = list()
    for i in range(df.shape[0]):
        euclidean_worst_ideal.append(np.sqrt(np.sum(np.square(num[i,:]-worst_ideal))))
        
    p_score = np.array(euclidean_worst_ideal) / (np.array(euclidean_best) + np.array(euclidean_worst_ideal))
    
    df['Topsis Score'] = p_score
    rank = len(p_score) - ss.rankdata(p_score).astype(int) + 1
    df['Rank'] = rank
    
    df.to_csv(result_file, index=False)
    
    return 

topsis_calc()

