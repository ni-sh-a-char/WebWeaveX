import re

from core.extractor_engine import BaseExtractor


class GenericHTMLExtractor(BaseExtractor):
    priority = -100
    
    def can_handle(self, url, html, metadata):
        return True
    
    def extract(self, url, html, metadata):
        if not html:
            return None
        
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text).strip()
        
        code_blocks = re.findall(r'<code.*?>(.*?)</code>', html, re.DOTALL)
        
        return {
            "type": "generic_html",
            "text": text[:3000],
            "code": code_blocks[:20],
            "structured": {},
            "metadata": {
                "confidence": 0.3,
                "source": "generic_extractor"
            }
        }