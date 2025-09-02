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
            return jsonify({"error": "city_metrics.json not found"}), 500

        # Find city in JSON (fix: use "city" instead of "name")
        match = next((m for m in metrics if m["city"].lower() == city_name.lower()), None)

        # If no match found → fallback response
        if not match:
            logging.warning(f"No data found for {city_name}, returning fallback.")
            avg_temp = round(float(lat) % 40 + 20, 2)   # just dummy value
            mitigated_temp = round(avg_temp * 0.9, 2)
            return jsonify({
                "city": city_name,
                "avg_temp": avg_temp,
                "mitigated_temp": mitigated_temp,
                "level": "Medium"
            })

        return jsonify({
            "city": city_name,
            "avg_temp": match["original_LST"],
            "mitigated_temp": match["mitigated_LST"],
            "level": match["level"]
        })
    except Exception as e:
        logging.error(f"Error in prediction for {city_name}: {e}")
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
        logging.error(f"Error in heatmap generation: {e}")
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
        logging.error(f"Error loading cities: {e}")
        return jsonify({"error": str(e)}), 500
