import ee
import requests
import numpy as np
import os
import json
import joblib
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

# -----------------------------
# Initialize Google Earth Engine
# -----------------------------
try:
    ee.Initialize(project='earthengine-uhi')
except Exception as e:
    ee.Authenticate(project='earthengine-uhi')
    ee.Initialize(project='earthengine-uhi')

# -----------------------------
# OpenWeatherMap API
# -----------------------------
API_KEY = "220ed8731749a0aac8cb99828f4776b6"

# -----------------------------
# Load 50 Indian Cities
# -----------------------------
CITIES_FILE = os.path.join("app", "data", "indian_cities.json")

if os.path.exists(CITIES_FILE):
    with open(CITIES_FILE, "r", encoding="utf-8") as f:
        cities = json.load(f)
else:
    raise FileNotFoundError(f"{CITIES_FILE} not found! Please ensure your cities JSON exists.")

# -----------------------------
# Fetch Satellite LST
# -----------------------------
def get_satellite_lst(lat, lon):
    """Fetch MODIS LST for last 30 days"""
    point = ee.Geometry.Point([lon, lat])
    dataset = (
        ee.ImageCollection("MODIS/061/MOD11A2")
        .select("LST_Day_1km")
        .filterDate(datetime.now() - timedelta(days=30), datetime.now())
        .filterBounds(point)
        .mean()
    )

    lst = dataset.reduceRegion(
        reducer=ee.Reducer.mean(), geometry=point, scale=1000
    ).get("LST_Day_1km").getInfo()

    if lst is None:
        return None
    return (lst * 0.02) - 273.15  # Convert Kelvin to Celsius

# -----------------------------
# Fetch Ground Temp (Weather API)
# -----------------------------
def get_weather_temp(lat, lon):
    """Fetch real ground temperature from OpenWeatherMap"""
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    try:
        r = requests.get(url, timeout=10).json()
        return r["main"]["temp"] if "main" in r else None
    except Exception:
        return None

# -----------------------------
# Collect Training Data
# -----------------------------
X, y = [], []

for city in cities:
    name, lat, lon = city["name"], city["lat"], city["lon"]

    lst_c = get_satellite_lst(lat, lon)
    temp_obs = get_weather_temp(lat, lon)

    if lst_c is not None and temp_obs is not None:
        print(f"📍 {name} → LST={lst_c:.2f}°C, Obs={temp_obs:.2f}°C")
        X.append([lat, lon, lst_c])
        y.append(temp_obs)
    else:
        print(f"⚠️ Skipping {name}: Missing data.")

# -----------------------------
# Train & Save Model
# -----------------------------
if len(X) > 5:  # Need at least 5 samples
    X = np.array(X)
    y = np.array(y)

    model = LinearRegression()
    model.fit(X, y)

    MODEL_PATH = os.path.join("app", "model", "avg_temp_model.pkl")
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"✅ Model trained & saved at {MODEL_PATH}")
else:
    print("⚠️ Not enough data collected to train model. Please check API or Earth Engine.")
