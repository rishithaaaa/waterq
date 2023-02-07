import uvicorn
import gunicorn
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pickle
import pandas as pd
app=FastAPI()
pickle_in=open('clsxgb.pkl','rb')
classifier=pickle.load(pickle_in)

class Water(BaseModel):
    ph:float
    Hardness:float
    Solids:float
    Chloramines:float
    Sulfate:float
    Conductivity:float
    Organic_carbon:float
    Trihalomethanes:float
    Turbidity:float

@app.get('/')
def index():
    return{'message': 'Welcome to water quality prediction API'}
@app.get('/name')
def get_name(name:str):
    return{'message':f'Hello,{name}'}    
@app.post('/predict')
def predict_water(data:Water):
    data=data.dict()
    print(data)
    ph=data['ph']
    Hardness=data['Hardness']
    Solids=data['Solids']
    Chloramines=data['Chloramines']
    Sulfate=data['Sulfate']
    Conductivity=data['Sulfate']
    Organic_carbon=data['Organic_carbon']
    Trihalomethanes=data['Trihalomethanes']
    Turbidity=data['Turbidity']
    values = [[ph,Hardness,Solids,Chloramines,Sulfate,Conductivity,Organic_carbon,Trihalomethanes,Turbidity]]
    df = pd.DataFrame(values, columns=["ph","Hardness","Solids","Chloramines","Sulfate","Conductivity","Organic_carbon","Trihalomethanes","Turbidity"])
    prediction=classifier.predict(df)
    if(prediction[0]>0.5):
        prediction="Good water"
    else:
        prediction="Bad water"
    return{
        'prediction':prediction
    }
    # if _name=='main_':
    #     uvicorn.run(app,host='126.0.0.1',port=8000)
#uvicorn app:app --reload
