import ee
import numpy as np
from datetime import datetime, timedelta
import joblib
import os

# Initialize Earth Engine
ee.Initialize(project='earthengine-uhi')

# Load trained AI model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "avg_temp_model.pkl")
model = joblib.load(MODEL_PATH)

def preprocess_city_data(lat, lon):
    """Fetches MODIS data + runs AI model for UHI metrics"""
    point = ee.Geometry.Point([lon, lat])

    # Get MODIS LST (Land Surface Temperature) v061
    dataset = ee.ImageCollection("MODIS/061/MOD11A2").select("LST_Day_1km") \
        .filterDate(datetime.now() - timedelta(days=30), datetime.now()) \
        .filterBounds(point) \
        .mean()

    lst = dataset.reduceRegion(
        reducer=ee.Reducer.mean(), geometry=point, scale=1000
    ).get("LST_Day_1km").getInfo()

    if lst is None:
        lst_celsius = 30.0  # fallback value
    else:
        lst_celsius = (lst * 0.02) - 273.15

    # Features: [lat, lon, lst_celsius]
    features = np.array([[lat, lon, lst_celsius]])
    predicted_temp = model.predict(features)[0]

    # Mitigation: assume +15% green cover → -3°C reduction
    mitigated_temp = predicted_temp - 3.0

    # Determine UHI level
    if predicted_temp >= 40:
        level = "High"
    elif predicted_temp >= 35:
        level = "Medium"
    else:
        level = "Low"

    return {
        "avg_temp": round(predicted_temp, 2),
        "mitigated_temp": round(mitigated_temp, 2),
        "level": level,
        "green_space_percent": 15
    }
