import logging
import datetime
import ee
from .model.predictor import UHIMLModel

# ------------------ Logging ------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------ Earth Engine Service Account Setup ------------------
SERVICE_ACCOUNT = "uhi-backend@earthengine-uhi.iam.gserviceaccount.com"
KEY_FILE = r"D:\jsonfile\earthengine-uhi-9da822721bd6.json"

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
def get_green_space_percentage(lat, lon, radius_km=5):
    """
    Calculate green space percentage around a point using NDVI from Google Earth Engine.
    Improved method: uses Sentinel-2, 1-year range, and urban+vegetation mask.
    """
    try:
        point = ee.Geometry.Point([lon, lat])
        buffer = point.buffer(radius_km * 1000)

        # 1-year range (dynamic, always latest year)
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=365)

        # Sentinel-2 collection
        collection = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(buffer)
            .filterDate(str(start_date), str(end_date))
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
            .select(["B8", "B4"])  # NIR and Red bands
        )

        image = collection.median()

        # NDVI calculation
        ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")

        # Consider vegetation if NDVI > 0.2 (captures both dense & sparse vegetation)
        green_pixels = ndvi.gt(0.2)

        # Mask urban area from ESA WorldCover but keep vegetation too
        worldcover = ee.ImageCollection("ESA/WorldCover/v100").first().clip(buffer)
        # Class 50 = Tree cover, 40 = Shrubland, 30 = Grassland
        vegetation_mask = worldcover.remap([10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100],
                                           [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0])
        combined_mask = green_pixels.updateMask(vegetation_mask)

        stats = combined_mask.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=buffer,
            scale=10,
            maxPixels=1e13
        )

        green_percent = stats.get("NDVI").getInfo()
        if green_percent is None:
            green_percent = 0.0
        else:
            green_percent = green_percent * 100

        return round(green_percent, 2)

    except Exception as e:
        logger.error(f"❌ Failed to fetch green space: {e}")
        return 0.0  # fallback


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

        # Fetch real green space if not provided
        if processed["green_space_percent"] is None:
            logger.info("🌿 Fetching real green space from satellite...")
            processed["green_space_percent"] = get_green_space_percentage(
                lat=processed["lat"],
                lon=processed["lon"],
                radius_km=5
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
