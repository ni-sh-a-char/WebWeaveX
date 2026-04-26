import re


class BaseExtractor:
    priority = 0
    
    def can_handle(self, url, html, metadata):
        raise NotImplementedError
    
    def extract(self, url, html, metadata):
        raise NotImplementedError


class ExtractionEngine:
    def __init__(self):
        self.extractors = []
    
    def register(self, extractor):
        self.extractors.append(extractor)
        self.extractors.sort(key=lambda x: getattr(x, "priority", 0), reverse=True)
    
    def extract(self, url, html, metadata):
        for ext in self.extractors:
            try:
                if ext.can_handle(url, html, metadata):
                    result = ext.extract(url, html, metadata)
                    if result:
                        return self._normalize_output(url, result)
            except Exception:
                continue
        
        return self._fallback_extract(url, html)
    
    def _fallback_extract(self, url, html):
        text = html[:5000] if html else ""
        
        return {
            "url": url,
            "type": "generic",
            "content": {
                "text": text,
                "code": [],
                "structured": {}
            },
            "metadata": {
                "confidence": 0.1,
                "source": "fallback"
            }
        }
    
    def _normalize_output(self, url, result):
        return {
            "url": url,
            "type": result.get("type", "unknown"),
            "content": {
                "text": result.get("text", "") or "",
                "code": result.get("code", []) or [],
                "structured": result.get("structured", {}) or {}
            },
            "metadata": result.get("metadata", {}) or {}
        }