import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# ---------------- SAMPLE TRAINING DATA ----------------
# [NDVI, temperature, humidity, rainfall]

X = [
    [0.2, 30, 40, 0],   # urban/barren
    [0.6, 28, 60, 10],  # wheat
    [0.75, 27, 70, 20], # forest
    [0.55, 29, 65, 15], # soybean
    [0.3, 35, 30, 0],   # dry land
    [0.8, 26, 80, 25],  # dense forest
]

y = [
    "Urban",
    "Wheat",
    "Forest",
    "Soybean",
    "Barren",
    "Forest"
]

# ---------------- TRAIN MODEL ----------------
model = RandomForestClassifier(n_estimators=50)
model.fit(X, y)

# ---------------- SAVE MODEL ----------------
joblib.dump(model, "crop_model.pkl")

print("Model trained & saved!")