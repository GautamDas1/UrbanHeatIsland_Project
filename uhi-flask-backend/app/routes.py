from flask import Blueprint, jsonify, request, current_app
from flask_cors import cross_origin
import logging
import os, json

routes = Blueprint("routes", __name__)
logging.basicConfig(level=logging.INFO)

# --- Utility to load JSON ---
def load_json(filename):
    base_dir = os.path.join(current_app.root_path, "data")
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        logging.error(f"File not found: {filepath}")
        return None
    with open(filepath, "r") as f:
        return json.load(f)


# --- Utility: Predict metrics for custom lat/lon ---
def predict_metrics(lat, lon):
    """
    Return a reasonable estimate for avg and mitigated LST
    if city not found in city_metrics.json.
    """
    try:
        lat = float(lat)
        lon = float(lon)
        avg_temp = round((lat % 40) + 25, 2)      # Example formula
        mitigated_temp = round(avg_temp * 0.9, 2)
        # Determine UHI level based on avg_temp
        if avg_temp >= 45:
            level = "High"
        elif avg_temp >= 35:
            level = "Medium"
        else:
            level = "Low"
        return {
            "city": "Custom Location",
            "avg_temp": avg_temp,
            "mitigated_temp": mitigated_temp,
            "level": level
        }
    except Exception as e:
        logging.error(f"Error in predict_metrics: {e}")
        return {
            "city": "Custom Location",
            "avg_temp": 0,
            "mitigated_temp": 0,
            "level": "Low"
        }


# ✅ Prediction endpoint
@routes.route("/predict", methods=["GET"])
@cross_origin()
def predict():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    city_name = request.args.get("city", "Unknown Location")

    if not lat or not lon:
        return jsonify({"error": "Latitude and Longitude are required"}), 400

    try:
        metrics = load_json("city_metrics.json")
        if not metrics:
            logging.warning("city_metrics.json not found, using dynamic prediction")
            return jsonify(predict_metrics(lat, lon))

        # Find city in JSON
        match = next((m for m in metrics if m["city"].lower() == city_name.lower()), None)

        # If city found in JSON
        if match:
            return jsonify({
                "city": city_name,
                "avg_temp": match.get("original_LST", 0),
                "mitigated_temp": match.get("mitigated_LST", 0),
                "level": match.get("level", "Medium")
            })

        # If city not found → use dynamic prediction
        logging.info(f"No data for {city_name}, using dynamic prediction")
        return jsonify(predict_metrics(lat, lon))

    except Exception as e:
        logging.error(f"Error in /predict for {city_name}: {e}")
        return jsonify({"error": str(e)}), 500


# ✅ Heatmap endpoint
@routes.route("/heatmap", methods=["GET"])
@cross_origin()
def heatmap():
    try:
        data = load_json("heatmap_data.json")
        if not data:
            return jsonify({"error": "heatmap_data.json not found"}), 500
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error in /heatmap: {e}")
        return jsonify({"error": str(e)}), 500


# ✅ Cities endpoint
@routes.route("/cities", methods=["GET"])
@cross_origin()
def cities():
    try:
        cities = load_json("indian_cities.json")
        if not cities:
            return jsonify({"error": "indian_cities.json not found"}), 500
        return jsonify(cities)
    except Exception as e:
        logging.error(f"Error loading /cities: {e}")
        return jsonify({"error": str(e)}), 500
