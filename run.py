#!/usr/bin/env python

import sys
import os
import json

sys.path.insert(0, 'src')
sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/features')
sys.path.insert(0, 'src/models')

from etl import get_data
from build_features import build_features
from train_model import train
from test_model import test


def main(targets):
    '''
    Runs the main project pipeline logic, given the targets.
    targets must contain: 'data', 'analysis', 'model'. 
    
    `main` runs the targets in order of data=>analysis=>model.
    '''

#     if 'eda' in targets:
#         with open('config/eda-params.json') as fh:
#             data_cfg = json.load(fh)

#         # make the data target
#         data = main_eda(**data_cfg)
        
    if 'test-data' in targets:
        with open('config/test-data-params.json') as fh:
            test_data_cfg = json.load(fh)

        get_data(**test_data_cfg)
        
    if 'features' in targets:
        with open('config/features-params.json') as fh:
            features_cfg = json.load(fh)

        build_features(**features_cfg)
        
    if 'model' in targets:
        with open('config/model-params.json') as fh:
            model_cfg = json.load(fh)

        train(**model_cfg)
        test(**model_cfg)
        
    if 'test' in targets:
        with open('config/test-data-params.json') as fh:
            test_data_cfg = json.load(fh)
            
        get_data(**test_data_cfg)
            
        with open('config/features-params.json') as fh:
            features_cfg = json.load(fh)
            
        build_features(**features_cfg)
            
        with open('config/model-params.json') as fh:
            model_cfg = json.load(fh)
            
        train(**model_cfg)
        test(**model_cfg)



if __name__ == '__main__':
    # run via:
    # python main.py data features model
    targets = sys.argv[1:]
    main(targets)