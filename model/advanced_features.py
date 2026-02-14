import whois
import datetime
import ssl
import socket
from urllib.parse import urlparse

def get_domain_age(domain_name):
    try:
        w = whois.whois(domain_name)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        
        if creation_date:
            today = datetime.datetime.now()
            age = (today - creation_date).days
            return age
        return -1
    except Exception as e:
        # print(f"Whois Error: {e}")
        return -1

def check_ssl_validity(domain_name):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain_name, 443), timeout=3) as sock:
            with context.wrap_socket(sock, server_hostname=domain_name) as ssock:
                cert = ssock.getpeercert()
                expiry_date_str = cert['notAfter']
                # Convert date format if needed, but just checking connection success implies basic validity
                # Example format: 'May 16 23:59:59 2024 GMT'
                expiry_date = datetime.datetime.strptime(expiry_date_str, '%b %d %H:%M:%S %Y %GMT')
                
                if expiry_date > datetime.datetime.now():
                    return True, expiry_date
                else:
                    return False, expiry_date
    except Exception as e:
        # print(f"SSL Error: {e}")
        return False, None

import requests
import json
import os

def check_google_safe_browsing(url, api_key):
    if not api_key:
        return "Skipped (No API Key)", 0
    
    sb_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    payload = {
        "client": {
            "clientId": "phishguard-app",
            "clientVersion": "1.0.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }
    
    try:
        response = requests.post(sb_url, json=payload)
        if response.status_code == 200:
            result = response.json()
            if "matches" in result:
                return "DANGEROUS (Google Blacklist)", 1
            else:
                return "Safe (Google Clean)", 0
        else:
            return f"Error (API: {response.status_code})", 0
    except Exception as e:
        return f"Error ({str(e)})", 0

def analyze_advanced_features(url, api_key=None):
    results = {}
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc
    
    if not domain_name:
         # Handle case where URL might not have scheme
         domain_name = url.split('/')[0]

    # Clean domain (remove www.)
    if domain_name.startswith('www.'):
        domain_name = domain_name[4:]

    # Domain Age
    age = get_domain_age(domain_name)
    results['domain_age_days'] = age
    
    # Heuristic: Domains < 30 days old are suspicious
    if age != -1 and age < 30:
        results['age_risk'] = "High (New Domain)"
        results['age_score'] = 1  # 1 means suspicious
    elif age == -1:
        results['age_risk'] = "Unknown (Whois Hidden/Error)"
        results['age_score'] = 0.5 # Neutral/Suspicious
    else:
        results['age_risk'] = "Low (Established Domain)"
        results['age_score'] = 0 # Safe

    # SSL Check
    is_valid, expiry = check_ssl_validity(domain_name)
    results['ssl_valid'] = is_valid
    results['ssl_expiry'] = str(expiry) if expiry else "N/A"
    
    if not is_valid:
        results['ssl_risk'] = "High (No Valid SSL)"
        results['ssl_score'] = 1
    else:
        results['ssl_risk'] = "Low (Valid SSL)"
        results['ssl_score'] = 0

    # Google Safe Browsing
    sb_status, sb_score = check_google_safe_browsing(url, api_key)
    results['safe_browsing_status'] = sb_status
    results['safe_browsing_score'] = sb_score

    return results
