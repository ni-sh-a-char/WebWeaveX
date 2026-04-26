import re

from core.extractor_engine import BaseExtractor


class StackOverflowExtractor(BaseExtractor):
    priority = 200
    
    def can_handle(self, url, html, metadata):
        if not url:
            return False
        try:
            domain = url.split("/")[2].lower()
        except:
            return False
        return domain == "stackoverflow.com" or domain.endswith(".stackoverflow.com")
    
    def extract(self, url, html, metadata):
        if not html:
            return None
        
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else ""
        
        question_match = re.findall(r'<div class="s-prose js-post-body".*?>(.*?)</div>', html, re.DOTALL)
        question_text = ""
        if question_match:
            question_text = re.sub(r'<[^>]+>', ' ', question_match[0])
            question_text = re.sub(r'\s+', ' ', question_text).strip()
        
        answers = re.findall(r'<div class="answer".*?>(.*?)</div>', html, re.DOTALL)
        
        answer_texts = []
        for ans in answers[:3]:
            cleaned = re.sub(r'<[^>]+>', ' ', ans)
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
            answer_texts.append(cleaned[:1000])
        
        code_blocks = re.findall(r'<pre><code>(.*?)</code></pre>', html, re.DOTALL)
        
        return {
            "type": "stackoverflow",
            "text": question_text[:2000],
            "code": code_blocks[:20],
            "structured": {
                "title": title,
                "answers": answer_texts,
                "answer_count": len(answers)
            },
            "metadata": {
                "confidence": 0.85,
                "source": "stackoverflow_extractor"
            }
        }