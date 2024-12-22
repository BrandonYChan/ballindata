import pandas as pd, numpy as np, sklearn as sklm
import sqlalchemy 
from sklearn.linear_model import LogisticRegression, LinearRegression 
import joblib 
# import tensorflow as tf
from keras.models import load_model 
import os 
from django.conf import settings 

db_path = f"sqlite:///{os.path.join(settings.BASE_DIR, 'ballindata/DB/ballbase.db')}" 

engine = sqlalchemy.create_engine(db_path) 
master = pd.read_sql("master_as", con=engine) 
numeric_df = pd.read_sql("numeric_as", con=engine)  

def make_prediction(data, selected_model): 
    if selected_model == 'logistic_regression': 
        lr = joblib.load(os.path.join(settings.BASE_DIR, 'ballindata/MLMODELS/lr_model.pkl')) 
        prediction = lr.predict(data)[0] 
    elif selected_model == 'random_forest': 
        rf = joblib.load(os.path.join(settings.BASE_DIR, 'ballindata/MLMODELS/rf_model.pkl')) 
        prediction = rf.predict(data)[0] 
    # elif selected_model == 'neural_network':
    #     nn = load_model(os.path.join(settings.BASE_DIR, 'ballindata/MLMODELS/seq_model.keras'))  
    #     prediction = nn.predict(tf.convert_to_tensor(data))[0][0].astype('float64') 
    elif selected_model == 'neural_network_simple':
        nn_simple = load_model(os.path.join(settings.BASE_DIR, 'ballindata/MLMODELS/as_nn_tool.keras')) 
        prediction = round(nn_simple.predict(tf.convert_to_tensor(data))[0][0].astype('float64'), 4)  
    elif selected_model == 'logistic_regression_simple': 
        model = joblib.load(os.path.join(settings.BASE_DIR, 'ballindata/MLMODELS/as_lr_tool.pkl'))
        prediction = round(model.predict_proba(data)[0][1], 4) 
    elif selected_model == 'random_forest_simple': 
        model = joblib.load(os.path.join(settings.BASE_DIR, 'ballindata/MLMODELS/as_rf_tool.pkl')) 
        prediction = round(model.predict_proba(data)[0][1], 4) 
    
    
    if isinstance(prediction, np.ndarray):
        prediction = prediction.tolist()
    
    return prediction  

def get_stat_names(): 
    cols = numeric_df.drop('AS', axis=1).columns.tolist() 
    return cols 

def get_avg(stat_name): 
    return np.mean(master[stat_name].dropna(axis=0)) 