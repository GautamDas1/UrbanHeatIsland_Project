import ee
import numpy as np
from datetime import datetime, timedelta

class UHIMLModel:
    def __init__(self, project_id=None):
        try:
            ee.Initialize(project='earthengine-uhi')
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Earth Engine: {e}. Make sure you authenticated and project ID is correct.") from e

    def fetch_satellite_data(self, lat, lon):
        point = ee.Geometry.Point(lon, lat)
        start_date = '2023-01-01'
        end_date = '2023-12-31'
        dataset = ee.ImageCollection('MODIS/061/MOD11A1') \
            .filterDate(start_date, end_date) \
            .filterBounds(point) \
            .select('LST_Day_1km')

        mean_lst_image = dataset.mean()
        reduction = mean_lst_image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=1000,
            maxPixels=1e9
        )
        try:
            temp_val_ee = reduction.get('LST_Day_1km')
            temp_val = temp_val_ee.getInfo()
        except Exception as e:
            print(f"Error fetching satellite data for ({lat}, {lon}): {e}")
            return None

        if temp_val is not None:
            return round((temp_val * 0.02) - 273.15, 2)
        else:
            return None

    def generate_heatmap_url(self, lat, lon):
        point = ee.Geometry.Point(lon, lat)
        region = point.buffer(5000).bounds()

        end_date = datetime.today()
        # Broaden date range slightly for better chance of data availability
        start_date = end_date - timedelta(days=14) # Changed to 14 days

        # Switching to MODIS/061/MOD11A1 for heatmap as it's more reliable and active
        # Selecting LST_Day_1km for consistency with fetch_satellite_data
        collection = ee.ImageCollection("MODIS/061/MOD11A1") \
            .filterDate(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')) \
            .filterBounds(point) \
            .select('LST_Day_1km') # Ensures the correct band is selected

        # Check if the image collection is empty before computing mean
        if collection.size().getInfo() == 0:
            print(f"No MODIS/061/MOD11A1 data available for heatmap generation in the last 14 days for ({lat}, {lon}).")
            return None # Return None if no data

        dataset_mean = collection.mean()

        lst_celsius = dataset_mean.multiply(0.02).subtract(273.15)

        thermal_map = lst_celsius.visualize(
            min=20, max=45,
            palette=['blue', 'cyan', 'green', 'yellow', 'orange', 'red']
        )
        
        try:
            map_id_dict = ee.data.getMapId({'image': thermal_map, 'region': region.getInfo()})
            return f"https://earthengine.googleapis.com/map/{map_id_dict['mapid']}/{{z}}/{{x}}/{{y}}?token={map_id_dict['token']}"
        except Exception as e:
            print(f"Error generating heatmap URL for ({lat}, {lon}): {e}")
            return None

    def predict_uhi(self, lat, lon, city_name="Unknown Location"):
        avg_temp = self.fetch_satellite_data(lat, lon)
        if avg_temp is None:
            raise ValueError(f"No satellite data available for {city_name} at ({lat}, {lon}).")
        mitigated_temp = round(avg_temp * 0.85, 2)
        if avg_temp >= 38:
            level = "High"
        elif avg_temp >= 34:
            level = "Medium"
        else:
            level = "Low"
        return avg_temp, mitigated_temp, level
