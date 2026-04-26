from .pattern_engine import detect_patterns
from .domain_intelligence import extract_domain, update_domain_learning


def _normalize(weights):
    total = sum(weights.values())
    if total <= 0:
        return weights
    for key in sorted(weights.keys()):
        weights[key] = weights[key] / total
    return weights


def update_weights(context):
    if context["meta"]["deterministic_mode"]:
        return

    weights = dict(context["learning"]["weights"])
    learning_rate = 0.05

    scores = list(context.get("intelligence", {}).get("scores", []))
    reward_signal = (sum(scores) / len(scores)) if scores else 0.0

    score_values = list(context.get("crawl", {}).get("path_scores", {}).values())
    if score_values:
        reward_signal = (reward_signal + (sum(score_values) / len(score_values) + 5.0) / 25.0) / 2.0

    signal_map = {
        "url": 0.2,
        "preview": 0.15,
        "topic": 0.15,
        "goal": 0.1,
        "learning": 0.05,
        "domain": 0.05,
        "pattern": 0.1,
        "knowledge": 0.1,
        "intelligence": 0.2,
    }

    for key in sorted(weights.keys()):
        delta = learning_rate * reward_signal * signal_map.get(key, 0.0)
        weights[key] = weights[key] + delta
        weights[key] = max(0.0, min(1.0, weights[key]))

    context["learning"]["weights"] = _normalize(weights)


def update_patterns(context):
    if context["meta"]["deterministic_mode"]:
        return
    context["intelligence"]["patterns"] = detect_patterns(context)


def update_domain_profiles(context):
    if context["meta"]["deterministic_mode"]:
        return

    visited = list(context["crawl"].get("visited_urls", []))
    scores = context["crawl"].get("path_scores", {})

    for url in visited:
        domain = extract_domain(url)
        if not domain:
            continue
        score = scores.get(url, 0.0)
        progress_delta = 0.1 if score >= 1 else -0.1 if score < 0 else 0.0
        update_domain_learning(domain, score, progress_delta, context)


def run_learning(context):
    if context["meta"]["deterministic_mode"]:
        return

    update_weights(context)
    update_patterns(context)
    update_domain_profiles(context)
