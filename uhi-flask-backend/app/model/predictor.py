import ee
from datetime import datetime, timedelta

class UHIMLModel:
    def __init__(self, project_id="earthengine-uhi"):
        try:
            ee.Initialize(project=project_id)
            print("✅ Earth Engine initialized successfully!")
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize Earth Engine: {e}. "
                f"Authenticate first using `earthengine authenticate`."
            ) from e

    # ------------------ Fetch Satellite LST (Day) ------------------
    def fetch_satellite_data(self, lat, lon):
        point = ee.Geometry.Point(lon, lat)
        start_date = "2023-01-01"
        end_date = "2023-12-31"

        dataset = ee.ImageCollection("MODIS/061/MOD11A1") \
            .filterDate(start_date, end_date) \
            .filterBounds(point) \
            .select("LST_Day_1km")

        if dataset.size().getInfo() == 0:
            print(f"⚠️ No MODIS LST data at ({lat},{lon})")
            return None

        mean_image = dataset.mean()
        reduction = mean_image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=1000,
            maxPixels=1e9
        )

        try:
            val = reduction.get("LST_Day_1km")
            val = val.getInfo() if val else None
        except Exception as e:
            print(f"❌ Error fetching satellite data ({lat},{lon}): {e}")
            return None

        if val is not None:
            return round((val * 0.02) - 273.15, 2)
        else:
            return None

    # ------------------ Fetch Green Space % using MODIS NDVI ------------------
    def fetch_green_space_percent(self, lat, lon, radius_km=5):
        point = ee.Geometry.Point(lon, lat)
        region = point.buffer(radius_km * 1000)  # radius in meters

        ndvi_collection = ee.ImageCollection("MODIS/061/MOD13A1") \
            .filterDate("2023-01-01", "2023-12-31") \
            .select("NDVI") \
            .mean()  # annual mean NDVI

        veg_pixels = ndvi_collection.gt(3000)  # NDVI > 0.3

        green_fraction = veg_pixels.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=500,
            maxPixels=1e9
        ).get("NDVI").getInfo()

        return round(green_fraction * 100, 2) if green_fraction else 0

    # ------------------ Heatmap URL ------------------
    def generate_heatmap_url(self, lat, lon):
        point = ee.Geometry.Point(lon, lat)
        region = point.buffer(5000).bounds()

        end_date = datetime.today()
        start_date = end_date - timedelta(days=14)

        collection = ee.ImageCollection("MODIS/061/MOD11A1") \
            .filterDate(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")) \
            .filterBounds(point) \
            .select("LST_Day_1km")

        if collection.size().getInfo() == 0:
            print(f"⚠️ No MODIS data for last 14 days at ({lat},{lon})")
            return None

        dataset_mean = collection.mean()
        lst_celsius = dataset_mean.multiply(0.02).subtract(273.15)

        thermal_map = lst_celsius.visualize(
            min=20, max=45,
            palette=["blue","cyan","green","yellow","orange","red"]
        )

        try:
            map_id_dict = ee.data.getMapId({
                "image": thermal_map,
                "region": region.getInfo()
            })
            return f"https://earthengine.googleapis.com/map/{map_id_dict['mapid']}/{{z}}/{{x}}/{{y}}?token={map_id_dict['token']}"
        except Exception as e:
            print(f"❌ Error generating heatmap URL ({lat},{lon}): {e}")
            return None

    # ------------------ UHI Prediction ------------------
    def predict_uhi(self, lat, lon, green_space_percent=None, city_name="Unknown Location"):
        avg_temp = self.fetch_satellite_data(lat, lon)
        if avg_temp is None:
            raise ValueError(f"No satellite data for {city_name} at ({lat},{lon})")

        # If green_space_percent not provided, fetch automatically
        if green_space_percent is None:
            green_space_percent = self.fetch_green_space_percent(lat, lon)

        # Mitigated temperature factoring green space
        mitigation_factor = 0.85 + (green_space_percent / 100 * 0.1)  # up to +10% cooling
        mitigated_temp = round(avg_temp * mitigation_factor, 2)

        # Risk level
        if avg_temp >= 38:
            level = "High"
        elif avg_temp >= 34:
            level = "Medium"
        else:
            level = "Low"

        return avg_temp, mitigated_temp, level, green_space_percent
