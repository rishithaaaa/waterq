import uvicorn
import gunicorn
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pickle
import pandas as pd
app=FastAPI()
pickle_in1=open('clsxgb.pkl','rb')
classifier1=pickle.load(pickle_in1)

pickle_in2=open('clsrf.pkl','rb')
classifier2=pickle.load(pickle_in2)

pickle_in3=open('clslr.pkl','rb')
classifier3=pickle.load(pickle_in3)

def predicts(df,num):
    if num==1:
        return classifier1.predict(df)
    if num==2:    
        return classifier2.predict(df)
    if num==3:
       return classifier3.predict(df)  
    

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
# def get_model(model: int):
#     return model
def predict_water(data:Water,model:int):
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
    # prediction=classifier.predict(df)
    prediction=predicts(df,model)
    if(prediction[0]>0.5):
        prediction="Safe to drink"
    else:
        prediction="Unsafe to drink"
    return{
        'prediction':prediction
    }
    # if _name=='main_':
    #     uvicorn.run(app,host='126.0.0.1',port=8000)
#uvicorn app:app --reload

