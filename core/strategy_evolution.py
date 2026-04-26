def evolve_strategy(context):
    metrics = context["meta"]["metrics"]
    weights = context["learning"]["weights"]

    if metrics.get("exploration_ratio", 0) < 0.3:
        weights["url"] = weights.get("url", 0) + 0.05
        weights["preview"] = weights.get("preview", 0) + 0.05

    if metrics.get("decision_quality", 0) < 0.5:
        weights["intelligence"] = weights.get("intelligence", 0) + 0.1

    if metrics.get("knowledge_growth", 0) < 10:
        weights["topic"] = weights.get("topic", 0) + 0.05

    for key in sorted(weights.keys()):
        weights[key] = max(0.0, min(1.0, float(weights[key])))

    total = sum(weights.values())
    if total > 0:
        keys = sorted(weights.keys())
        running = 0.0
        for key in keys[:-1]:
            normalized = round(weights[key] / total, 6)
            weights[key] = normalized
            running += normalized
        last_key = keys[-1]
        weights[last_key] = round(max(0.0, 1.0 - running), 6)
