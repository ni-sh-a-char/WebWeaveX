import re
from urllib.parse import urljoin


def clean_html(html):
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    html = html.replace('&amp;', '&')
    html = html.replace('&lt;', '<')
    html = html.replace('&gt;', '>')
    html = html.replace('&quot;', '"')
    html = html.replace('&#39;', "'")
    html = html.replace('&nbsp;', ' ')
    html = re.sub(r'\s+', ' ', html)
    return html


def extract_title(html):
    match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    if match:
        text = match.group(1)
        text = re.sub(r'<[^>]+>', '', text)
        return text.strip()
    return None


def extract_meta_description(html):
    match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']', html, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def extract_headings(html):
    headings = []
    seen = set()
    for tag in ['h1', 'h2', 'h3']:
        pattern = rf'<{tag}[^>]*>(.*?)</{tag}>'
        for match in re.finditer(pattern, html, re.IGNORECASE | re.DOTALL):
            text = match.group(1)
            text = re.sub(r'<[^>]+>', '', text)
            text = text.strip()
            if text and text not in seen:
                headings.append({"tag": tag.upper(), "text": text})
                seen.add(text)
    return sorted(headings, key=lambda x: x["text"])


def extract_links(html, base_url):
    links = []
    seen = set()
    
    anchor_pattern = r'<a[^>]*href=["\'](.*?)["\'][^>]*>(.*?)</a>'
    for match in re.finditer(anchor_pattern, html, re.IGNORECASE | re.DOTALL):
        raw_link = match.group(1).strip()
        anchor_text = match.group(2).strip()
        anchor_text = re.sub(r'<[^>]+>', '', anchor_text)
        anchor_text = re.sub(r'\s+', ' ', anchor_text).strip()
        
        if not raw_link or raw_link.startswith('#') or raw_link.startswith('javascript:'):
            continue
        
        if raw_link.startswith("http"):
            resolved = raw_link
            link_type = "absolute"
        else:
            resolved = urljoin(base_url, raw_link)
            link_type = "relative"
        
        if resolved not in seen:
            links.append({"url": resolved, "type": link_type, "text": anchor_text})
            seen.add(resolved)
    
    simple_pattern = r'href=["\'](.*?)["\']'
    for match in re.finditer(simple_pattern, html, re.IGNORECASE):
        raw_link = match.group(1).strip()
        
        if not raw_link or raw_link.startswith('#') or raw_link.startswith('javascript:'):
            continue
        
        if raw_link.startswith("http"):
            resolved = raw_link
        else:
            resolved = urljoin(base_url, raw_link)
        
        if resolved not in seen:
            links.append({"url": resolved, "type": "absolute" if raw_link.startswith("http") else "relative", "text": ""})
            seen.add(resolved)
    
    return sorted(links, key=lambda x: x["url"])


def extract_code_blocks(html):
    code_blocks = []
    seen = set()
    
    patterns = [
        (r'<pre[^>]*>(.*?)</pre>', 'pre'),
        (r'<code[^>]*>(.*?)</code>', 'code'),
    ]
    
    for pattern, block_type in patterns:
        for match in re.finditer(pattern, html, re.IGNORECASE | re.DOTALL):
            content = match.group(1)
            content = re.sub(r'<[^>]+>', '', content)
            content = content.strip()
            if content and content not in seen:
                code_blocks.append({"type": block_type, "content": content})
                seen.add(content)
    
    return sorted(code_blocks, key=lambda x: x["content"])


def extract_embedded_json(html):
    json_data = []
    seen = set()
    
    patterns = [
        r'window\.__NEXT_DATA__\s*=\s*(\{.*?\});',
        r'window\.__DATA__\s*=\s*(\{.*?\});',
    ]
    
    for pattern in patterns:
        for match in re.finditer(pattern, html, re.DOTALL):
            content = match.group(0).strip()[:1000]
            if content and content not in seen:
                var_name = "__NEXT_DATA__" if "NEXT" in pattern else "__DATA__"
                json_data.append({"variable": var_name, "content": content})
                seen.add(content)
    
    return sorted(json_data, key=lambda x: x["content"])


def extract_all(html, base_url):
    cleaned = clean_html(html)
    return {
        "title": extract_title(cleaned),
        "meta_description": extract_meta_description(cleaned),
        "headings": extract_headings(cleaned),
        "links": extract_links(cleaned, base_url),
        "code_blocks": extract_code_blocks(cleaned),
        "embedded_json": extract_embedded_json(cleaned)
    }