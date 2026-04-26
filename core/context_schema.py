def init_context(context):
    deterministic = context.get("meta", {}).get("deterministic_mode", True)

    context["crawl"] = {
        "visited_urls": [],
        "path_history": [],
        "link_previews": {},
        "page_scores": {},
        "path_scores": {},
        "url_scores_history": {},
        "last_page_text": "",
        "remaining_subgoals": [],
        "queue": [],
        "queue_counter": 0,
        "rate_limiter": None,
    }

    context["knowledge"] = {
        "entities": [],
        "graph": {},
        "topic_counts": {},
        "topic_graph": {},
        "last_intelligence": {},
    }

    context["learning"] = {
        "success_paths": {},
        "failed_paths": {},
        "trend": {},
        "weights": {
            "url": 0.25,
            "preview": 0.2,
            "topic": 0.15,
            "goal": 0.1,
            "learning": 0.1,
            "domain": 0.05,
            "pattern": 0.05,
            "knowledge": 0.1,
            "intelligence": 0.1,
        },
        "version": "v4b_hard_fix",
        "confidence": 0,
    }

    context["agent"] = {
        "decisions": {
            "explorer": [],
            "analyzer": [],
            "strategist": [],
        },
        "visited": [],
        "scores": [],
        "analyzer_cache": {},
        "strategy_performance": {
            "explore": {"success": 0, "failure": 0},
            "balanced": {"success": 0, "failure": 0},
            "exploit": {"success": 0, "failure": 0},
        },
        "self_reflection": [],
        "mode": "balanced",
    }

    context["domain"] = {
        "profiles": {},
        "navigation_patterns": {},
    }

    context["intelligence"] = {
        "history": [],
        "scores": [],
        "patterns": {},
        "decision_trace": [],
        "overrides": [],
    }

    context["meta"] = {
        "deterministic_mode": deterministic,
        "metrics": {},
        "mode": "balanced",
    }

    return context


def ensure_knowledge_schema(context):
    if "knowledge" not in context:
        context["knowledge"] = {}
    
    context["knowledge"].setdefault("entities", [])
    context["knowledge"].setdefault("graph", {})
    context["knowledge"].setdefault("topic_counts", {})
    context["knowledge"].setdefault("topic_graph", {})
    
    return context


def sanitize_context(context):
    data = context.get_all() if hasattr(context, "get_all") else context

    def _sanitize(value):
        if isinstance(value, dict):
            cleaned = {}
            for key, item in value.items():
                if key == "analyzer_cache":
                    continue
                if not isinstance(key, (str, int, float, bool)) and key is not None:
                    key = str(key)
                cleaned[key] = _sanitize(item)
            return cleaned
        if isinstance(value, list):
            return [_sanitize(item) for item in value]
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        return str(value)

    return _sanitize(data)
