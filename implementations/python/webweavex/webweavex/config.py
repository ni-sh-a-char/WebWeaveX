"""WebWeaveX Configuration - Built-in defaults, no external dependencies."""

DEFAULT_CONFIG = {
    "version": "1.0.0",
    "meta": {
        "url": "",
        "title": ""
    },
    "fetch": {
        "timeout": 10,
        "retries": 3,
        "retry_delay": 1,
        "retry_backoff": 2,
        "user_agent": "WebWeaveX/1.0 (Python Library)",
        "accept_language": "en-US,en;q=0.9",
        "accept_encoding": "gzip, deflate",
        "follow_redirects": True,
        "max_redirects": 5,
    },
    "parse": {
        "extract_visible_text": True,
        "remove_scripts": True,
        "remove_styles": True,
        "remove_comments": True,
        "remove_hidden": True,
    },
    "clean": {
        "normalize_whitespace": True,
        "strip": True,
        "remove_empty_lines": True,
        "lowercase": False,
    },
    "chunking": {
        "size": 500,
        "overlap": 50,
        "method": "sliding_window",
        "preserve_words": True,
    },
    "entity_patterns": {
        "email": {
            "regex": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "type": "email",
        },
        "url": {
            "regex": r"https?://[^\s<>\"']+",
            "type": "url",
        },
        "number": {
            "regex": r"\b\d+(?:\.\d+)?\b",
            "type": "number",
        },
        "phone": {
            "regex": r"\+?[0-9]{1,4}?[-.\s]?\(?[0-9]{1,4}\)?[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,9}",
            "type": "phone",
        },
        "capitalized": {
            "regex": r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b",
            "type": "capitalized",
        },
    },
    "graph": {
        "edge_rule": "cooccurrence",
        "node_types": ["email", "url", "number", "capitalized", "phone"],
        "min_occurrence": 1,
        "directed": False,
    },
    "relations": {
        "enabled": True,
        "within_chunks": True,
        "edge_type": "cooccurrence",
    },
    "insights": {
        "enabled": True,
        "top_entities_count": 10,
        "include_stats": True,
    },
    "ai": {
        "providers": {
            "openai": {
                "endpoint": "https://api.openai.com/v1/chat/completions",
                "model": "gpt-3.5-turbo",
                "max_tokens": 1000,
                "temperature": 0.0,
            },
            "openrouter": {
                "endpoint": "https://openrouter.ai/api/v1/chat/completions",
                "model": "openai/gpt-3.5-turbo",
                "max_tokens": 1000,
                "temperature": 0.0,
            },
            "groq": {
                "endpoint": "https://api.groq.com/openai/v1/chat/completions",
                "model": "llama-3.1-8b-instant",
                "max_tokens": 1000,
                "temperature": 0.0,
            },
            "ollama": {
                "endpoint": "http://localhost:11434/api/chat",
                "model": "llama3.2",
                "max_tokens": 1000,
                "temperature": 0.0,
            },
        },
        "timeout": 30,
        "retries": 2,
    },
    "cache": {
        "enabled": False,
        "max_size": 1000,
        "ttl": 3600,
    },
}


def get_config(overrides=None):
    """Get configuration with optional overrides."""
    config = DEFAULT_CONFIG.copy()
    if overrides:
        config = _deep_merge(config, overrides)
    return config


def _deep_merge(base, overrides):
    """Deep merge two dictionaries."""
    result = base.copy()
    for key, value in overrides.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


CONFIG = DEFAULT_CONFIG


def set_config(config):
    """Set the global configuration."""
    global CONFIG
    CONFIG = config if config else DEFAULT_CONFIG


def get_current_config():
    """Get the current configuration."""
    return CONFIG
