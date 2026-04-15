from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import requests

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML model
model = pickle.load(open("models/crop_model.pkl","rb"))
soil_encoder = pickle.load(open("models/soil_encoder.pkl","rb"))
season_encoder = pickle.load(open("models/season_encoder.pkl","rb"))
crop_encoder = pickle.load(open("models/crop_encoder.pkl","rb"))
# -----------------------------
# Crop Prediction API
# -----------------------------
@app.post("/predict")
def predict(data: dict):

    soil = data["soil"]
    season = data["season"]

    soil_encoded = soil_encoder.transform([soil])[0]
    season_encoded = season_encoder.transform([season])[0]

    prediction = model.predict([[soil_encoded, season_encoded]])

    crop_name = crop_encoder.inverse_transform(prediction)[0]

    return {
        "recommended_crop": crop_name
    }

# -----------------------------
# Weather API
# -----------------------------
API_KEY = "c39f5f17162c4baf866d39cd95be2ffc"

@app.get("/weather/{city}")
def weather(city:str):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if "main" not in data:
        return {"error":"City not found or API error"}

    return {
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"]
    }