from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from .utils import load_city_data
from .model.predictor import UHIMLModel
import logging
# from .utils import load_city_data


routes = Blueprint('routes', __name__)
uhi_model = UHIMLModel()

logging.basicConfig(level=logging.INFO)

@routes.route("/predict", methods=["GET"])
@cross_origin()
def predict():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    city_name = request.args.get("city", "Unknown Location")

    if not lat or not lon:
        return jsonify({"error": "Latitude and Longitude are required"}), 400

    try:
        avg_temp, mitigated_temp, level = uhi_model.predict_uhi(float(lat), float(lon), city_name)
        return jsonify({
            "city": city_name,
            "avg_temp": avg_temp,
            "mitigated_temp": mitigated_temp,
            "level": level
        })
    except Exception as e:
        logging.error(f"Error in prediction for {city_name}: {e}")
        return jsonify({"error": str(e)}), 500


@routes.route("/heatmap", methods=["GET"])
@cross_origin()
def heatmap():
    """
    Returns heatmap tile URLs for all cities from indian_cities.json
    """
    try:
        cities = load_city_data()
        heatmap_data = []

        for city in cities:
            city_name = city.get("name")
            lat = city.get("lat")
            lon = city.get("lon")

            if lat is None or lon is None:
                logging.warning(f"Skipping {city_name} due to missing coordinates")
                continue

            logging.info(f"Generating heatmap for {city_name} at ({lat}, {lon})")

            try:
                tile_url = uhi_model.generate_heatmap_url(float(lat), float(lon))
                if not tile_url:
                    logging.warning(f"No heatmap available for {city_name}")
                    continue

                heatmap_data.append({
                    "city": city_name,
                    "lat": float(lat),
                    "lon": float(lon),
                    "heatmap_tile_url": tile_url
                })
            except Exception as e:
                logging.error(f"Error generating heatmap for {city_name}: {e}")
                continue

        return jsonify({"heatmap": heatmap_data})

    except Exception as e:
        logging.error(f"Error in heatmap generation: {e}")
        return jsonify({"error": str(e)}), 500


@routes.route("/cities", methods=["GET"])
@cross_origin()
def cities():
    try:
        cities = load_city_data()
        return jsonify({"cities": cities})
    except Exception as e:
        logging.error(f"Error loading cities: {e}")
        return jsonify({"error": str(e)}), 500
