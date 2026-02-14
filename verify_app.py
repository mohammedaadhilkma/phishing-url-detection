import requests
import sys

try:
    # Test GET
    response = requests.get('http://127.0.0.1:5000')
    if response.status_code == 200:
        print("GET / passed.")
    else:
        print(f"GET / failed: {response.status_code}")

    # Test POST
    payload = {'url': 'http://google.com'}
    response = requests.post('http://127.0.0.1:5000', data=payload)
    if response.status_code == 200:
        print("POST / passed.")
        if "Google Safe Browsing" in response.text:
             print("Content check passed (Safe Browsing present).")
        else:
             print("Warning: Content check failed (Safe Browsing missing).")
             # print(response.text) # Uncomment to debug
    else:
        print(f"POST / failed: {response.status_code}")
        print(response.text) # Print error to see traceback
except Exception as e:
    print(f"Error connecting to application: {e}")
