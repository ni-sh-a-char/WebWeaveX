from .config import CONFIG


def is_ai_available():
    return CONFIG.get("ai_enabled") and CONFIG.get("provider") is not None


def ai_extract(html, url):
    provider = CONFIG.get("provider")
    
    if not provider:
        return None
    
    try:
        prompt = f"Extract structured data from {url}"
        result = provider.generate(prompt)
        
        if not isinstance(result, dict):
            return None
        
        text = result.get("text", "")
        
        return {
            "summary": text[:500],
            "important_data": [],
            "code_snippets": [],
            "inferred_links": []
        }
    except Exception:
        return None


def augment_with_ai(adaptive_result, html, url, detection):
    new_result = dict(adaptive_result)
    
    if not is_ai_available():
        return new_result
    
    strategy = new_result.get("strategy", "")
    data = new_result.get("data", [])
    
    if isinstance(data, dict):
        weak_links = len(data.get("links", [])) < 2
    else:
        weak_links = True
    
    trigger = (
        (strategy == "api_execution" and not data)
        or (strategy == "enhanced" and weak_links)
        or detection.get("confidence", 1.0) < 0.6
    )
    
    if trigger:
        ai_data = ai_extract(html, url)
        if ai_data:
            new_result["ai_data"] = ai_data
            new_result["strategy"] = "ai_augmented"
    
    return new_result