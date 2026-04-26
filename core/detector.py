import re
from .intelligence import analyze_content, classify_page, ai_analyze


def detect_page(html, extracted_data, url=""):
    analysis = analyze_content(html, extracted_data)
    classification = classify_page(analysis)
    
    ai_result = None
    if url:
        ai_result = ai_analyze(html, url)
    
    if ai_result:
        classification = ai_result
        intelligence_level = "ai_augmented"
    else:
        intelligence_level = "rule_based"
    
    signals = []
    
    if html and len(html) < 500:
        signals.append({"signal": "low_content", "score": 0.2})
    
    script_count = len(re.findall(r'<script', html, re.IGNORECASE))
    if script_count > 10:
        signals.append({"signal": "heavy_script", "score": 0.3, "count": script_count})
    
    framework_patterns = [
        r'__NEXT_DATA__',
        r'window\.__DATA__',
        r'react',
        r'angular',
        r'vue',
    ]
    
    for pattern in framework_patterns:
        if re.search(pattern, html, re.IGNORECASE):
            signals.append({"signal": "framework_detected", "pattern": pattern, "score": 0.3})
    
    api_patterns = [
        r'fetch\s*\(',
        r'axios',
        r'XMLHttpRequest',
    ]
    
    for pattern in api_patterns:
        if re.search(pattern, html, re.IGNORECASE):
            signals.append({"signal": "api_detected", "pattern": pattern, "score": 0.3})
    
    headings = extracted_data.get("headings", [])
    text_content = extracted_data.get("title") or extracted_data.get("meta_description")
    
    if not headings and not text_content:
        signals.append({"signal": "empty_body", "score": 0.2})
    
    extractable = classification.get("type", "static")
    if extractable == "static":
        extractable = "full"
    elif extractable == "partial":
        extractable = "partial"
    else:
        extractable = "dynamic"
    
    confidence = classification.get("confidence", 1.0)
    
    return {
        "extractable": extractable,
        "confidence": confidence,
        "analysis": analysis,
        "classification": classification,
        "signals": signals[:5],
        "intelligence_level": intelligence_level
    }