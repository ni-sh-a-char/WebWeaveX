"""WebWeaveX Code Reconstruction Engine (CRE)

Reconstructs code from web pages into logical files.
"""
import re
import os
from collections import defaultdict


LANGUAGE_PATTERNS = {
    "python": {
        "extensions": [".py"],
        "keywords": ["def ", "class ", "import ", "from ", "async def ", "print(", "if __name__", "raise "],
        "imports": [r"^import\s+(\w+)", r"^from\s+(\w+)\s+import"],
    },
    "javascript": {
        "extensions": [".js", ".jsx", ".ts", ".tsx"],
        "keywords": ["function ", "const ", "let ", "var ", "=>", "require(", "export ", "import "],
        "imports": [r"require\(['\"](\w+)['\"]", r"import\s+.*\s+from\s+['\"](\w+)['\"]"],
    },
    "typescript": {
        "extensions": [".ts", ".tsx"],
        "keywords": ["interface ", ": string", ": number", "type ", "<T>"],
    },
    "html": {
        "extensions": [".html", ".htm"],
        "keywords": ["<html", "<div", "<script", "<style", "<!DOCTYPE"],
    },
    "css": {
        "extensions": [".css", ".scss", ".sass"],
        "keywords": ["{", "}", "color:", "margin:", "padding:", "@media"],
    },
    "json": {
        "extensions": [".json"],
        "keywords": ["{", "}", "[\"", "\": {"],
    },
    "yaml": {
        "extensions": [".yaml", ".yml"],
        "keywords": [": ", "---"],
    },
    "bash": {
        "extensions": [".sh"],
        "keywords": ["#!/bin/bash", "echo ", "if [", "fi", "done"],
    },
    "go": {
        "extensions": [".go"],
        "keywords": ["package ", "func ", "import (", "type ", "struct {"],
    },
    "rust": {
        "extensions": [".rs"],
        "keywords": ["fn ", "impl ", "use ", "mod ", "pub ", "let mut"],
    },
}


PROJECT_INDICATORS = {
    "fastapi": ["fastapi", "FastAPI", "@app.get(", "@app.post("],
    "flask": ["flask", "Flask", "@app.route(", "from flask import"],
    "django": ["django", "from django"],
    "react": ["React", "useState", "useEffect", "import { Component"],
    "nextjs": ["next", "getServerSideProps", "getStaticProps", "Link from 'next"],
    "express": ["express", "Express", "app.get(", "app.post("],
    "node": ["module.exports", "require(", "process.env"],
    "vue": ["Vue", "createApp", "ref(", "computed("],
    "django": ["django", "class Meta:", "settings."],
    "pandas": ["pandas", "pd.read_", "DataFrame"],
    "numpy": ["numpy", "np.", "import numpy"],
    "torch": ["torch", "nn.", "Tensor"],
    "tensorflow": ["tensorflow", "tf.", "keras"],
}


def detect_language(code: str) -> tuple[str, float]:
    """Detect programming language from code content."""
    scores = defaultdict(float)
    
    for lang, config in LANGUAGE_PATTERNS.items():
        for keyword in config.get("keywords", []):
            if keyword in code:
                scores[lang] += 1.0
        
        for pattern in config.get("imports", []):
            matches = re.findall(pattern, code, re.MULTILINE)
            scores[lang] += len(matches) * 2.0
    
    if not scores:
        return "text", 0.0
    
    max_lang = max(scores.items(), key=lambda x: x[1])
    confidence = min(1.0, max_lang[1] / 10.0)
    
    return max_lang[0], confidence


UI_PATTERNS = [
    r"window\.",
    r"document\.",
    r"gtag\(",
    r"analytics",
    r"dataLayer",
    r"googletag",
    r"fbq\(",
    r"_gaq",
    r"mixpanel",
    r"amplitude",
    r"segment",
    r"Intercom",
    r"HubSpot",
    r"zendesk",
    r"drift",
    r"pendo",
    r"Hotjar",
]

MINIFIED_PATTERNS = [
    r"^\s*\{[^}]+\{[^}]+\{",  # Multiple { on same line without closing
    r"^[a-zA-Z0-9$_-]{100,}$",  # Very long identifier without spaces
]

CSS_PATTERNS = [
    r"color:\s*#",
    r"color:\s*rgb",
    r"display:\s*",
    r"margin:\s*",
    r"padding:\s*",
    r"background-color:",
    r"font-size:\s*",
    r"width:\s*\d+",
    r"height:\s*\d+",
    r"position:\s*absolute",
    r"position:\s*fixed",
    r"z-index:\s*",
    r"@media\s*\(",
    r"@keyframes\s*",
    r"@import\s*url",
]


def is_valid_code(block: dict, domain: str = "", min_length: int = 20) -> bool:
    """Validate if code block is meaningful developer code."""
    code = block.get("content", "")
    source = block.get("source", "generic")
    
    if not code:
        return False
    
    if source == "github" and "github.com" in domain:
        return True
    
    logical_keywords = ['def ', 'function ', 'class ', 'import ', 'from ', 'const ', 'let ', 'var ', 'return ', 'async ', 'public ', 'private ', 'interface ']
    has_logical = any(kw in code for kw in logical_keywords)
    
    if source == "stackoverflow" and has_logical:
        return True
    
    if len(code) < min_length:
        return False
    
    for pattern in UI_PATTERNS:
        if re.search(pattern, code, re.IGNORECASE):
            return False
    
    lines = code.split('\n')
    if len(lines) == 1:
        if len(code) > 200 and ':' in code:
            for pattern in CSS_PATTERNS:
                if re.search(pattern, code):
                    return False
            if all(c in '{}()[];' + string.ascii_letters + string.digits for c in code.replace(' ', '')):
                if code.count('{') > 3 or code.count('[') > 3:
                    return False
    
    for pattern in MINIFIED_PATTERNS:
        if re.match(pattern, code.strip()):
            return False
    
    has_logical_code = False
    logical_keywords = ['def ', 'function ', 'class ', 'import ', 'from ', 'const ', 'let ', 'var ', 'return ', 'async ', 'public ', 'private ', 'interface ']
    for kw in logical_keywords:
        if kw in code:
            has_logical_code = True
            break
    
    if not has_logical_code:
        return False
    
    return True


def extract_code_blocks(html: str, base_url: str = "") -> list[dict]:
    """Extract code blocks from HTML with strict filtering."""
    blocks = []
    domain = base_url.lower()
    
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<link[^>]*rel=["\']stylesheet["\'][^>]*>', '', html, flags=re.IGNORECASE)
    
    github_pattern = r'<table class="highlighttable">.*?<td class="code">\s*<pre>(.*?)</pre>\s*</td>'
    for match in re.finditer(github_pattern, html, re.DOTALL):
        code = clean_code(match.group(1))
        if code:
            blocks.append({
                "content": code,
                "source": "github",
                "confidence": 0.95,
            })
    
    code_fence_pattern = r'```(\w+)?\s*(.*?)```'
    for match in re.finditer(code_fence_pattern, html, re.DOTALL):
        lang = match.group(1) or ""
        code = match.group(2).strip()
        block = {"content": code, "source": "blog", "language": lang, "confidence": 0.7}
        if code and is_valid_code(block, domain):
            blocks.append(block)
    
    pre_pattern = r'<pre[^>]*>(.*?)</pre>'
    for match in re.finditer(pre_pattern, html, re.DOTALL):
        code = clean_code(match.group(1))
        block = {"content": code, "source": "stackoverflow", "confidence": 0.6}
        if code and is_valid_code(block, domain):
            blocks.append(block)
    
    code_tags = re.findall(r'<code[^>]*>(.*?)</code>', html, re.DOTALL)
    for code in code_tags:
        cleaned = clean_code(code)
        block = {"content": cleaned, "source": "generic", "confidence": 0.5}
        if cleaned and is_valid_code(block, domain):
            blocks.append(block)
    
    return blocks


def clean_code(html_text: str) -> str:
    """Remove HTML tags and cleanup code."""
    text = re.sub(r'<br\s*/?>', '\n', html_text)
    text = re.sub(r'<span[^>]*>(.*?)</span>', r'\1', text)
    text = re.sub(r'<[^<>]+>', '', text)
    text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    text = re.sub(r'\n\s*\n', '\n', text)
    lines = [line.rstrip() for line in text.split('\n')]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return '\n'.join(lines)


def infer_filename(code: str, source: str = "", index: int = 0) -> str:
    """Infer appropriate filename from code."""
    lang, _ = detect_language(code)
    extensions = LANGUAGE_PATTERNS.get(lang, {}).get("extensions", [".txt"])
    
    if "def " in code and "import pytest" not in code:
        if "main" in code.split('\n')[0]:
            return "main" + extensions[0]
        return f"module_{index + 1}" + extensions[0]
    
    if "class " in code:
        class_match = re.search(r'class\s+(\w+)', code)
        if class_match:
            class_name = class_match.group(1)
            base = class_name.lower().replace("Exception", "")
            return base + extensions[0]
    
    if "function" in code or "=>" in code:
        return f"index.{lang}"
    
    for ext in extensions:
        return f"file_{index + 1}" + ext
    
    return f"script_{index + 1}.py"


def group_code_files(blocks: list[dict], source_type: str = "") -> list[dict]:
    """Group code blocks into logical files."""
    if not blocks:
        return []
    
    if source_type == "github" or not source_type:
        files = []
        for i, block in enumerate(blocks):
            path = infer_filename(block["content"], block.get("source", ""), i)
            lang, conf = detect_language(block["content"])
            files.append({
                "path": path,
                "language": lang,
                "content": block["content"],
                "confidence": block.get("confidence", 0.5) * conf,
                "source": block.get("source", "generic"),
            })
        return files
    
    if blocks:
        lang, conf = detect_language(blocks[0]["content"])
        ext = ".txt"
        if lang in LANGUAGE_PATTERNS:
            exts = LANGUAGE_PATTERNS.get(lang, {}).get("extensions", [".txt"])
            if exts:
                ext = exts[0]
        combined = '\n\n'.join(b["content"] for b in blocks)
        return [{
            "path": "solution" + ext,
            "language": lang,
            "content": combined,
            "confidence": conf * 0.7,
            "source": "stackoverflow",
        }]
    
    return []


def detect_project_type(code: str) -> tuple[str, float]:
    """Detect project type from code."""
    scores = defaultdict(float)
    
    for ptype, indicators in PROJECT_INDICATORS.items():
        for indicator in indicators:
            if indicator in code:
                scores[ptype] += 1.0
    
    if not scores:
        return "unknown", 0.0
    
    max_type = max(scores.items(), key=lambda x: x[1])
    confidence = min(1.0, max_type[1] / 5.0)
    
    return max_type[0], confidence


def extract_dependencies(code: str) -> list[tuple[str, str]]:
    """Extract dependencies from code."""
    deps = set()
    
    py_imports = re.findall(r'^\s*import\s+(\w+)', code, re.MULTILINE)
    py_froms = re.findall(r'^\s*from\s+(\w+)\s+import', code, re.MULTILINE)
    for imp in py_imports + py_froms:
        if imp not in ("typing", "os", "sys", "re", "json", "datetime"):
            deps.add((imp, "python"))
    
    js_requires = re.findall(r"require\(['\"](\w+)['\"]", code)
    js_imports = re.findall(r"import\s+.*\s+from\s+['\"](\w+)['\"]", code)
    for imp in js_requires + js_imports:
        if isinstance(imp, tuple):
            imp = imp[0] if imp[0] else imp[1]
        if imp not in ("react", "vue", "angular", "express"):
            continue
        deps.add((imp, "javascript"))
    
    return sorted(list(deps), key=lambda x: x[0])


def detect_entry_points(files: list[dict]) -> list[str]:
    """Detect entry point files."""
    candidates = []
    
    priority_names = ["main", "app", "index", "server", "run", "start", "api", "server"]
    
    for f in files:
        path = f.get("path", "").lower()
        base = os.path.splitext(path)[0]
        
        for pri in priority_names:
            if base == pri or base.startswith(pri):
                candidates.append(f["path"])
                break
        else:
            if path in ["index.js", "main.js", "server.js", "app.py", "main.py"]:
                candidates.append(f["path"])
    
    return candidates[:3]


def is_code_expected(url: str, html: str) -> bool:
    if not url:
        return False
    
    url_lower = url.lower()
    
    if "github.com" in url_lower:
        return True
    if "stackoverflow.com" in url_lower:
        return True
    
    return False


def reconstruct_project(html: str, url: str = "", deterministic: bool = False) -> dict | None:
    """Reconstruct code project from HTML (pure engine)."""
    if not html:
        return None
    
    blocks = extract_code_blocks(html, url)
    
    if not blocks:
        return None
    
    source_type = "generic"
    if "github.com" in url:
        source_type = "github"
    elif "stackoverflow.com" in url:
        source_type = "stackoverflow"
    elif "medium.com" in url or "blog" in url:
        source_type = "blog"
    
    files = group_code_files(blocks, source_type)
    
    if deterministic:
        files = sorted(files, key=lambda x: (x["path"], x["content"]))
    
    if not files:
        return None
    
    all_code = '\n'.join(f["content"] for f in files)
    project_type, ptype_conf = detect_project_type(all_code)
    dependencies = extract_dependencies(all_code)
    entry_points = detect_entry_point_detect(files)
    
    return {
        "files": files,
        "project_type": project_type,
        "confidence": ptype_conf,
        "entry_points": entry_points,
        "dependencies": [dep[0] for dep in dependencies],
    }


def detect_entry_point_detect(files: list[dict]) -> list[str]:
    """Detect entry points from files."""
    candidates = []
    priority_names = ["main", "app", "index", "server", "run", "start", "api"]
    
    for f in files:
        path = f.get("path", "").lower()
        base = os.path.splitext(path)[0]
        
        for pri in priority_names:
            if base == pri or path == pri + ".py" or path == pri + ".js":
                candidates.append(f["path"])
                break
    
    if not candidates and files:
        candidates.append(files[0]["path"])
    
    return candidates[:3]