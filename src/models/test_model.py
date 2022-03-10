import sys

sys.path.insert(0, '../')

from ..helper_functions import split_X_y, read_data, test_split
import pickle
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score

def test(data_dir, model_save_path, train_prop):
    
    test_df = test_split(read_data(data_dir), train_prop)    
    test_X, test_y = split_X_y(test_df)
    
    loaded_model = pickle.load(open(model_save_path, 'rb'))
    
    y_pred = loaded_model.predict(test_X)
    
    with open('results/model_performance.txt', 'w') as f:
        f.write('Accuracy: %d \nRecall: %d' % (accuracy_score(test_y, y_pred), 
                                                recall_score(test_y, y_pred, pos_label = 'Bad')))