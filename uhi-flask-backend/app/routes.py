from flask import Blueprint, jsonify, request
from .utils import get_uhi_metrics
import logging

routes = Blueprint("routes", __name__)
logger = logging.getLogger(__name__)

# ------------------ 50 Indian Cities (no dummy green space) ------------------
CITIES = [
    {"name": "Delhi", "lat": 28.7041, "lon": 77.1025},
    {"name": "Mumbai", "lat": 19.076, "lon": 72.8777},
    {"name": "Bengaluru", "lat": 12.9716, "lon": 77.5946},
    {"name": "Chennai", "lat": 13.0827, "lon": 80.2707},
    {"name": "Kolkata", "lat": 22.5726, "lon": 88.3639},
    {"name": "Hyderabad", "lat": 17.385, "lon": 78.4867},
    {"name": "Ahmedabad", "lat": 23.0225, "lon": 72.5714},
    {"name": "Pune", "lat": 18.5204, "lon": 73.8567},
    {"name": "Jaipur", "lat": 26.9124, "lon": 75.7873},
    {"name": "Lucknow", "lat": 26.8467, "lon": 80.9462},
    {"name": "Kanpur", "lat": 26.4499, "lon": 80.3319},
    {"name": "Nagpur", "lat": 21.1458, "lon": 79.0882},
    {"name": "Indore", "lat": 22.7196, "lon": 75.8577},
    {"name": "Thane", "lat": 19.2183, "lon": 72.9781},
    {"name": "Bhopal", "lat": 23.2599, "lon": 77.4126},
    {"name": "Visakhapatnam", "lat": 17.6868, "lon": 83.2185},
    {"name": "Pimpri-Chinchwad", "lat": 18.6278, "lon": 73.812},
    {"name": "Patna", "lat": 25.5941, "lon": 85.1376},
    {"name": "Vadodara", "lat": 22.3072, "lon": 73.1812},
    {"name": "Ghaziabad", "lat": 28.6692, "lon": 77.4538},
    {"name": "Ludhiana", "lat": 30.9000, "lon": 75.8573},
    {"name": "Agra", "lat": 27.1767, "lon": 78.0081},
    {"name": "Nashik", "lat": 19.9975, "lon": 73.7898},
    {"name": "Faridabad", "lat": 28.4089, "lon": 77.3178},
    {"name": "Meerut", "lat": 28.9845, "lon": 77.7064},
    {"name": "Rajkot", "lat": 22.3039, "lon": 70.8022},
    {"name": "Kalyan-Dombivli", "lat": 19.2403, "lon": 73.1306},
    {"name": "Vasai-Virar", "lat": 19.3914, "lon": 72.8397},
    {"name": "Varanasi", "lat": 25.3176, "lon": 82.9739},
    {"name": "Srinagar", "lat": 34.0837, "lon": 74.7973},
    {"name": "Dhanbad", "lat": 23.7957, "lon": 86.4304},
    {"name": "Jodhpur", "lat": 26.2389, "lon": 73.0243},
    {"name": "Coimbatore", "lat": 11.0168, "lon": 76.9558},
    {"name": "Bhubaneswar", "lat": 20.2961, "lon": 85.8245},
    {"name": "Mysore", "lat": 12.2958, "lon": 76.6394},
    {"name": "Gurgaon", "lat": 28.4595, "lon": 77.0266},
    {"name": "Aligarh", "lat": 27.8974, "lon": 78.0880},
    {"name": "Jalandhar", "lat": 31.3260, "lon": 75.5762},
    {"name": "Tiruchirappalli", "lat": 10.7905, "lon": 78.7047},
    {"name": "Ujjain", "lat": 23.1828, "lon": 75.7772},
    {"name": "Salem", "lat": 11.6643, "lon": 78.1460},
    {"name": "Mangalore", "lat": 12.9141, "lon": 74.8560},
    {"name": "Jammu", "lat": 32.7266, "lon": 74.8570},
    {"name": "Belgaum", "lat": 15.8497, "lon": 74.4977},
    {"name": "Guwahati", "lat": 26.1445, "lon": 91.7362},
    {"name": "Amritsar", "lat": 31.6340, "lon": 74.8723},
    {"name": "Solapur", "lat": 17.6599, "lon": 75.9064},
    {"name": "Ranchi", "lat": 23.3441, "lon": 85.3096},
    {"name": "Tirupati", "lat": 13.6288, "lon": 79.4192},
]

# ------------------ Routes ------------------

@routes.route("/cities", methods=["GET"])
def list_cities():
    """Return list of all predefined cities."""
    return jsonify(CITIES), 200


@routes.route("/predict", methods=["GET"])
def predict():
    """Predict UHI metrics for a given lat/lon (green space dynamic)."""
    try:
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))

        # Find city in predefined list or use lat/lon directly
        city_data = next((c for c in CITIES if c["lat"] == lat and c["lon"] == lon), None)
        if not city_data:
            city_data = {"lat": lat, "lon": lon}

        # Fetch UHI metrics (green space dynamically)
        metrics = get_uhi_metrics(city_data)
        return jsonify(metrics), 200

    except Exception as e:
        logger.error(f"❌ Error in /predict: {e}")
        return jsonify({"error": str(e)}), 500


@routes.route("/heatmap", methods=["GET"])
def heatmap():
    """Return heatmap array for all cities with dynamic green space."""
    heatmap_data = []
    for city in CITIES:
        try:
            metrics = get_uhi_metrics(city)
            heatmap_data.append({
                "lat": city["lat"],
                "lon": city["lon"],
                "mitigated_temp": metrics["mitigated_temp"],
                "green_space_percent": metrics.get("green_space_percent", 0),
                "risk_level": metrics.get("risk_level", "No Data")
            })
        except Exception as e:
            logger.warning(f"⚠️ Skipping city {city['name']} due to error: {e}")
            continue

    return jsonify({"heatmap": heatmap_data}), 200
