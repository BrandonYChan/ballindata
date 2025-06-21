import pandas as pd, numpy as np, sklearn as sklm
import sqlalchemy 
from sklearn.linear_model import LogisticRegression, LinearRegression 
import joblib 
# import tensorflow as tf
# import keras 
# from keras.models import load_model 
import os 
from django.conf import settings 

def make_prediction(names, data, selected_model): 
    stat_string = '_'.join(names) 
    model = joblib.load(os.path.join(settings.BASE_DIR, f'ballindata/MLMODELS/allstar/{selected_model}/{stat_string}.pkl')) 
    prediction = model.predict_proba(data)[0][1]
    prediction = np.round(prediction, 4) 
    return prediction  

