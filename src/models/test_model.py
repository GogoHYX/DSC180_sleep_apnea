import sys

sys.path.insert(0, '../')

from helper_functions import split_X_y, read_data, test_split, vote
import pickle
import pandas as pd
from sklearn.metrics import recall_score

def test(data_dir, model_save_path, train_prop):
    
    test_df = test_split(read_data(data_dir), train_prop)    
    test_X, test_y = split_X_y(test_df)
    
    red_loaded_model = pickle.load(open(model_save_path + 'red_light_model.pkl', 'rb'))
    green_loaded_model = pickle.load(open(model_save_path + 'green_light_model.pkl', 'rb'))
    blue_loaded_model = pickle.load(open(model_save_path + 'blue_light_model.pkl', 'rb'))
    white_loaded_model = pickle.load(open(model_save_path + 'white_light_model.pkl', 'rb'))
    
    red_preds = red_loaded_model.predict(test_X.dim_red.to_frame())
    green_preds = green_loaded_model.predict(test_X.dim_green.to_frame())
    blue_preds = blue_loaded_model.predict(test_X.dim_blue.to_frame())
    white_preds = white_loaded_model.predict(test_X.dim_white.to_frame())

    preds_df = pd.DataFrame({'red_pred': red_preds, 
                            'blue_pred': green_preds, 
                            'green_pred': blue_preds, 
                            'white_pred': white_preds})

    model_preds = preds_df.apply(lambda row: vote(list(row)), axis = 1)

    model_preds.to_csv(model_save_path + 'model_predictions.csv', index = False)
    
    with open(model_save_path + 'model_recall.txt', 'w') as f:
        f.write('Bad Sleep Quality Recall: %d \nGood Sleep Quality Recall: %d' % (recall_score(test_y, model_preds, pos_label = 'Bad'), 
                                                                                  recall_score(test_y, model_preds, pos_label = 'Good')))