def extract_domain(url):
    if not url:
        return ""
    parts = url.split("/")
    if len(parts) < 3:
        return ""
    domain = parts[2]
    return domain if domain_valid(domain) else ""


def domain_valid(domain):
    return isinstance(domain, str) and "." in domain and 3 <= len(domain) <= 100


def compute_domain_score(profile):
    if not profile:
        return 0
    score = (
        profile.get("success_paths", 0) * 2
        - profile.get("failure_paths", 0)
        + (profile.get("avg_score", 0) / 5)
    )
    return max(-10, min(score, 10))


def compute_exploration_priority(profile):
    if not profile:
        return 0
    visits = profile.get("visits", 0)
    success = profile.get("success_paths", 0)
    failure = profile.get("failure_paths", 0)
    quality = profile.get("quality_score", 0.0)
    exploration_bonus = 3.0 / (visits + 1)
    success_ratio = success / (success + failure + 1)
    return (success_ratio * 2) + (quality * 2) + exploration_bonus


def compute_pattern_score(path_history, context):
    if len(path_history) < 3:
        return 0
    patterns = context["domain"]["navigation_patterns"]
    key = tuple(path_history[-3:])
    data = patterns.get(key)
    if not data:
        return 0
    return data.get("success", 0) - data.get("failure", 0)


def detect_domain_type(url, content="", detection=None):
    url_lower = url.lower()
    url_patterns = {
        "documentation": ["/docs/", "/api/", "/reference/", "/guide/", "/manual/"],
        "news": ["/news/"],
        "blog": ["/blog/", "/post/", "/article/"],
        "ecommerce": ["/product/", "/cart/", "/checkout/", "/shop/", "/buy/"],
        "forum": ["/forum/", "/thread/", "/discussion/", "/topic/"],
    }
    for dtype, patterns in url_patterns.items():
        for pattern in patterns:
            if pattern in url_lower:
                return dtype

    if content:
        content_lower = content.lower()
        if sum(1 for c in ["```", "def ", "function", "class ", "import ", "const ", "var "] if c in content_lower) >= 3:
            return "documentation"
        if sum(1 for p in ["$", "rs", "eur", "gbp", "price", "cost", "buy"] if p in content_lower) >= 2:
            return "ecommerce"
        if sum(1 for c in ["comment", "replied", "posted", "said:"] if c in content_lower) >= 2:
            return "forum"
        if sum(1 for h in ["breaking", "reports", "announces", "exclusive", "analysis"] if h in content_lower) >= 2:
            return "news"
        if sum(1 for b in ["opinion", "featured", "tips", "how to", "guide"] if b in content_lower) >= 2:
            return "blog"

    if detection:
        dtype = detection.get("type", "")
        if dtype in ["documentation", "api", "reference"]:
            return "documentation"
        if dtype in ["product", "shop"]:
            return "ecommerce"
        if dtype in ["forum", "community"]:
            return "forum"
        if dtype in ["article", "post"]:
            return "blog"

    return "generic"


def get_domain_profile(domain, context):
    if not domain or not domain_valid(domain):
        return {}
    profiles = context["domain"]["profiles"]
    profile = profiles.get(domain)
    if profile is None:
        return {
            "type": "generic",
            "success_paths": 0,
            "failure_paths": 0,
            "avg_score": 0.0,
            "visits": 0,
            "quality_score": 0.0,
            "type_votes": {},
        }
    return {
        "type": profile.get("type"),
        "success_paths": profile.get("success_paths"),
        "failure_paths": profile.get("failure_paths"),
        "avg_score": profile.get("avg_score"),
        "visits": profile.get("visits"),
        "quality_score": profile.get("quality_score"),
        "type_votes": dict(profile.get("type_votes", {})),
    }


def update_domain_learning(domain, score, progress_delta, context):
    if not domain or not domain_valid(domain):
        return
    if context["meta"]["deterministic_mode"]:
        return

    profiles = context["domain"]["profiles"]
    if domain not in profiles:
        profiles[domain] = {
            "type": "generic",
            "success_paths": 0,
            "failure_paths": 0,
            "avg_score": 0.0,
            "visits": 0,
            "quality_score": 0.0,
            "type_votes": {},
        }

    profile = profiles[domain]
    profile["visits"] += 1

    if progress_delta > 0.05:
        profile["success_paths"] += 1
    elif progress_delta < -0.02:
        profile["failure_paths"] += 1

    visits = profile["visits"]
    old_avg = profile["avg_score"]
    profile["avg_score"] = ((old_avg * (visits - 1)) + score) / visits if visits > 0 else score

    quality = 1.0 if progress_delta > 0.05 else -1.0 if progress_delta < -0.02 else 0.0
    old_quality = profile.get("quality_score", 0.0)
    profile["quality_score"] = 0.8 * old_quality + 0.2 * quality


def set_domain_type(domain, domain_type, context):
    if not domain or not domain_valid(domain):
        return
    if context["meta"]["deterministic_mode"]:
        return

    profiles = context["domain"]["profiles"]
    if domain not in profiles:
        profiles[domain] = {
            "type": "generic",
            "success_paths": 0,
            "failure_paths": 0,
            "avg_score": 0.0,
            "visits": 0,
            "quality_score": 0.0,
            "type_votes": {},
        }

    profile = profiles[domain]
    type_votes = profile.setdefault("type_votes", {})
    type_votes[domain_type] = type_votes.get(domain_type, 0) + 1
    profile["type"] = max(type_votes, key=type_votes.get)
