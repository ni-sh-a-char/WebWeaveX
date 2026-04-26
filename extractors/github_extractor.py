import re

from core.extractor_engine import BaseExtractor


class GitHubExtractor(BaseExtractor):
    priority = 100
    
    def can_handle(self, url, html, metadata):
        if not url:
            return False
        try:
            domain = url.split("/")[2].lower()
        except:
            return False
        return domain == "github.com" or domain.endswith(".github.com")
    
    def extract(self, url, html, metadata):
        if not html:
            return None
        
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else ""
        
        code_blocks = re.findall(r'<pre.*?><code.*?>(.*?)</code></pre>', html, re.DOTALL)
        
        readme_match = re.findall(r'<article.*?>(.*?)</article>', html, re.DOTALL)
        readme_text = ""
        if readme_match:
            readme_text = re.sub(r'<[^>]+>', ' ', readme_match[0])
            readme_text = re.sub(r'\s+', ' ', readme_text).strip()
        
        languages = set()
        for code in code_blocks:
            if "def " in code:
                languages.add("python")
            elif "function" in code:
                languages.add("javascript")
            elif "class " in code:
                languages.add("general")
        
        return {
            "type": "github",
            "text": readme_text[:3000],
            "code": code_blocks[:20],
            "structured": {
                "title": title,
                "languages": sorted(list(languages)),
                "code_blocks_count": len(code_blocks)
            },
            "metadata": {
                "confidence": 0.9,
                "source": "github_extractor"
            }
        }