import numpy as np
import ee
import json
import os

# ------------------ Earth Engine Initialization ------------------
try:
    ee.Initialize(project='earthengine-uhi')  # Replace with your EE project ID
except Exception as e:
    raise RuntimeError("Failed to initialize Earth Engine. Make sure you authenticated.") from e


# ------------------ Preprocess City Satellite Data ------------------
def preprocess_city_data(city_name, city_coordinates=None):
    """
    Retrieves and processes satellite data for the given city.

    Args:
        city_name (str): Name of the city.
        city_coordinates (dict): Mapping city names to (lat, lon) tuples.
                                 If None, assumes CITY_COORDINATES is globally available.

    Returns:
        np.ndarray: 2D numpy array with features: NDVI, LST_day, LST_night, green_space_percent
    """
    coords_source = city_coordinates if city_coordinates is not None else globals().get('CITY_COORDINATES')

    if coords_source is None or city_name not in coords_source:
        raise ValueError(f"City '{city_name}' is not in the predefined list or coordinates not provided.")

    lat, lon = coords_source[city_name]
    point = ee.Geometry.Point([lon, lat])

    # Date range for data retrieval
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    
    # -------- 1. NDVI --------
    ndvi_collection = ee.ImageCollection("MODIS/006/MOD13A1") \
        .filterDate(start_date, end_date) \
        .filterBounds(point) \
        .select("NDVI")

    ndvi_image = ndvi_collection.mean()
    ndvi_dict = ndvi_image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=point,
        scale=500,
        maxPixels=1e9
    ).getInfo()

    ndvi_value = ndvi_dict.get("NDVI", None)
    ndvi_value = (ndvi_value / 10000.0) if ndvi_value is not None else 0.2

    # -------- 2. LST --------
    lst_collection = ee.ImageCollection("MODIS/006/MOD11A2") \
        .filterDate(start_date, end_date) \
        .filterBounds(point) \
        .select("LST_Day_1km", "LST_Night_1km")

    lst_image = lst_collection.mean()
    lst_dict = lst_image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=point,
        scale=1000,
        maxPixels=1e9
    ).getInfo()

    lst_day = lst_dict.get("LST_Day_1km", None)
    lst_night = lst_dict.get("LST_Night_1km", None)
    
    lst_day = (lst_day * 0.02) - 273.15 if lst_day is not None else 30.0
    lst_night = (lst_night * 0.02) - 273.15 if lst_night is not None else 20.0

    # -------- 3. Green Space --------
    green_space_percent = max(0.0, ndvi_value * 100.0)

    return np.array([ndvi_value, lst_day, lst_night, green_space_percent]).reshape(1, -1)


# ------------------ Load City Data from JSON ------------------
def load_city_data(base_dir=None):
    """
    Load Indian cities from the JSON file.
    base_dir: optional, the base directory of the app (Flask app config["BASE_DIR"])
    """
    if base_dir is None:
        base_dir = os.path.dirname(__file__)  # folder containing utils.py

    file_path = os.path.join(base_dir, "data", "indian_cities.json")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"City data JSON file not found at {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
