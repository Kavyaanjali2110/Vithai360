import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# Load dataset
data = pd.read_csv("crop_data.csv")

# Encoders
soil_encoder = LabelEncoder()
season_encoder = LabelEncoder()
crop_encoder = LabelEncoder()

data["soil"] = soil_encoder.fit_transform(data["soil"])
data["season"] = season_encoder.fit_transform(data["season"])
data["crop"] = crop_encoder.fit_transform(data["crop"])

# Features and target
X = data[["soil","season"]]
y = data["crop"]

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X,y)

# Save model and encoders
pickle.dump(model, open("models/crop_model.pkl","wb"))
pickle.dump(soil_encoder, open("models/soil_encoder.pkl","wb"))
pickle.dump(season_encoder, open("models/season_encoder.pkl","wb"))
pickle.dump(crop_encoder, open("models/crop_encoder.pkl","wb"))

print("Model trained successfully")