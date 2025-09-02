import ee
import logging

# Initialize Earth Engine
try:
    ee.Initialize(project='earthengine-uhi')
except Exception as e:
    logging.info("Authenticating Earth Engine...")
    ee.Authenticate(project='earthengine-uhi')
    ee.Initialize(project='earthengine-uhi')

# Example city green space percentages (can expand later)
CITY_GREEN_SPACE = {
    "Mumbai": 12,
    "Delhi": 14,
    "Bangalore": 17,
    # Add others as needed
}

def preprocess_city_data(lat, lon):
    """
    Fetch UHI metrics for given coordinates using MODIS/061/MOD11A2.
    Returns avg_temp, mitigated_temp, UHI level, and green space percent.
    """
    try:
        point = ee.Geometry.Point([lon, lat])

        # MODIS/061/MOD11A2 (8-day LST at 1km resolution)
        dataset = ee.ImageCollection("MODIS/061/MOD11A2").select("LST_Day_1km")
        dataset = dataset.filterDate("2025-01-01", "2025-08-31")  # adjust date range
        lst_image = dataset.mean().clip(point)

        # Get the temperature at the point (Kelvin -> Celsius)
        temp = lst_image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=1000
        ).getInfo()["LST_Day_1km"] * 0.02 - 273.15  # MODIS scale factor

        # Simple mitigation estimate (just for example)
        mitigated_temp = temp - 3  # assume 3°C reduction via green space

        # Determine UHI level
        if temp >= 45:
            level = "High"
        elif temp >= 40:
            level = "Medium"
        else:
            level = "Low"

        # Approximate green space % (if known)
        green_space = 0
        for city, perc in CITY_GREEN_SPACE.items():
            # simple distance check (optional)
            if abs(lat - point.coordinates().get(1).getInfo()) < 0.1 and abs(lon - point.coordinates().get(0).getInfo()) < 0.1:
                green_space = perc
                break

        return {
            "avg_temp": round(temp, 2),
            "mitigated_temp": round(mitigated_temp, 2),
            "level": level,
            "green_space_percent": green_space
        }

    except Exception as e:
        logging.error(f"Error fetching data for coordinates ({lat}, {lon}): {e}")
        return {
            "avg_temp": None,
            "mitigated_temp": None,
            "level": "Unknown",
            "green_space_percent": None
        }
