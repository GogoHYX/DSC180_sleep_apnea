import sys

sys.path.insert(0, '../')

import numpy as np
import pandas as pd
import os
import json
from helper_functions import save_data


def create_features(raw_df):
    '''Takes in the raw df and outputs df ready to put into the classifier'''
    
    df = raw_df.drop(['pid', 'sawa2'], axis = 1)

    df = df.loc[df.interval != 'EXCLUD'].reset_index(drop = True)

    df['interval_num'] = df.interval.replace({'ACTIVE': 3, 'REST': 1, 'REST-S': 0}) # so the differences are unique

    df['lines'] = range(1, df.shape[0] + 1)

    epochs_in_each_interval = (df.loc[df.interval_num.diff() != 0, :] # epochs where state changed
                               .lines
                               .diff()) # number of epochs in each state, starting from active

    # interval_epochs eventually contains 1) indicies where state changes, 2) what interval starts at that epoch,  
    # 3) num of epochs in the state before it and 4) the num of epochs in that state itself
    interval_epochs = (df.iloc[epochs_in_each_interval.index,:].interval_num.to_frame()
                       .join(epochs_in_each_interval).reset_index())
    interval_epochs.columns = ['index', 'interval_num', 'num_epochs_before_interval']
    interval_epochs['num_epochs_in_interval'] = interval_epochs.num_epochs_before_interval[1:].reset_index(drop=True)

    sleep_eff = [] # will contain sleep efficiency for the different times that subject sleeps

    for i in range(len(interval_epochs)):
        if interval_epochs.iloc[i, 1] == 0:
            if interval_epochs.iloc[i-1, 1] == 1:
                sleep_eff.append(interval_epochs.iloc[i, 3]/(interval_epochs.iloc[i-1, 3]+interval_epochs.iloc[i, 3]))
            else:
                sleep_eff.append(1)
                
    # indicies where light exposure occurs before the subject sleeps (active + rest)
    awake_light_idx = []
    for i in range(interval_epochs.shape[0]):
        if interval_epochs.iloc[i, 1] == 0:
            if interval_epochs.iloc[i-1, 1] == 1:
                awake_light_idx.append(tuple((interval_epochs.iloc[i-2, 0], interval_epochs.iloc[i, 0])))
            else:
                awake_light_idx.append(tuple((interval_epochs.iloc[i-1, 0], interval_epochs.iloc[i, 0])))

                # series with series of light (this is the format that sktime dfs take)
    awake_whitelight_series = pd.Series([df.whitelight.iloc[x:y].fillna(0).iloc[-240:].reset_index(drop=True) 
                                         for x,y in awake_light_idx]) # light for last 2 hours before sleep only
    awake_bluelight_series = pd.Series([df.bluelight.iloc[x:y].fillna(0).iloc[-240:].reset_index(drop=True) 
                                        for x,y in awake_light_idx])
    awake_greenlight_series = pd.Series([df.greenlight.iloc[x:y].fillna(0).iloc[-240:].reset_index(drop=True) 
                                         for x,y in awake_light_idx])
    awake_redlight_series = pd.Series([df.redlight.iloc[x:y].fillna(0).iloc[-240:].reset_index(drop=True) 
                                       for x,y in awake_light_idx])

    # each entry in column dim_xxxx is a series of light
    final_df = pd.DataFrame({"dim_white": awake_whitelight_series.values, 
                             "dim_blue": awake_bluelight_series.values,
                             "dim_green": awake_greenlight_series.values,
                             "dim_red": awake_redlight_series.values,
                             "sleep_eff": sleep_eff})

    # threshold chosen using idea that good sleep efficiency is when one sleeps in ~24 mins
    # for a sleep of 8 hrs (ratio -- 24mins/8hrs = 3mins/1hr)
    final_df["sleep_eff_cat"] = (final_df.sleep_eff >= 0.95).replace({True: "Good", False: "Bad"})

    return final_df
    
def build_features(data_dir, outpath):
    '''Takes in directory of raw dfs, builds features, concatenates them and saves the final df in appropriate format'''
    
    concat_df = pd.DataFrame(columns = ["dim_white","dim_blue","dim_green","dim_red","sleep_eff","sleep_eff_cat"])
    
    files = os.listdir(data_dir)
    
    for f in files:
        if f.endswith(".csv"):
            proc_data = create_features(pd.read_csv(os.path.join(data_dir, f)))
            concat_df = pd.concat([concat_df, proc_data])
    concat_df = concat_df.reset_index(drop = True)
    concat_df = concat_df.loc[concat_df.dim_white.apply(lambda x: len(x)) >= 240].reset_index(drop = True)
    
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    save_data(concat_df, outpath)