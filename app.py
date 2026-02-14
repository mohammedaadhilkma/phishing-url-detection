from flask import Flask, request, render_template
import joblib
import numpy as np
import os
import sys

# Add model directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'model'))
from feature_extractor import extract_features
from advanced_features import analyze_advanced_features

app = Flask(__name__)

# Load Model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'phishing_model.pkl')
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    print(f"Error: Model not found at {MODEL_PATH}. Run python model/train_model.py first.")
    model = None

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction_text = None
    url_input = ""
    error_message = None
    result_class = ""
    confidence = None
    advanced_results = None

    if request.method == 'POST':
        url_input = request.form.get('url', '')
        if not url_input:
            error_message = "Please enter a URL."
        elif model:
            try:
                # Extract features
                features = extract_features(url_input)
                # Predict
                prediction = model.predict([features])[0]
                
                # Get probabilities if available
                if hasattr(model, "predict_proba"):
                    proba = model.predict_proba([features])[0]
                    # Assuming class 1 is phishing
                    confidence = proba[1] if prediction == 1 else proba[0]
                    confidence_percent = round(confidence * 100, 2)
                else:
                    confidence_percent = None

                # Advanced Features Analysis
                try:
                    api_key = os.environ.get('SAFE_BROWSING_API_KEY')
                    advanced_results = analyze_advanced_features(url_input, api_key)
                except Exception as e:
                    print(f"Advanced analysis failed: {e}")
                    advanced_results = {}

                # --- HYBRID SCORING LOGIC ---
                # Combined Risk Score (0-100)
                # Weighted Average:
                # - ML Probability: 50%
                # - Advanced Features: 50% (Age 20%, SSL 20%, Safe Browsing 10%)
                
                # Get ML Probability of Phishing (Class 1)
                ml_phishing_prob = 0
                if hasattr(model, "predict_proba"):
                    proba = model.predict_proba([features])[0]
                    ml_phishing_prob = proba[1] # Probability of being phishing
                else:
                    ml_phishing_prob = 1 if prediction == 1 else 0

                # Get Advanced Risks
                age_score = advanced_results.get('age_score', 0) # 0, 0.5, or 1
                ssl_score = advanced_results.get('ssl_score', 0) # 0 or 1
                sb_score = advanced_results.get('safe_browsing_score', 0) # 0 or 1

                # Calculate Hybrid Risk Score
                # Adjusted Weights to penalize SSL/Age more heavily
                # Weights: ML=0.3, Age=0.3, SSL=0.3, SB=0.1
                hybrid_score = (ml_phishing_prob * 0.3) + (age_score * 0.3) + (ssl_score * 0.3) + (sb_score * 0.1)
                
                # Override Logic:
                # If Safe Browsing says DANGEROUS -> Force Phishing
                # If SSL is Invalid -> High suspicion
                
                if sb_score == 1:
                    prediction_text = "DANGEROUS Website ⛔"
                    result_class = "danger"
                    confidence_percent = 100
                elif hybrid_score > 0.35: # Lowered threshold for suspicion
                    if prediction == 0 and hybrid_score > 0.6:
                         prediction_text = "Phishing Website ⚠️ (High Risk Factors)"
                         result_class = "danger"
                    elif prediction == 0:
                         prediction_text = "Suspicious Website ⚠️"
                         result_class = "danger" 
                    else:
                         prediction_text = "Phishing Website ⚠️"
                         result_class = "danger"
                    confidence_percent = round(hybrid_score * 100, 2)
                else:
                    if prediction == 1:
                        prediction_text = "Phishing Website ⚠️"
                        result_class = "danger"
                        confidence_percent = round(ml_phishing_prob * 100, 2)
                    else:
                        prediction_text = "Legitimate Website ✅"
                        result_class = "success"
                        confidence_percent = round((1 - hybrid_score) * 100, 2)
                
                return render_template('index.html', 
                                     prediction_text=prediction_text, 
                                     url=url_input, 
                                     result_class=result_class,
                                     confidence=confidence_percent,
                                     advanced_results=advanced_results)
            except Exception as e:
                error_message = f"Error processing URL: {str(e)}"
        else:
            error_message = "Model not loaded. Please contact administrator."

    return render_template('index.html', prediction_text=prediction_text, url=url_input, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
