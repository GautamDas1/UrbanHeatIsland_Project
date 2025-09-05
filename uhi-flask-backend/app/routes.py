from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import logging
from .utils import preprocess_city_data

routes = Blueprint("routes", __name__)
logging.basicConfig(level=logging.INFO)

# ------------------ Prediction ------------------
@routes.route("/predict", methods=["GET"])
@cross_origin()
def predict():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    city_name = request.args.get("city", "Custom Location")

    if not lat or not lon:
        return jsonify({"error": "Latitude and Longitude are required"}), 400

    try:
        lat = float(lat)
        lon = float(lon)

        # Fetch real satellite data + AI prediction
        metrics = preprocess_city_data(lat, lon)

        response = {
            "city": city_name,
            "avg_temp": metrics["avg_temp"],
            "mitigated_temp": metrics["mitigated_temp"],
            "level": metrics["level"],
            "green_space_percent": metrics["green_space_percent"]
        }

        return jsonify(response)
    except Exception as e:
        logging.error(f"Error fetching data for {city_name}: {e}")
        return jsonify({"error": str(e)}), 500

# ------------------ Heatmap ------------------
@routes.route("/heatmap", methods=["GET"])
@cross_origin()
def heatmap():
    return jsonify({"message": "Heatmap API placeholder"})

# ------------------ Cities ------------------
@routes.route("/cities", methods=["GET"])
@cross_origin()
def cities():
    city_list = [
        {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
        {"name": "Delhi", "lat": 28.7041, "lon": 77.1025},
        {"name": "Bangalore", "lat": 12.9716, "lon": 77.5946},
        {"name": "Hyderabad", "lat": 17.3850, "lon": 78.4867},
        {"name": "Ahmedabad", "lat": 23.0225, "lon": 72.5714},
        {"name": "Chennai", "lat": 13.0827, "lon": 80.2707},
        {"name": "Kolkata", "lat": 22.5726, "lon": 88.3639},
        {"name": "Pune", "lat": 18.5204, "lon": 73.8567},
        {"name": "Jaipur", "lat": 26.9124, "lon": 75.7873},
        {"name": "Surat", "lat": 21.1702, "lon": 72.8311},
        {"name": "Lucknow", "lat": 26.8467, "lon": 80.9462},
        {"name": "Kanpur", "lat": 26.4499, "lon": 80.3319},
        {"name": "Nagpur", "lat": 21.1458, "lon": 79.0882},
        {"name": "Indore", "lat": 22.7196, "lon": 75.8577},
        {"name": "Bhopal", "lat": 23.2599, "lon": 77.4126},
        {"name": "Patna", "lat": 25.5941, "lon": 85.1376},
        {"name": "Varanasi", "lat": 25.3176, "lon": 82.9739},
        {"name": "Srinagar", "lat": 34.0837, "lon": 74.7973},
        {"name": "Coimbatore", "lat": 11.0168, "lon": 76.9558},
        {"name": "Raipur", "lat": 21.2514, "lon": 81.6296}
    ]
    return jsonify(city_list)
