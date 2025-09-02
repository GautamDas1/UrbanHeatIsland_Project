import ee
import numpy as np
from datetime import datetime, timedelta

class UHIMLModel:
    def __init__(self, project_id="earthengine-uhi"):
        """
        Initialize the Earth Engine client.
        Make sure you have authenticated with `earthengine authenticate`.
        """
        try:
            ee.Initialize(project=project_id)
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize Earth Engine: {e}. "
                f"Ensure you authenticated with `earthengine authenticate` and project ID is correct."
            ) from e

    # ------------------ Fetch Satellite Data ------------------
    def fetch_satellite_data(self, lat, lon):
        """
        Fetch average LST (Land Surface Temperature) for a given lat/lon.
        Uses MODIS MOD11A1 dataset (daily).
        """
        point = ee.Geometry.Point(lon, lat)
        start_date = "2023-01-01"
        end_date = "2023-12-31"

        dataset = ee.ImageCollection("MODIS/061/MOD11A1") \
            .filterDate(start_date, end_date) \
            .filterBounds(point) \
            .select("LST_Day_1km")

        mean_lst_image = dataset.mean()
        reduction = mean_lst_image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=1000,
            maxPixels=1e9
        )

        try:
            temp_val_ee = reduction.get("LST_Day_1km")
            temp_val = temp_val_ee.getInfo() if temp_val_ee is not None else None
        except Exception as e:
            print(f"❌ Error fetching satellite data for ({lat}, {lon}): {e}")
            return None

        if temp_val is not None:
            # Convert to Celsius
            return round((temp_val * 0.02) - 273.15, 2)
        else:
            return None

    # ------------------ Heatmap Generation ------------------
    def generate_heatmap_url(self, lat, lon):
        """
        Generate a heatmap tile URL for a given lat/lon using MODIS data.
        Returns a URL template usable in Leaflet or Mapbox.
        """
        point = ee.Geometry.Point(lon, lat)
        region = point.buffer(5000).bounds()

        end_date = datetime.today()
        start_date = end_date - timedelta(days=14)  # Last 14 days window

        collection = ee.ImageCollection("MODIS/061/MOD11A1") \
            .filterDate(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")) \
            .filterBounds(point) \
            .select("LST_Day_1km")

        if collection.size().getInfo() == 0:
            print(f"⚠️ No MODIS data available for heatmap in last 14 days at ({lat}, {lon}).")
            return None

        dataset_mean = collection.mean()
        lst_celsius = dataset_mean.multiply(0.02).subtract(273.15)

        thermal_map = lst_celsius.visualize(
            min=20,
            max=45,
            palette=["blue", "cyan", "green", "yellow", "orange", "red"]
        )

        try:
            map_id_dict = ee.data.getMapId({
                "image": thermal_map,
                "region": region.getInfo()
            })
            return (
                f"https://earthengine.googleapis.com/map/{map_id_dict['mapid']}"
                f"/{{z}}/{{x}}/{{y}}?token={map_id_dict['token']}"
            )
        except Exception as e:
            print(f"❌ Error generating heatmap URL for ({lat}, {lon}): {e}")
            return None

    # ------------------ UHI Prediction ------------------
    def predict_uhi(self, lat, lon, city_name="Unknown Location"):
        """
        Predict UHI metrics for given coordinates.
        Returns: avg_temp, mitigated_temp, risk_level
        """
        avg_temp = self.fetch_satellite_data(lat, lon)
        if avg_temp is None:
            raise ValueError(
                f"No satellite data available for {city_name} at ({lat}, {lon})."
            )

        mitigated_temp = round(avg_temp * 0.85, 2)  # Example mitigation factor (15% cooling)

        # Risk level classification
        if avg_temp >= 38:
            level = "High"
        elif avg_temp >= 34:
            level = "Medium"
        else:
            level = "Low"

        return avg_temp, mitigated_temp, level
