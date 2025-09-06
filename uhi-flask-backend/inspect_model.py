import joblib
import os

# Path to your model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "app", "model", "avg_temp_model.pkl")

# Load model
model = joblib.load(MODEL_PATH)

print("✅ Model loaded successfully!")
print("Model type:", type(model))

# If it's a scikit-learn model, print details
if hasattr(model, "n_features_in_"):
    print("Number of input features:", model.n_features_in_)

if hasattr(model, "feature_names_in_"):
    print("Feature names:", model.feature_names_in_)

# Try predicting with a sample input
sample = [[28.61, 77.20, 35.0]]  # [lat, lon, LST]
try:
    prediction = model.predict(sample)
    print("Sample prediction:", prediction)
except Exception as e:
    print("⚠️ Could not predict with sample:", e)
