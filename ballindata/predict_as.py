import pandas as pd, numpy as np, sklearn as sklm
import tensorflow as tf, sqlalchemy 
from sklearn.linear_model import LogisticRegression, LinearRegression 
import joblib 
from keras.models import load_model 


db_path = 'sqlite:///C:\\Users\\bchan\\OneDrive\\Personal Projects\\BID_Django\\ballindata\\DB\\ballbase.db' 
engine = sqlalchemy.create_engine(db_path) 
master = pd.read_sql("master_as", con=engine) 
numeric_df = pd.read_sql("numeric_as", con=engine)  
rf = joblib.load("C:\\Users\\bchan\OneDrive\Personal Projects\BID_Django\\ballindata\IPYNB\Analyses\\rf_model.pkl") 
lr = joblib.load("C:\\Users\\bchan\OneDrive\Personal Projects\BID_Django\\ballindata\IPYNB\Analyses\lr_model.pkl") 

nn = load_model("C:\\Users\\bchan\OneDrive\Personal Projects\BID_Django\\ballindata\IPYNB\Analyses\seq_model.keras") 

def make_prediction(data, selected_model):
    if selected_model == 'logistic_regression': 
        prediction = lr.predict(data)[0] 
    elif selected_model == 'random_forest': 
        prediction = rf.predict(data)[0] 
    else: 
        prediction = nn.predict(tf.convert_to_tensor(data))[0][0].astype('float64') 
    
    
    # if isinstance(prediction, np.ndarray):
    #             prediction = prediction.tolist()
    
    return prediction   # Return the first prediction (assuming single input)

def get_stat_names(): 
    cols = numeric_df.drop('AS', axis=1).columns.tolist() 
    return cols 

def get_avg(stat_name): 
    return np.mean(master[stat_name].dropna(axis=0)) 