import sys

sys.path.insert(0, '../')

from helper_functions import split_X_y, read_data, train_split
from sktime.classification.kernel_based import RocketClassifier
import pickle
import os

def train(data_dir, model_save_path, train_prop):

    if not os.path.exists(model_save_path):
        os.makedirs(model_save_path)
    
    train_df = train_split(read_data(data_dir), train_prop)
    train_X, train_y = split_X_y(train_df)
    
    rocket_red = RocketClassifier()
    rocket_red.fit(train_X.dim_red.to_frame(), train_y)
    pickle.dump(rocket_red, open(model_save_path + 'red_light_model.pkl', 'wb'))

    rocket_green = RocketClassifier()
    rocket_green.fit(train_X.dim_green.to_frame(), train_y)
    pickle.dump(rocket_green, open(model_save_path + 'green_light_model.pkl', 'wb'))

    rocket_blue = RocketClassifier()
    rocket_blue.fit(train_X.dim_blue.to_frame(), train_y)
    pickle.dump(rocket_blue, open(model_save_path + 'blue_light_model.pkl', 'wb'))

    rocket_white = RocketClassifier()
    rocket_white.fit(train_X.dim_white.to_frame(), train_y)
    pickle.dump(rocket_white, open(model_save_path + 'white_light_model.pkl', 'wb'))