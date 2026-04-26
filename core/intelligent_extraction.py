import re


STOPWORDS = {"this", "that", "with", "from", "have", "your", "about", "there", "will", "just", "only", "when", "what", "which", "their", "also", "been", "were", "they", "them", "than", "then", "some", "into", "more", "most", "such", "out", "here", "did", "do", "does", "doing", "done", "very", "just", "like", "over", "could", "would", "should", "may", "must", "need", "make", "made"}


TECH_KEYWORDS = {
    "python", "javascript", "java", "typescript", "go", "rust", "c++", "csharp",
    "api", "rest", "graphql", "http", "https", "endpoint",
    "database", "sql", "nosql", "mysql", "postgresql", "mongodb", "redis",
    "docker", "kubernetes", "container", "k8s", "pod",
    "machine", "learning", "ml", "ai", "neural", "model", "training", "inference",
    "deep", "tensorflow", "pytorch", "keras", "scikit",
    "frontend", "backend", "fullstack", "server", "client",
    "web", "http", "html", "css", "react", "vue", "angular",
    "json", "xml", "csv", "yaml", "toml", "config",
    "authentication", "oauth", "jwt", "token", "security",
    "cloud", "aws", "azure", "gcp", "serverless",
    "devops", "ci", "cd", "pipeline", "jenkins", "github",
    "testing", "unit", "integration", "mock", "stub",
    "async", "promise", "await", "thread", "parallel",
    "microservice", "monolith", "architecture", "design",
    "pattern", "singleton", "factory", "observer"
}


CAPABILITY_PATTERNS = {
    "web_scraping": ["scrape", "crawl", "extract", "fetch", "parse", "parser"],
    "api_usage": ["api", "endpoint", "request", "response", "http", "rest", "graphql"],
    "machine_learning": ["model", "train", "predict", "inference", "neural", "deep", "tensorflow", "pytorch"],
    "web_dev": ["frontend", "backend", "server", "client", "html", "css", "react", "vue"],
    "data_processing": ["json", "xml", "csv", "pipeline", "etl", "transform"],
    "database": ["sql", "query", "database", "mongodb", "postgresql", "mysql", "redis"],
    "authentication": ["auth", "oauth", "jwt", "token", "login", "session"],
    "devops": ["docker", "kubernetes", "ci", "cd", "deploy", "pipeline"],
    "testing": ["test", "mock", "stub", "unittest", "jest", "pytest"],
    "async_programming": ["async", "await", "promise", "thread", "parallel", "concurrent"]
}


def build_intelligence(content, context):
    if not content:
        content = {}
    
    text = content.get("text") or ""
    code_blocks = content.get("code") or []
    structured = content.get("structured") or {}
    
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    filtered = [w for w in words if w not in STOPWORDS]
    
    freq = {}
    for w in filtered:
        freq[w] = freq.get(w, 0) + 1
    
    topics = sorted(freq.keys(), key=lambda x: (-freq.get(x, 0), x))[:5]
    
    urls = re.findall(r'https?://[^\s,\)\">]+', text)
    emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    file_pattern = r'\b([a-zA-Z0-9_./-]+\.(?:py|js|ts|json|yaml|yml|md|txt|css|html|xml|sql|sh|go|rs|java|cpp|c|h|kt))\b'
    files = sorted(set(re.findall(file_pattern, text)))
    
    entities = sorted(set(urls + emails + files))
    
    text_split_lower = set(text.lower().split())
    concepts = sorted(text_split_lower & TECH_KEYWORDS)
    
    capabilities = []
    text_lower = text.lower()
    for cap, patterns in sorted(CAPABILITY_PATTERNS.items()):
        for pat in patterns:
            if pat in text_lower:
                capabilities.append(cap)
                break
    capabilities = sorted(set(capabilities))
    
    relations = []
    concepts_in_text = text_split_lower & TECH_KEYWORDS
    for cap in capabilities:
        for concept in sorted(concepts_in_text):
            relations.append((cap, "related_to", concept))
    relations = sorted(relations, key=lambda x: (x[0], x[2]))[:10]
    
    languages = set()
    functions = 0
    classes = 0
    
    for code in code_blocks:
        code_str = str(code) if code else ""
        if "def " in code_str:
            languages.add("python")
            functions += code_str.count("def ")
        if "function" in code_str:
            languages.add("javascript")
            functions += code_str.count("function")
        if "class " in code_str:
            classes += code_str.count("class ")
    
    code_insights = {
        "total_blocks": len(code_blocks) if code_blocks else 0,
        "languages": sorted(list(languages)),
        "functions": functions,
        "classes": classes
    }
    
    if code_blocks:
        content_type = "code"
    elif structured:
        content_type = "structured"
    elif len(text) > 1000:
        content_type = "article"
    else:
        content_type = "short_text"
    
    score = 0
    score += min(len(text) / 1000, 1) * 0.3
    score += min(len(code_blocks) / 5, 1) * 0.3
    score += min(len(entities) / 10, 1) * 0.2
    score += 0.2 if structured else 0
    
    importance_score = max(0.0, min(score, 1.0))
    
    confidence = 0.0
    if topics:
        confidence += 0.3
    if len(topics) >= 3:
        confidence += 0.1
    if entities:
        confidence += 0.3
    if len(entities) >= 3:
        confidence += 0.1
    if concepts:
        confidence += 0.2
    if capabilities:
        confidence += 0.1
    
    confidence = max(0.0, min(confidence, 1.0))
    
    return {
        "summary": " ".join(text.split()[:50]) if text else "",
        "topics": topics or [],
        "entities": entities or [],
        "concepts": concepts or [],
        "capabilities": capabilities or [],
        "relations": relations or [],
        "code_insights": code_insights,
        "content_type": content_type,
        "importance_score": importance_score,
        "confidence": confidence
    }
