import sys

sys.path.insert(0, '../')

from ..helper_functions import split_X_y, read_data, train_split
from sktime.classification.kernel_based import RocketClassifier
import pickle

def train(data_dir, model_save_path, train_prop):
    
    train_df = train_split(read_data(data_dir), train_prop)
    train_X, train_y = split_X_y(train_df)
    
    rocket = RocketClassifier()
    rocket.fit(train_X, train_y)
    pickle.dump(rocket, open(model_save_path, 'wb'))