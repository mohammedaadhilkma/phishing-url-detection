import sys
import os
import joblib
import numpy as np

# Add model directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'model'))
from feature_extractor import extract_features
from advanced_features import analyze_advanced_features

# Load Model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'phishing_model.pkl')
model = joblib.load(MODEL_PATH)

url = "www.google./p.comm/ksj"

print(f"--- Debugging URL: {url} ---")

# 1. Feature Extraction
features = extract_features(url)
feature_names = [
    "Length", "Has IP", "Dot Count", "Has @", "Has -", "Has HTTPS", "Subdomain Count", "Suspicious Words"
]
print("\n[ML Features]")
for name, value in zip(feature_names, features):
    print(f"{name}: {value}")

# 2. Prediction
prediction = model.predict([features])[0]
proba = model.predict_proba([features])[0]
print("\n[Model Prediction]")
print(f"Class: {prediction} (0=Legit, 1=Phishing)")
print(f"Probabilities: Legit={proba[0]:.4f}, Phishing={proba[1]:.4f}")

# 3. Advanced Features
print("\n[Advanced Analysis]")
adv = analyze_advanced_features(url)
print(adv)
