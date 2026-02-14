import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import sys

# Add current directory to path to import feature_extractor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.feature_extractor import extract_features

# Configuration
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'dataset.csv')
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'phishing_model.pkl')

def train():
    print("Loading dataset...")
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        print(f"Error: Dataset not found at {DATA_PATH}")
        return

    # Basic cleanup
    df.dropna(subset=['URL', 'label'], inplace=True)
    
    # Extract features
    print("Extracting features from URLs... This might take a moment.")
    # For performance, maybe limit to a subset if dataset is huge, but let's try full first or sample if too slow.
    # The dataset has ~235k rows. Feature extraction in Python loop might be slow.
    # Let's use a sample of 10000 for quick training/demo purposes if it's too large, but 200k is manageable.
    # Let's verify dataset size first.
    
    # Check if dataset is huge
    if len(df) > 50000:
        print(f"Dataset is large ({len(df)} rows). Sampling 20,000 rows for faster training demo.")
        df = df.sample(20000, random_state=42)
    
    X = np.array([extract_features(url) for url in df['URL']])
    y = df['label'].values

    # Train/Test Split
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model Initialization
    print("Training Random Forest Model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluation
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save Model
    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(model, MODEL_PATH)
    print("Done!")

if __name__ == "__main__":
    train()
