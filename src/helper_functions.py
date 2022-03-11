import os
import json
import pandas as pd
import numpy as np
from collections import Counter

def split_X_y(df):
    '''Split X features and y outcome.'''
    return (df.iloc[:, :4], df.iloc[:, 5])

def save_data(df, outpath):
    '''Saves df with each "dim" column as a separate json and
    sleep eff columns as separate csv files'''
    df_dict = dict(df)
    for k, v in df_dict.items():
        if k.startswith("dim"): # dim cols are saved as .json
            with open(os.path.join(os.getcwd(), outpath, k+".json"), 'w+') as outfile:
                      json.dump(v.to_json(), outfile)
        else: # sleep eff columns are saved as csv
            v.to_csv(os.path.join(outpath, k+".csv"), index = False)
            
def read_data(in_path):
    '''Reads the separate json/csv files into one df'''
    
    all_files = os.listdir(in_path)
    
    df = pd.DataFrame()
    
    c = 0
    for f in all_files:
        if f.endswith('.json'):
            with open(os.path.join(in_path, f)) as fh:
                col = json.load(fh)
            df.insert(c, f.split('.')[0], 
                      [pd.Series(i) for i in pd.read_json(col, typ='series', orient='records')],
                      True)
            c += 1
        elif f.endswith('.csv'):
            df.insert(c, f.split('.')[0],
                      list(pd.read_csv(os.path.join(in_path, f)).iloc[:, 0]),
                      True)
            c += 1
            
    return df

def vote(lst):
    '''Returns the result of voting'''

    data = Counter(lst[::-1])
    return max(lst[::-1], key=data.get)

def train_split(df, train_prop):
    '''Returns train split based on train_prop''' 
    
    train_rows = int(np.round(df.shape[0] * train_prop))
    
    train_df = df.iloc[:train_rows, :]
#     test_df = df.iloc[train_rows:, :]
    
    return train_df
    
def test_split(df, train_prop):
    '''Returns test split based on train_prop''' 
    
    train_rows = int(np.round(df.shape[0] * train_prop))
    
#     train_df = df.iloc[:train_rows, :]
    test_df = df.iloc[train_rows:, :]
    
    return test_df