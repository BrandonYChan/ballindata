import pandas as pd, numpy as np, sklearn as sklm
import sqlalchemy 
from sklearn.linear_model import LogisticRegression, LinearRegression 
import joblib 
import tensorflow as tf
import keras 
from keras.models import load_model 
import os 
from django.conf import settings 

# db_path = f"sqlite:///{os.path.join(settings.BASE_DIR, 'ballindata/DB/ballbase.db')}" 

# engine = sqlalchemy.create_engine(db_path) 
# master = pd.read_sql("master_as", con=engine) 
# numeric_df = pd.read_sql("numeric_as", con=engine)  



def make_prediction(names, data, selected_model): 
    stat_string = '_'.join(names) 
    
    if selected_model == 'neural_network':
        model = load_model(os.path.join(settings.BASE_DIR, f'ballindata/MLMODELS/allstar/nn/{stat_string}.keras')) 
        prediction = model.predict(tf.convert_to_tensor(data))[0][0].astype('float64')         
    elif selected_model == 'logistic_regression': 
        model = joblib.load(os.path.join(settings.BASE_DIR, f'ballindata/MLMODELS/allstar/lr/{stat_string}.pkl'))
        prediction = model.predict_proba(data)[0][1] 
    elif selected_model == 'random_forest': 
        model = joblib.load(os.path.join(settings.BASE_DIR, f'ballindata/MLMODELS/allstar/rf/{stat_string}.pkl')) 
        prediction = model.predict_proba(data)[0][1]
    
    prediction = np.round(prediction, 4) 
    return prediction  

