import numpy as np
import pandas as pd
import sys
import scipy.stats as ss
from detect_delimiter import detect


def topsis_102003478():
    in_data = sys.argv
    
    try:
        in_file = in_data[1]
        weights = in_data[2]
        impacts = in_data[3]
        out_file = in_data[4]
    
    except IndexError:
        print('Incomplete number of input paramters.')
    
    try:
        data_frame = pd.read_csv(in_file)
    except FileNotFoundError:
        print('File not found on provided path.')
    
    if data_frame.shape[1]<3:
        print('Input file with less than 3 columns. Try Again!')
        exit()
        
    no_of_cols_except1 = data_frame.iloc[:,1:].shape[1]
    num_cols = data_frame.select_dtypes(include='number').shape[1]
    if num_cols < no_of_cols_except1:
        print('Columns from 2nd to last do not have numeric values.')
        exit()
        
    if(detect(impacts)!=',' or detect(weights)!=','):
        print('Use \',\' as your delimiter.')
    
    weights = list(map(float, weights.split(',')))
    impacts = impacts.split(',')
    
    if num_cols!=len(weights) or num_cols!=len(impacts):
        print('Please make sure that number of weights and impacts is equal to number of feature columns')
    
    if any(element not in ['+','-'] for element in impacts):
        print('Weights should be either \'+\' or \'-\'')
    
    num_Sehaj = data_frame.iloc[:,1:].to_numpy()
    
    num_Sehaj = num_Sehaj / np.sqrt(np.sum(np.square(num_Sehaj), axis=0))
    
    num_Sehaj = np.multiply(num_Sehaj, np.array(weights))
    
    finest_ideal = list()
    for i in range(len(impacts)):
        if impacts[i]=='+':
            finest_ideal.append(max(num_Sehaj[:,i]))
        else:
            finest_ideal.append(min(num_Sehaj[:,i]))
    
    worst_ideal = list()
    for i in range(len(impacts)):
        if impacts[i]=='+':
            worst_ideal.append(min(num_Sehaj[:,i]))
        else:
            worst_ideal.append(max(num_Sehaj[:,i]))
            
    euclidean_finest_ideal = list()
    for i in range(data_frame.shape[0]):
        euclidean_finest_ideal.append(np.sqrt(np.sum(np.square(num_Sehaj[i,:]-finest_ideal))))
        
    euclidean_worst_ideal = list()
    for i in range(data_frame.shape[0]):
        euclidean_worst_ideal.append(np.sqrt(np.sum(np.square(num_Sehaj[i,:]-worst_ideal))))
        
    p_score = np.array(euclidean_worst_ideal) / (np.array(euclidean_finest_ideal) + np.array(euclidean_worst_ideal))
    
    data_frame['Topsis Score'] = p_score
    rank = len(p_score) - ss.rankdata(p_score).astype(int) + 1
    data_frame['Rank'] = rank
    
    data_frame.to_csv(out_file, index=False)
    
    return 

topsis_calc()

