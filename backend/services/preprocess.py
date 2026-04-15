import numpy as np

def preprocess(data):

    ph = float(data["ph"])
    nitrogen = float(data["nitrogen"])
    phosphorus = float(data["phosphorus"])
    potassium = float(data["potassium"])
    rainfall = float(data["rainfall"])
    temperature = float(data["temperature"])

    return np.array([[ph,nitrogen,phosphorus,potassium,rainfall,temperature]])