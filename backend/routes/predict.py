from fastapi import APIRouter
import pickle
from services.preprocess import preprocess
from database.db import predictions

router = APIRouter()

model = pickle.load(open("models/crop_model.pkl","rb"))

@router.post("/predict")

def predict(data:dict):

    processed = preprocess(data)

    result = model.predict(processed)

    crop = result[0]

    predictions.insert_one({
        "input":data,
        "prediction":crop
    })

    return {
        "recommended_crop":crop
    }