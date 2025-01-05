import pandas as pd, numpy as np, sklearn as sklm
import tensorflow as tf, sqlalchemy 
from sklearn.linear_model import LogisticRegression, LinearRegression 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.model_selection import train_test_split 
import joblib 
pd.set_option('display.max_columns', None)
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname('functions.py'), '..', '..', 'PY')))
import functions 
from keras.models import load_model 

# Neural Network 

engine = sqlalchemy.create_engine("sqlite:///../DB/ballbase.db") 
df = pd.read_sql("master_as", con=engine) 

nn_path = "../../MLModels/as_nn_tool.keras"

if(not(os.path.exists(nn_path))): 
    numeric_tensor = tf.convert_to_tensor(numeric_df) 
    normalizer = tf.keras.layers.Normalization(axis=-1) 
    normalizer.adapt(numeric_tensor) 

    seq_model = tf.keras.models.Sequential() 
    # seq_model.add(normalizer) 
    seq_model.add(tf.keras.layers.Dense(units=10, activation='relu', input_shape=(5, ))) 
    seq_model.add(tf.keras.layers.Dense(units=10, activation='relu')) 
    seq_model.add(tf.keras.layers.Dense(units=1, activation='sigmoid')) 

    seq_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy']) 

    seq_model.fit(x=X_train, y=y_train, epochs=10, batch_size=1) 
    seq_model.save(nn_path) 
else:
    seq_model = tf.keras.models.load_model(nn_path)
    
# Logistic Regression 

lr_path = "../../MLModels/as_lr_tool.pkl"

if(os.path.exists(lr_path)):
    lr_as = joblib.load(lr_path) 
else:
    lr_as = LogisticRegression() 
    lr_as.fit(X=numeric_select, y=numeric_df['AS']) 
    joblib.dump(lr_as, lr_path) 

lr_as = LogisticRegression() 
lr_as.fit(X=numeric_select, y=numeric_df['AS']) 
joblib.dump(lr_as, lr_path) 

# Random Forest 

rf_path = "../../MLModels/as_rf_tool.pkl"

if(os.path.exists(rf_path)): 
    rf_as = joblib.load(rf_path) 
else: 
    rf_as = sklm.ensemble.RandomForestClassifier()  
    rf_as.fit(X=numeric_select, y=numeric_df['AS'])
    joblib.dump(rf_as, rf_path)

rf_as = sklm.ensemble.RandomForestClassifier()  
rf_as.fit(X=numeric_select, y=numeric_df['AS'])
joblib.dump(rf_as, rf_path)