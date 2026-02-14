import requests
import os

URL = "https://raw.githubusercontent.com/elaaatif/DATA-MINING-PhiUSIIL-Phishing-URL/main/PhiUSIIL_Phishing_URL_Dataset.csv"
OUTPUT_FILE = "dataset.csv"

def download_data():
    if os.path.exists(OUTPUT_FILE):
        print(f"{OUTPUT_FILE} already exists.")
        return

    print(f"Downloading dataset from {URL}...")
    try:
        response = requests.get(URL)
        response.raise_for_status()
        with open(OUTPUT_FILE, 'wb') as f:
            f.write(response.content)
        print("Download complete.")
    except Exception as e:
        print(f"Error downloading dataset: {e}")

if __name__ == "__main__":
    download_data()
