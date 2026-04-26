import re
from collections import Counter


def normalize_text(text):
    if not text:
        return ""
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.lower().strip()
    return text


def extract_entities(text):
    if not text:
        return []
    
    entities = []
    seen = set()
    
    url_pattern = r'https?://[^\s]+'
    for match in re.finditer(url_pattern, text):
        url = match.group(0)[:100]
        if url and url not in seen:
            entities.append({"type": "url", "value": url})
            seen.add(url)
    
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    for match in re.finditer(email_pattern, text):
        email = match.group(0)
        if email and email not in seen:
            entities.append({"type": "email", "value": email})
            seen.add(email)
    
    file_pattern = r'[a-zA-Z0-9_-]+\.(py|js|json|html|css|txt|md|yml|yaml|xml|csv|sql)'
    for match in re.finditer(file_pattern, text):
        filename = match.group(0)
        if filename and filename not in seen:
            entities.append({"type": "file", "value": filename})
            seen.add(filename)
    
    words = re.findall(r'\b[a-zA-Z]{5,}\b', text.lower())
    valid_words = []
    for w in words:
        if not w.isalpha():
            continue
        if len(set(w)) < 3:
            continue
        valid_words.append(w)
    
    keyword_counts = Counter(valid_words).most_common(10)
    for kw, _ in keyword_counts:
        if kw not in seen:
            entities.append({"type": "keyword", "value": kw})
            seen.add(kw)
    
    return sorted(entities, key=lambda x: x["value"])


def extract_topics(text):
    if not text:
        return []
    
    normalized = normalize_text(text)
    words = normalized.split()
    stopwords = {'about', 'after', 'again', 'being', 'below', 'could', 'couldn', 'didn', 'doing', 'down', 'during', 'each', 'first', 'found', 'from', 'further', 'had', 'has', 'have', 'having', 'here', 'hers', 'herself', 'himself', 'his', 'how', 'however', 'into', 'just', 'more', 'most', 'much', 'mustn', 'needn', 'never', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'should', 'shouldn', 'since', 'some', 'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'wasn', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'won', 'would', 'you', 'your', 'example', 'domain', 'domainexample', 'domainthis'}
    filtered = [w for w in words if w not in stopwords and len(w) >= 5 and w.isalpha()]
    counts = Counter(filtered)
    filtered_counts = {k: v for k, v in counts.items() if v >= 2}
    return sorted(filtered_counts.keys(), key=lambda x: filtered_counts[x], reverse=True)[:10]


def generate_insights(unified):
    insights = []
    
    text = unified.get("text", "")
    code = unified.get("code", [])
    structured = unified.get("structured", {})
    links = structured.get("links", []) if isinstance(structured, dict) else []
    
    if code and len(code) > 0:
        insights.append("Page contains code examples")
    
    if len(links) > 10:
        insights.append("Page is highly connected with many links")
    elif len(links) > 5:
        insights.append("Page has moderate link density")
    
    if text and len(text) > 2000:
        insights.append("Detailed content page with substantial text")
    elif text and len(text) > 500:
        insights.append("Page has moderate content length")
    
    if isinstance(structured, dict):
        if structured.get("headings"):
            insights.append("Page uses structured headings")
        if structured.get("sections"):
            insights.append("Page has multiple content sections")
    
    if not insights:
        insights.append("Standard web page")
    
    return insights


def analyze_code(code_blocks):
    if not code_blocks:
        return {"count": 0, "languages_detected": [], "complexity": "low"}
    
    count = len(code_blocks)
    total_length = sum(len(b.get("code", "")) for b in code_blocks)
    avg_length = total_length / count if count > 0 else 0
    
    languages = set()
    for block in code_blocks:
        code = block.get("code", "").lower()
        if "def " in code or "import " in code or "class " in code:
            languages.add("python")
        if "function " in code or "const " in code or "let " in code or "var " in code:
            languages.add("javascript")
        if "public " in code or "private " in code or "class " in code:
            languages.add("java")
        if "fn " in code or "let mut" in code or "impl " in code:
            languages.add("rust")
        if "#include" in code or "int main" in code:
            languages.add("c")
    
    if avg_length > 500:
        complexity = "high"
    elif avg_length > 200:
        complexity = "medium"
    else:
        complexity = "low"
    
    return {
        "count": count,
        "languages_detected": sorted(list(languages)),
        "complexity": complexity
    }


def extract_relationships(text):
    if not text:
        return []
    
    normalized = normalize_text(text)
    words = normalized.split()
    stopwords = {'about', 'after', 'again', 'being', 'below', 'could', 'didn', 'doing', 'down', 'during', 'each', 'first', 'found', 'from', 'further', 'had', 'has', 'have', 'having', 'here', 'hers', 'herself', 'himself', 'his', 'how', 'however', 'into', 'just', 'more', 'most', 'much', 'mustn', 'needn', 'never', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'should', 'shouldn', 'since', 'some', 'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'wasn', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'won', 'would', 'you', 'your'}
    filtered = [w for w in words if w not in stopwords and len(w) >= 5 and w.isalpha()]
    counts = Counter(filtered)
    
    relationships = []
    for word, count in counts.items():
        if count >= 3:
            relationships.append({
                "type": "strong_topic",
                "value": word,
                "frequency": count
            })
    
    return sorted(relationships, key=lambda x: -x["frequency"])[:10]


def build_knowledge(unified):
    text = unified.get("text", "") or ""
    code = unified.get("code", []) or []
    
    entities = extract_entities(text)
    topics = extract_topics(text)
    insights = generate_insights(unified)
    code_intel = analyze_code(code)
    relationships = extract_relationships(text)
    
    if topics:
        insights.append(f"Primary topics detected: {', '.join(topics[:3])}")
    
    if len(entities) > 10:
        insights.append("Entity-rich page")
    
    if code_intel.get("complexity") == "high":
        insights.append("Technically complex page with substantial code")
    
    return {
        "entities": entities[:50],
        "topics": topics,
        "insights": insights,
        "code_intelligence": code_intel,
        "relationships": relationships
    }