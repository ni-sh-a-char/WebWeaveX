from __future__ import annotations

def route_format(content_type: str, source_url: str = ""):
    c = (content_type or '').lower()
    u = (source_url or '').lower()
    if 'json' in c or u.endswith('.json'): return 'json'
    if 'yaml' in c or u.endswith(('.yaml', '.yml')): return 'yaml'
    if 'xml' in c or u.endswith('.xml'): return 'xml'
    if 'markdown' in c or u.endswith('.md'): return 'markdown'
    if 'pdf' in c or u.endswith('.pdf'): return 'pdf'
    if 'html' in c or u.startswith('http'): return 'html'
    return 'text'
