import requests
import json


def is_valid_endpoint(url):
    if not url:
        return False
    url_lower = url.lower()
    return url_lower.startswith('http') and ('/api/' in url_lower or url_lower.endswith('.json'))


def fetch_api(url):
    try:
        response = requests.get(url, timeout=5)
        status = response.status_code
        
        try:
            data = response.json()
            data = json.dumps(data, sort_keys=True)
        except Exception:
            data = response.text[:500] if response.text else None
        
        return {
            "url": url,
            "status": status,
            "data": data
        }
    except Exception as e:
        return {
            "url": url,
            "status": 0,
            "data": None,
            "error": str(e)
        }


def execute_endpoints(endpoints):
    valid_endpoints = sorted([e for e in endpoints if is_valid_endpoint(e)])[:5]
    
    results = []
    for endpoint in valid_endpoints:
        result = fetch_api(endpoint)
        results.append(result)
    
    results = sorted(results, key=lambda x: x["url"])
    return results