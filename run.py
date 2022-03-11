#!/usr/bin/env python

import sys
import os
import json
import shutil

sys.path.insert(0, 'src')
sys.path.insert(0, 'src/features')
sys.path.insert(0, 'src/models')

from build_features import build_features
from train_model import train
from test_model import test
import rnn_model


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
        
    # if 'test-data' in targets:
    #     with open('config/test-data-params.json') as fh:
    #         test_data_cfg = json.load(fh)

    #     get_data(**test_data_cfg)
        
    if 'features' in targets:
        with open('config/features-params.json') as fh:
            features_cfg = json.load(fh)

        build_features(**features_cfg)
        
    if 'model' in targets:
        with open('config/model-params.json') as fh:
            model_cfg = json.load(fh)

        train(**model_cfg)

    if 'predict' in targets:
        with open('config/model-params.json') as fh:
            model_cfg = json.load(fh)

        test(**model_cfg)
    
    if 'test_rnn' in targets:
        with open('config/test-rnn-params.json') as fh:
            test_rnn_cfg = json.load(fh)

        rnn_model.test_rnn(test_rnn_cfg)
        
    if 'test' in targets:
        # with open('config/test-data-params.json') as fh:
        #     test_data_cfg = json.load(fh)
            
        # get_data(**test_data_cfg)
            
        with open('config/test-features-params.json') as fh:
            features_cfg = json.load(fh)
            
        build_features(**features_cfg)
            
        with open('config/test-model-params.json') as fh:
            model_cfg = json.load(fh)
            
        train(**model_cfg)
        test(**model_cfg)
        
        with open('config/test-rnn-params.json') as fh:
            test_rnn_cfg = json.load(fh)

        rnn_model.test_rnn(test_rnn_cfg)


    if 'clean' in targets:
        if os.path.exists('data'):
            shutil.rmtree('data')

        if os.path.exists('results/test'):
            shutil.rmtree('results/test')



if __name__ == '__main__':
    # run via:
    # python main.py data features model
    targets = sys.argv[1:]
    main(targets)