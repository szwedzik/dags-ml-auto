from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

app = FastAPI()

with open("model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

class InputData(BaseModel):
    feature1: float
    feature2: float
    feature3: float

@app.post("/predict")
def predict(data: InputData):
    input_features = np.array([[data.feature1, data.feature2, data.feature3]])
    prediction = model.predict(input_features)
    return {"prediction": prediction.tolist()}
