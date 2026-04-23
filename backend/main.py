from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import requests
import os
from datetime import datetime
import numpy as np

# ================= INIT =================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================= PATH =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# ================= LOAD DATASET =================
import pandas as pd

df = pd.read_csv(os.path.join(BASE_DIR, "datasets/crop_data.csv"))

# normalize dataset
df["soil"] = df["soil"].str.lower().str.strip()
df["location"] = df["location"].str.lower().str.strip()
df["crop"] = df["crop"].str.lower().str.strip()

# ================= LOAD MODEL =================
ml_model = None
soil_encoder = None
season_encoder = None
location_encoder = None
crop_encoder = None

try:
    ml_model = pickle.load(open(os.path.join(MODEL_DIR, "random_forest_model.pkl"), "rb"))
    soil_encoder = pickle.load(open(os.path.join(MODEL_DIR, "soil_encoder.pkl"), "rb"))
    season_encoder = pickle.load(open(os.path.join(MODEL_DIR, "season_encoder.pkl"), "rb"))
    location_encoder = pickle.load(open(os.path.join(MODEL_DIR, "location_encoder.pkl"), "rb"))
    crop_encoder = pickle.load(open(os.path.join(MODEL_DIR, "crop_encoder.pkl"), "rb"))

    print("✅ ML Model Loaded")

except Exception as e:
    print("❌ Model error:", e)

# ================= WEATHER =================
WEATHER_API = "c39f5f17162c4baf866d39cd95be2ffc"

def get_weather(location):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": f"{location},IN",
            "appid": WEATHER_API,
            "units": "metric"
        }

        res = requests.get(url, params=params, timeout=5)

        if res.status_code != 200:
            raise Exception("Invalid location")

        data = res.json()

        return {
            "temperature": round(data["main"]["temp"], 1),
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"]
        }

    except:
        return {
            "temperature": 39,
            "humidity": 20,
            "condition": "few clouds",
            "note": "fallback weather"
        }

# ================= SEASON =================
def get_season():
    m = datetime.now().month

    if m in [3,4,5]:
        return "summer"
    elif m in [6,7,8]:
        return "autumn"
    elif m in [9,10,11]:
        return "spring"
    else:
        return "winter"

# ================= EXTRA RECOMMENDATIONS =================
def get_crop_details(crop):

    data = {
        "rice": {
            "irrigation": "High (standing water)",
            "fertilizer": "Urea + DAP",
            "pesticide": "Neem oil",
            "duration": "120–150 days"
        },
        "wheat": {
            "irrigation": "Moderate",
            "fertilizer": "NPK",
            "pesticide": "Chlorpyrifos",
            "duration": "100–120 days"
        }
    }

    return data.get(crop, {
        "irrigation": "Moderate",
        "fertilizer": "General NPK",
        "pesticide": "Basic pest control",
        "duration": "Varies"
    })

# ================= HOME =================
@app.get("/")
def home():
    return {"message": "🌾 Backend running"}

# ================= RECOMMEND =================
@app.post("/recommend")
def recommend(data: dict):

    try:
        soil = data.get("soil", "").lower().strip()
        location = data.get("location", "").lower().strip()
        season = get_season()

        # 🔧 FIX COMMON TYPO
        if location == "tuticorin":
            location = "thoothukudi"

        # ================= DATASET BASED (PRIMARY) =================
        filtered = df[
            (df["soil"] == soil) &
            (df["location"] == location)
        ]

        if len(filtered) > 0:
            crop = filtered["crop"].mode()[0]

        # ================= ML FALLBACK =================
        elif ml_model is not None:

            if soil not in soil_encoder.classes_:
                return {"error": "Invalid soil"}

            if location not in location_encoder.classes_:
                return {"error": "Invalid location"}

            X = np.array([[
                soil_encoder.transform([soil])[0],
                season_encoder.transform([season])[0],
                location_encoder.transform([location])[0]
            ]])

            pred = ml_model.predict(X)[0]
            crop = crop_encoder.inverse_transform([pred])[0]

        # ================= FINAL FALLBACK =================
        else:
            crop = "rice"

        # ================= EXTRA DETAILS =================
        details = get_crop_details(crop)

        return {
            "recommendation": {
                "best_crop": crop,
                "irrigation": details["irrigation"],
                "fertilizer": details["fertilizer"],
                "pesticide": details["pesticide"],
                "duration": details["duration"]
            },
            "weather": get_weather(location)
        }

    except Exception as e:
        return {"error": str(e)}

# ================= MARKET =================
@app.get("/market/{crop}")
def market(crop: str):

    try:
        url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

        params = {
            "api-key": "579b464db66ec23bdd000001469d5e02435f46e555299b25dc6431f6",
            "format": "json",
            "limit": 100
        }

        res = requests.get(url, params=params)
        data = res.json()

        prices = []

        for i in data.get("records", []):
            if crop.lower() in i.get("commodity", "").lower():
                if i.get("modal_price"):
                    prices.append(float(i["modal_price"]))

        if not prices:
            return {"crop": crop, "price": None}

        return {
            "crop": crop,
            "price": round(sum(prices)/len(prices)/100, 2)
        }

    except:
        return {"crop": crop, "price": None}

# ================= COST =================
@app.post("/cost-predict")
def cost(data: dict):

    crop = data.get("crop", "")
    area = float(data.get("area", 1))

    total_cost = sum([
        float(data.get("seed", 0)),
        float(data.get("irrigation", 0)),
        float(data.get("fertilizer", 0)),
        float(data.get("labour", 0))
    ])

    yield_map = {
        "rice": 2500,
        "wheat": 3000,
        "tomato": 20000
    }

    y = yield_map.get(crop, 2000)
    income = y * area * 20
    profit = income - total_cost

    return {
        "income": income,
        "profit": profit
    }

# ================= HYGIENE =================
@app.post("/hygiene-check")
def hygiene(data: dict):

    answers = data.get("answers", [])
    score = answers.count("yes")

    if score == 5:
        level = "Excellent"
    elif score >= 3:
        level = "Moderate"
    else:
        level = "Poor"

    return {
        "score": score,
        "level": level
    }