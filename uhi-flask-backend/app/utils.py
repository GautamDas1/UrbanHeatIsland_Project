import logging
import datetime
import ee
from .model.predictor import UHIMLModel

# ------------------ Logging ------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------ Earth Engine Service Account Setup ------------------
SERVICE_ACCOUNT = "Email_Project"  # e.g., uhi-backend@your-project.iam.gserviceaccount.com
KEY_FILE = "YOur_Key_Json_file"
  # path to the JSON key you downloaded

try:
    credentials = ee.ServiceAccountCredentials(SERVICE_ACCOUNT, KEY_FILE)
    ee.Initialize(credentials)
    logger.info("✅ Earth Engine initialized successfully with service account!")
except Exception as e:
    logger.error(f"❌ Failed to initialize Earth Engine: {e}")

# ------------------ Initialize UHI Model ------------------
try:
    uhi_model = UHIMLModel()
    logger.info("✅ UHI model initialized successfully!")
except Exception as e:
    logger.error(f"❌ Failed to initialize UHI model: {e}")
    uhi_model = None

# ------------------ Green Space Fetch Function ------------------
def get_green_space_percentage(lat, lon, radius_km=10):
    """
    Calculate green space percentage around a point using NDVI from Google Earth Engine.
    """
    try:
        point = ee.Geometry.Point([lon, lat])
        buffer = point.buffer(radius_km * 1000)

        # Sentinel-2 imagery from last year
        start_date = '2025-08-01'  # Aug–Sep is greener
        end_date = '2025-10-31'

        collection = (
            ee.ImageCollection('COPERNICUS/S2')
            .filterBounds(buffer)
            .filterDate(str(start_date), str(end_date))
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
            .select(['B8', 'B4'])  # NIR and Red bands
        )

        image = collection.median()
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        green_pixels = ndvi.gt(0.2)

        stats = green_pixels.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=buffer,
            scale=10,
            maxPixels=1e13
        )

        green_percent = stats.get('NDVI').getInfo() * 100
        return round(green_percent, 2)

    except Exception as e:
        logger.error(f"❌ Failed to fetch green space: {e}")
        return 0.0  # fallback value

# ------------------ Data Preprocessing ------------------
def preprocess_city_data(city_data):
    try:
        lat = float(city_data.get("lat"))
        lon = float(city_data.get("lon"))
        green_cover = city_data.get("green_space_percent", None)
        if green_cover is not None:
            green_cover = float(green_cover)
        return {"lat": lat, "lon": lon, "green_space_percent": green_cover}
    except Exception as e:
        logger.error(f"❌ Error preprocessing city data: {e}")
        raise ValueError("Invalid city data input") from e

# ------------------ Prediction Wrapper ------------------
def get_uhi_metrics(city_data):
    if uhi_model is None:
        raise RuntimeError("UHI model not initialized.")

    try:
        processed = preprocess_city_data(city_data)

        # Fetch green space if not provided
        if processed["green_space_percent"] is None:
            logger.info("🌿 Fetching real green space from satellite...")
            processed["green_space_percent"] = get_green_space_percentage(
                lat=processed["lat"],
                lon=processed["lon"],
                radius_km=10
            )
            logger.info(f"✅ Green space fetched: {processed['green_space_percent']}%")

        # Call UHI model
        avg_temp, mitigated_temp, level, green_space_percent = uhi_model.predict_uhi(
            lat=processed["lat"],
            lon=processed["lon"],
            green_space_percent=processed["green_space_percent"]
        )

        return {
            "avg_temp": avg_temp,
            "mitigated_temp": mitigated_temp,
            "green_space_percent": green_space_percent,
            "risk_level": level
        }

    except Exception as e:
        logger.error(
            f"❌ Error fetching data for coordinates ({city_data.get('lat')}, {city_data.get('lon')}): {e}"
        )
        raise
