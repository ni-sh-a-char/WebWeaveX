import re


def extract_code_blocks(html):
    code_blocks = []
    seen = set()
    
    patterns = [
        (r'<pre[^>]*>(.*?)</pre>', 'pre'),
        (r'<code[^>]*>(.*?)</code>', 'code'),
    ]
    
    for pattern, tag in patterns:
        for match in re.finditer(pattern, html, re.IGNORECASE | re.DOTALL):
            content = match.group(1)
            content = re.sub(r'<[^>]+>', '', content)
            content = content.strip()
            if content and content not in seen:
                code_blocks.append({"code": content[:1000], "language": "unknown"})
                seen.add(content)
    
    return code_blocks[:50]


def extract_clean_text(html):
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()[:5000]


def github_profile(html, data):
    files = []
    readme = ""
    description = ""
    code = extract_code_blocks(html)
    text = extract_clean_text(html)
    
    repo_match = re.search(r'<h1[^>]*>.*?([Aa-Za-z0-9_-]+/[Aa-Za-z0-9_-]+)', html)
    if repo_match:
        description = repo_match.group(1)
    
    file_patterns = [
        r'<a[^>]*href=["\'](/[^"\']+/blob/[^"\']+)["\'][^>]*>([^<]+)',
    ]
    for pattern in file_patterns:
        for match in re.finditer(pattern, html, re.IGNORECASE):
            filename = match.group(1) if match.lastindex else ""
            if filename and filename not in files:
                files.append(filename)
    
    readme_patterns = [r'<a[^>]*href=["\'](/[^"\']*README[^"\']*)["\']']
    for pattern in readme_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            readme = match.group(1)
    
    return {
        "type": "github",
        "content": {
            "text": text,
            "code": code,
            "structured": {
                "files": sorted(files)[:20]
            }
        },
        "metadata": {
            "repo": description,
            "readme": readme
        }
    }


def stackoverflow_profile(html, data):
    question = ""
    answers = []
    accepted = ""
    code = extract_code_blocks(html)
    text = extract_clean_text(html)
    
    q_pattern = r'<h1[^>]*>(.*?)</h1>'
    match = re.search(q_pattern, html, re.IGNORECASE | re.DOTALL)
    if match:
        question = match.group(1).strip()
    
    ans_pattern = r'<div[^>]*class=["\'][^"\']*answer[^"\']*["\'][^>]*>(.*?)</div>'
    for m in re.finditer(ans_pattern, html, re.IGNORECASE | re.DOTALL):
        answer_text = m.group(1)[:500]
        if answer_text:
            answers.append(answer_text)
    
    accepted_pattern = r'<div[^>]*class=["\'][^"\']*accepted[^"\']*["\'][^>]*>(.*?)</div>'
    match = re.search(accepted_pattern, html, re.IGNORECASE | re.DOTALL)
    if match:
        accepted = match.group(1)[:500]
    
    return {
        "type": "stackoverflow",
        "content": {
            "text": text,
            "code": code,
            "structured": {
                "question": question[:500],
                "answers": answers[:5],
                "accepted_answer": accepted
            }
        },
        "metadata": {}
    }


def blog_profile(html, data):
    title = data.get("title", "")
    headings = [h.get("text") for h in data.get("headings", [])]
    meta = data.get("meta_description", "")
    code = extract_code_blocks(html)
    text = extract_clean_text(html)
    
    paragraphs = []
    p_pattern = r'<p[^>]*>(.*?)</p>'
    for match in re.finditer(p_pattern, html, re.IGNORECASE | re.DOTALL):
        para = match.group(1)
        para = re.sub(r'<[^>]+>', '', para).strip()
        if para and len(para) > 50:
            paragraphs.append(para)
    
    return {
        "type": "blog",
        "content": {
            "text": text,
            "code": code,
            "structured": {
                "title": title,
                "headings": headings,
                "sections": paragraphs
            }
        },
        "metadata": {
            "description": meta
        }
    }


def generic_profile(html, data):
    code = extract_code_blocks(html)
    text = extract_clean_text(html)
    links = [l.get("url", "") for l in data.get("links", [])]
    
    return {
        "type": "generic",
        "content": {
            "text": text,
            "code": code,
            "structured": {
                "links": sorted(links)[:50]
            }
        },
        "metadata": {}
    }


def detect_page_type(url, detection, html, data):
    url_lower = url.lower()
    classification = detection.get("classification", {})
    page_type = classification.get("type", "static")
    
    if "github.com" in url_lower or "gitlab.com" in url_lower:
        return "github"
    
    if "stackoverflow.com" in url_lower or "stackexchange.com" in url_lower:
        return "stackoverflow"
    
    if page_type == "static" and data.get("headings"):
        if data.get("meta_description"):
            return "blog"
    
    return "generic"


def extract_profile(url, detection, html, data):
    page_type = detect_page_type(url, detection, html, data)
    
    if page_type == "github":
        return github_profile(html, data)
    elif page_type == "stackoverflow":
        return stackoverflow_profile(html, data)
    elif page_type == "blog":
        return blog_profile(html, data)
    else:
        return generic_profile(html, data)