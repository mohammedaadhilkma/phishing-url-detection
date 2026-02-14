import requests

url = "http://127.0.0.1:5000"
test_url = "www.google./p.comm/ksj"

try:
    print(f"Testing URL: {test_url}")
    response = requests.post(url, data={'url': test_url})
    
    if response.status_code == 200:
        content = response.text
        if "Legitimate Website" in content:
            print("❌ Result: Legitimate Website (False Negative persists)")
        elif "Phishing Website" in content or "Suspicious Website" in content or "DANGEROUS" in content:
            print("✅ Result: Phishing/Suspicious/Dangerous (Fix Successful)")
            # Extract confidence if possible (simple string check)
            # print(content) 
        else:
             print("❓ Result: Unknown status")
    else:
        print(f"Error: {response.status_code}")

except Exception as e:
    print(f"Connection failed: {e}")
