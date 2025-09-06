import ee
import numpy as np
from datetime import datetime, timedelta
import joblib
import os
import logging

# Initialize Earth Engine
ee.Initialize(project='earthengine-uhi')

# Load trained AI model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "avg_temp_model.pkl")
model = joblib.load(MODEL_PATH)

def preprocess_city_data(lat, lon, dt=None):
    """
    Fetch MODIS LST data + run AI model for UHI metrics.
    Handles missing keys safely and logs raw results.
    """

    try:
        point = ee.Geometry.Point([lon, lat])

        # Use provided datetime or current UTC
        if dt is None:
            dt = datetime.utcnow()

        # Use a wider date window to increase chance of valid data
        start_date = dt - timedelta(days=90)
        end_date = dt

        # Get MODIS LST dataset
        dataset = ee.ImageCollection("MODIS/061/MOD11A2") \
            .select("LST_Day_1km") \
            .filterDate(start_date, end_date) \
            .filterBounds(point) \
            .mean()

        # Reduce region safely
        lst_dict = dataset.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=1000
        ).getInfo()

        logging.info(f"LST raw dictionary for ({lat}, {lon}): {lst_dict}")

        # Extract value safely
        lst = None
        if lst_dict and isinstance(lst_dict, dict):
            if "LST_Day_1km" in lst_dict:
                lst = lst_dict["LST_Day_1km"]

        if lst is None:
            logging.warning(f"No LST data for ({lat}, {lon}) at {dt}. Using fallback 30°C.")
            lst_celsius = 30.0  # fallback
        else:
            lst_celsius = (lst * 0.02) - 273.15  # MODIS scale factor & Kelvin to °C

        # Features for AI model: [lat, lon, lst_celsius]
        features = np.array([[lat, lon, lst_celsius]])
        predicted_temp = model.predict(features)[0]

        # Mitigation assumption: +15% green cover → -3°C reduction
        mitigated_temp = predicted_temp - 3.0

        # Determine UHI severity
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

    except Exception as e:
        logging.error(f"Error in preprocess_city_data: {e}")
        # Return fallback values if EE fails completely
        return {
            "avg_temp": 30.0,
            "mitigated_temp": 27.0,
            "level": "Low",
            "green_space_percent": 15
        }
