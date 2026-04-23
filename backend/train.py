import pandas as pd
import pickle
import os
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ================= PATH SETUP =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "datasets", "crop_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)

# ================= LOAD DATA =================
df = pd.read_csv(DATA_PATH)

# ================= CLEAN COLUMNS =================
df.columns = df.columns.str.strip().str.lower()

required_cols = ["soil", "season", "location", "crop"]

if not set(required_cols).issubset(df.columns):
    print("❌ Missing required columns")
    print("Found:", df.columns)
    exit()

# ================= CLEAN DATA =================
df = df.dropna()

for col in required_cols:
    df[col] = df[col].astype(str).str.strip().str.lower()

# ❌ DON'T FILTER SEASON HARD (REMOVED BUG FIX)
# df = df[df["season"].isin([...])]  ❌ REMOVE THIS

df = df.drop_duplicates()

print("Rows after cleaning:", len(df))

# ================= ENCODING =================
soil_encoder = LabelEncoder()
season_encoder = LabelEncoder()
location_encoder = LabelEncoder()
crop_encoder = LabelEncoder()

df["soil"] = soil_encoder.fit_transform(df["soil"])
df["season"] = season_encoder.fit_transform(df["season"])
df["location"] = location_encoder.fit_transform(df["location"])
df["crop"] = crop_encoder.fit_transform(df["crop"])

# ================= FEATURES =================
X = df[["soil", "season", "location"]]
y = df["crop"]

# ================= TRAIN TEST SPLIT =================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ================= MODEL =================
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    random_state=42
)

model.fit(X_train, y_train)

# ================= EVALUATION =================
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"🎯 Model Accuracy: {accuracy * 100:.2f}%")

# ================= SAVE =================
pickle.dump(model, open(os.path.join(MODEL_DIR, "random_forest_model.pkl"), "wb"))
pickle.dump(soil_encoder, open(os.path.join(MODEL_DIR, "soil_encoder.pkl"), "wb"))
pickle.dump(season_encoder, open(os.path.join(MODEL_DIR, "season_encoder.pkl"), "wb"))
pickle.dump(location_encoder, open(os.path.join(MODEL_DIR, "location_encoder.pkl"), "wb"))
pickle.dump(crop_encoder, open(os.path.join(MODEL_DIR, "crop_encoder.pkl"), "wb"))

print("✅ Model & encoders saved successfully")

# ================= SAFE SAMPLE TEST =================
print("\n🔍 SAMPLE PREDICTION TEST")

sample = np.array([[df["soil"].iloc[0],
                    df["season"].iloc[0],
                    df["location"].iloc[0]]])

pred = model.predict(sample)
crop = crop_encoder.inverse_transform(pred)[0]

print("🌾 Sample Prediction:", crop)