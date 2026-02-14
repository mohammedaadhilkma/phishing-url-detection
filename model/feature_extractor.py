import re
from urllib.parse import urlparse

def extract_features(url):
    features = []

    # 1. URL Length
    features.append(len(url))

    # 2. Has IP address
    # Checks for IPv4 address pattern
    ip_pattern = r'(\d{1,3}\.){3}\d{1,3}'
    features.append(1 if re.search(ip_pattern, url) else 0)

    # 3. Count dots
    features.append(url.count('.'))

    # 4. Has @ symbol
    features.append(1 if '@' in url else 0)

    # 5. Has - symbol (dash)
    features.append(1 if '-' in url else 0)

    # 6. Uses HTTPS
    parsed_url = urlparse(url)
    features.append(1 if parsed_url.scheme == 'https' else 0)

    # 7. Number of subdomains
    # Heuristic: count dots in netloc, subtract 1 (e.g. www.google.com -> 2 dots -> 1 subdomain? or just use dot count)
    # Better: split netloc by dots. Length > 2 implies subdomains.
    try:
        domain_parts = parsed_url.netloc.split('.')
        # If www is present, ignore it? Or count it? Let's just count parts > 2 as subdomains essentially.
        # Actually, let's stick to total dots in URL for simplicity as per requirement 3, but prompt asked for "Number of subdomains" separately.
        # Let's count dots in hostname specifically for subdomain estimation.
        features.append(len(domain_parts) - 2 if len(domain_parts) > 2 else 0)
    except:
        features.append(0)

    # 8. Suspicious words
    suspicious_keywords = ['login', 'verify', 'account', 'update', 'banking', 'secure', 'ebay', 'paypal']
    count_suspicious = sum(1 for word in suspicious_keywords if word in url.lower())
    features.append(count_suspicious)

    return features
