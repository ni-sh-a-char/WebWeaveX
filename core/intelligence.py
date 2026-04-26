import re


def analyze_content(html, data):
    signals = []
    
    content_density = len(html)
    has_scripts = bool(re.search(r'<script', html, re.IGNORECASE))
    link_count = len(data.get("links", []))
    
    code_blocks = data.get("code_blocks", [])
    embedded_json = data.get("embedded_json", [])
    
    return {
        "content_density": content_density,
        "has_scripts": has_scripts,
        "link_count": link_count,
        "code_block_count": len(code_blocks),
        "has_embedded_json": len(embedded_json) > 0,
        "signals": signals
    }


def classify_page(analysis):
    score = 0.0
    
    if analysis.get("has_scripts"):
        score += 0.3
    
    if analysis.get("has_embedded_json"):
        score += 0.3
    
    if analysis.get("link_count") < 2:
        score += 0.2
    
    if analysis.get("code_block_count") > 5:
        score += 0.2
    
    if analysis.get("content_density") < 500:
        score += 0.1
    
    page_type = "static"
    if score >= 0.7:
        page_type = "dynamic"
    elif score >= 0.4:
        page_type = "partial"
    
    confidence = max(0.0, min(1.0, 1.0 - score))
    
    return {
        "type": page_type,
        "confidence": confidence,
        "score": score
    }


def ai_analyze(html, url):
    from .config import CONFIG
    
    provider = CONFIG.get("provider")
    if not provider:
        return None
    
    prompt = f"Is the page at {url} static, partial, or dynamic? Return JSON with 'type' and 'confidence'."
    
    try:
        result = provider.generate(prompt)
        text = result.get("text", "")
        if "dynamic" in text.lower():
            return {"type": "dynamic", "confidence": 0.8}
        elif "partial" in text.lower():
            return {"type": "partial", "confidence": 0.6}
        return {"type": "static", "confidence": 0.8}
    except Exception:
        return None