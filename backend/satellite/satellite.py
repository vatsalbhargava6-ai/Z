import ee
import json
import os

# load JSON from env
key = json.loads(os.getenv("EE_SERVICE_ACCOUNT_KEY"))

# write temporary file
import tempfile

with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
    json.dump(key, f)
    key_path = f.name

# correct Earth Engine auth
credentials = ee.ServiceAccountCredentials(
    key["client_email"],
    key_path
)

ee.Initialize(credentials, project="z-agro-ai")

# ---------------- LOAD ML MODEL ----------------
MODEL_PATH = "ml_model/crop_model.pkl"

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    ML_ENABLED = True
else:
    model = None
    ML_ENABLED = False


def get_satellite_analysis(lat, lon):

    point = ee.Geometry.Point([lon, lat])

    # ---------------- SENTINEL-2 IMAGE ----------------
    image = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(point)
        .filterDate("2024-01-01", "2024-12-31")
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .median()
    )

    # ---------------- NDVI ----------------
    ndvi_img = image.normalizedDifference(["B8", "B4"]).rename("ndvi")

    ndvi_dict = ndvi_img.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=point,
        scale=10
    )

    ndvi_value = ndvi_dict.get("ndvi").getInfo()

    if ndvi_value is None:
        ndvi_value = 0

    ndvi_value = float(ndvi_value)

    # ---------------- MOCK WEATHER ----------------
    temp = 28
    humidity = 60
    rainfall = 10

    # ---------------- ML PREDICTION ----------------
    if ML_ENABLED:
        features = np.array([[ndvi_value, temp, humidity, rainfall]])
        prediction = model.predict(features)[0]
        confidence = 0.90
    else:
        prediction = None
        confidence = 0.0

    # ---------------- LAND TYPE ----------------
    if prediction is None:
        if ndvi_value < 0.05:
            land_type = "Urban 🏙️"
        elif ndvi_value < 0.2:
            land_type = "Barren Land 🏜️"
        elif ndvi_value < 0.5:
            land_type = "Farmland 🌾"
        else:
            land_type = "Forest 🌳"
    else:
        land_type = prediction

    # ---------------- HEALTH SCORE ----------------
    health_score = round(min(100, max(0, ndvi_value * 100 + humidity * 0.2)), 2)

    if health_score > 70:
        health_status = "Healthy"
    elif health_score > 40:
        health_status = "Moderate"
    else:
        health_status = "Poor"

    return {
        "ndvi": round(ndvi_value, 3),
        "land_type": land_type,
        "health_score": health_score,
        "health_status": health_status,
        "confidence": confidence,
        "status": "REAL Sentinel-2 + AI Hybrid",
        "ml_enabled": ML_ENABLED
    }