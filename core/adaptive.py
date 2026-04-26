import re
import copy
from urllib.parse import urljoin
from .api_engine import execute_endpoints
from .config import CONFIG


def extract_scripts(html):
    raw_scripts = []
    pattern = r'<script[^>]*>(.*?)</script>'
    for match in re.finditer(pattern, html, re.IGNORECASE | re.DOTALL):
        content = match.group(1).strip()
        if content:
            raw_scripts.append(content[:500])
    unique_scripts = sorted(set(raw_scripts))
    return [{"content": s} for s in unique_scripts]


def find_api_endpoints(html, base_url):
    endpoints = set()
    patterns = [
        r'["\']([^"\']*/api/[^"\']*)["\']',
        r'["\']([^"\']*\.json)["\']',
        r'fetch\s*\(\s*["\']([^"\']+)["\']',
        r'axios\.\w+\s*\(\s*["\']([^"\']+)["\']',
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, html, re.IGNORECASE):
            url = match.group(1)
            if url:
                full_url = urljoin(base_url, url)
                endpoints.add(full_url)
    return sorted(list(endpoints))[:10]


def adaptive_extract(url, html, extracted_data, detection):
    if not CONFIG.get("enable_adaptive", True):
        return {"strategy": "disabled", "data": extracted_data}
    
    classification = detection.get("classification", {})
    analysis = detection.get("analysis", {})
    
    page_type = classification.get("type", "static")
    confidence = classification.get("confidence", 1.0)
    
    extractable = detection.get("extractable", "full")
    
    if page_type == "static" and confidence > 0.7:
        return {
            "strategy": "standard",
            "data": extracted_data,
            "intelligence_used": True
        }
    
    if confidence < 0.5:
        page_type = "partial"
    
    if page_type == "partial":
        scripts = extract_scripts(html)
        api_endpoints = find_api_endpoints(html, url)
        
        merged_data = copy.deepcopy(extracted_data)
        merged_data["scripts"] = scripts
        merged_data["api_endpoints"] = api_endpoints
        
        return {
            "strategy": "enhanced",
            "data": merged_data,
            "intelligence_used": True
        }
    
    scripts = extract_scripts(html)
    api_endpoints = find_api_endpoints(html, url)
    
    if CONFIG.get("enable_api_execution", True):
        api_results = execute_endpoints(api_endpoints)
    else:
        api_results = []
    
    return {
        "strategy": "api_execution",
        "data": api_results,
        "endpoints": api_endpoints,
        "scripts": scripts,
        "intelligence_used": True
    }