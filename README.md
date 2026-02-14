# Phishing Website Detection System 🛡️

A Machine Learning-based system to detect phishing URLs using feature extraction and a Random Forest Classifier. This project includes a Flask web application with a modern UI for real-time URL analysis.

## Features
-   **URL Analysis**: Extracts features like length, IP presence, special characters, etc.
-   **Machine Learning**: Uses a trained Random Forest model (~96% accuracy).
-   **Real-time Checks**:
    -   **Domain Age**: Checks creation date via WHOIS (flags domains <30 days old).
    -   **SSL Certificate**: Verifies SSL validity and expiration.
    -   **Google Safe Browsing**: Checks against Google's blacklist (requires API Key).
-   **Web Interface**: Clean, responsive UI built with Flask and CSS.

## Prerequisites
-   Python 3.8+
-   pip (Python package manager)

## Installation

1.  **Clone/Download the repository** to your local machine.
2.  **Navigate to the project directory**:
    ```bash
    cd "path/to/project/folder"
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 1. Train the Model (Optional)
The project comes with a pre-trained model (`model/phishing_model.pkl`). If you need to retrain it:
```bash
python model/train_model.py
```

### 2. Set Up Environment Variables (Optional)
To enable Google Safe Browsing checks, set your API key:
-   **Windows (PowerShell)**:
    ```powershell
    $env:SAFE_BROWSING_API_KEY="your_api_key_here"
    ```
-   **Linux/Mac**:
    ```bash
    export SAFE_BROWSING_API_KEY="your_api_key_here"
    ```

### 3. Run the Application
Start the Flask server:
```bash
python app.py
```

### 4. Access the Interface
Open your web browser and go to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

## Deployment (Antigravity)
1.  Create an application on Antigravity.
2.  Upload all project files.
3.  Set the **Build Command** (if applicable) to install requirements.
4.  Set the **Start Command** to `python app.py`.
5.  Add `SAFE_BROWSING_API_KEY` to the environment variables.

## Project Structure
-   `app.py`: Main Flask application.
-   `model/`: Contains ML scripts and the trained model.
-   `static/`: CSS and other static assets.
-   `templates/`: HTML templates.
-   `requirements.txt`: Python dependencies.
