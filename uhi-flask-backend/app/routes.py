from flask import Blueprint, jsonify, request
from .utils import get_uhi_metrics

routes = Blueprint("routes", __name__)

# ------------------ 50 Indian Cities ------------------
CITIES = [
    {"name": "Delhi", "lat": 28.7041, "lon": 77.1025, "green_space_percent": 12},
    {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777, "green_space_percent": 8},
    {"name": "Chennai", "lat": 13.0827, "lon": 80.2707, "green_space_percent": 15},
    {"name": "Kolkata", "lat": 22.5726, "lon": 88.3639, "green_space_percent": 7},
    {"name": "Bengaluru", "lat": 12.9716, "lon": 77.5946, "green_space_percent": 18},
    {"name": "Hyderabad", "lat": 17.3850, "lon": 78.4867, "green_space_percent": 16},
    {"name": "Ahmedabad", "lat": 23.0225, "lon": 72.5714, "green_space_percent": 10},
    {"name": "Pune", "lat": 18.5204, "lon": 73.8567, "green_space_percent": 20},
    {"name": "Jaipur", "lat": 26.9124, "lon": 75.7873, "green_space_percent": 14},
    {"name": "Lucknow", "lat": 26.8467, "lon": 80.9462, "green_space_percent": 11},
    {"name": "Kanpur", "lat": 26.4499, "lon": 80.3319, "green_space_percent": 9},
    {"name": "Nagpur", "lat": 21.1458, "lon": 79.0882, "green_space_percent": 13},
    {"name": "Indore", "lat": 22.7196, "lon": 75.8577, "green_space_percent": 17},
    {"name": "Thane", "lat": 19.2183, "lon": 72.9781, "green_space_percent": 12},
    {"name": "Bhopal", "lat": 23.2599, "lon": 77.4126, "green_space_percent": 19},
    {"name": "Visakhapatnam", "lat": 17.6868, "lon": 83.2185, "green_space_percent": 15},
    {"name": "Vadodara", "lat": 22.3072, "lon": 73.1812, "green_space_percent": 14},
    {"name": "Coimbatore", "lat": 11.0168, "lon": 76.9558, "green_space_percent": 18},
    {"name": "Patna", "lat": 25.5941, "lon": 85.1376, "green_space_percent": 8},
    {"name": "Ghaziabad", "lat": 28.6692, "lon": 77.4538, "green_space_percent": 10},
    {"name": "Ludhiana", "lat": 30.9010, "lon": 75.8573, "green_space_percent": 12},
    {"name": "Agra", "lat": 27.1767, "lon": 78.0081, "green_space_percent": 9},
    {"name": "Nashik", "lat": 19.9975, "lon": 73.7898, "green_space_percent": 16},
    {"name": "Faridabad", "lat": 28.4089, "lon": 77.3178, "green_space_percent": 11},
    {"name": "Meerut", "lat": 28.9845, "lon": 77.7064, "green_space_percent": 10},
    {"name": "Rajkot", "lat": 22.3039, "lon": 70.8022, "green_space_percent": 14},
    {"name": "Kalyan", "lat": 19.2433, "lon": 73.1308, "green_space_percent": 13},
    {"name": "Vasai-Virar", "lat": 19.3910, "lon": 72.8397, "green_space_percent": 12},
    {"name": "Varanasi", "lat": 25.3176, "lon": 82.9739, "green_space_percent": 8},
    {"name": "Srinagar", "lat": 34.0837, "lon": 74.7973, "green_space_percent": 20},
    {"name": "Aurangabad", "lat": 19.8762, "lon": 75.3433, "green_space_percent": 15},
    {"name": "Dhanbad", "lat": 23.7957, "lon": 86.4304, "green_space_percent": 10},
    {"name": "Amritsar", "lat": 31.6340, "lon": 74.8723, "green_space_percent": 18},
    {"name": "Navi Mumbai", "lat": 19.0330, "lon": 73.0297, "green_space_percent": 12},
    {"name": "Allahabad", "lat": 25.4358, "lon": 81.8463, "green_space_percent": 9},
    {"name": "Ranchi", "lat": 23.3441, "lon": 85.3096, "green_space_percent": 14},
    {"name": "Howrah", "lat": 22.5958, "lon": 88.2636, "green_space_percent": 10},
    {"name": "Jabalpur", "lat": 23.1815, "lon": 79.9864, "green_space_percent": 13},
    {"name": "Gwalior", "lat": 26.2183, "lon": 78.1828, "green_space_percent": 15},
    {"name": "Bhubaneswar", "lat": 20.2961, "lon": 85.8245, "green_space_percent": 17},
    {"name": "Moradabad", "lat": 28.8388, "lon": 78.7730, "green_space_percent": 10},
    {"name": "Jodhpur", "lat": 26.2389, "lon": 73.0243, "green_space_percent": 12},
    {"name": "Raipur", "lat": 21.2514, "lon": 81.6296, "green_space_percent": 16},
    {"name": "Kota", "lat": 25.2138, "lon": 75.8648, "green_space_percent": 13},
    {"name": "Guwahati", "lat": 26.1445, "lon": 91.7362, "green_space_percent": 14},
    {"name": "Chandigarh", "lat": 30.7333, "lon": 76.7794, "green_space_percent": 18},
    {"name": "Mysore", "lat": 12.2958, "lon": 76.6394, "green_space_percent": 17},
    {"name": "Tiruchirappalli", "lat": 10.7905, "lon": 78.7047, "green_space_percent": 15},
    {"name": "Bareilly", "lat": 28.3670, "lon": 79.4304, "green_space_percent": 11},
    {"name": "Aligarh", "lat": 27.8974, "lon": 78.0880, "green_space_percent": 10},
    {"name": "Tirupati", "lat": 13.6288, "lon": 79.4192, "green_space_percent": 16},
]

# ------------------ Routes ------------------
@routes.route("/cities", methods=["GET"])
def list_cities():
    return jsonify(CITIES)


@routes.route("/predict", methods=["GET"])
def predict():
    try:
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))
        city_name = request.args.get("city", "Unknown")
        # Find city in list
        city_data = next((c for c in CITIES if c["lat"] == lat and c["lon"] == lon), None)
        if not city_data:
            # Custom location fallback
            city_data = {"lat": lat, "lon": lon, "green_space_percent": 10}
        metrics = get_uhi_metrics(city_data)
        return jsonify(metrics)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route("/heatmap", methods=["GET"])
def heatmap():
    # Placeholder heatmap API
    return jsonify({"heatmap": [{"lat": c["lat"], "lon": c["lon"], "intensity": 1} for c in CITIES]})
