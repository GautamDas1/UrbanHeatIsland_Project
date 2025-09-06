import logging
from .model.predictor import UHIMLModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the model once
try:
    uhi_model = UHIMLModel()
    logger.info("✅ Earth Engine UHI model initialized successfully!")
except Exception as e:
    logger.error(f"❌ Failed to initialize UHI model: {e}")
    uhi_model = None

# ------------------ Data Preprocessing ------------------
def preprocess_city_data(city_data):
    """
    Preprocess incoming city data.
    Expects a dict with 'lat', 'lon', optionally 'green_space_percent'.
    """
    try:
        lat = float(city_data.get("lat"))
        lon = float(city_data.get("lon"))
        green_cover = city_data.get("green_space_percent", 0)  # default 0
        green_cover = float(green_cover)
        return {"lat": lat, "lon": lon, "green_space_percent": green_cover}
    except Exception as e:
        logger.error(f"❌ Error preprocessing city data: {e}")
        raise ValueError("Invalid city data input") from e

# ------------------ Prediction Wrapper ------------------
def get_uhi_metrics(city_data):
    """
    Returns avg_temp, mitigated_temp, risk_level for a city or custom area.
    """
    if uhi_model is None:
        raise RuntimeError("UHI model not initialized.")

    try:
        processed = preprocess_city_data(city_data)
        avg_temp, mitigated_temp, level = uhi_model.predict_uhi(
            lat=processed["lat"],
            lon=processed["lon"],
            green_space_percent=processed["green_space_percent"]
        )
        return {
            "avg_temp": avg_temp,
            "mitigated_temp": mitigated_temp,
            "level": level
        }
    except Exception as e:
        logger.error(f"❌ Error fetching data for coordinates ({city_data.get('lat')}, {city_data.get('lon')}): {e}")
        raise
