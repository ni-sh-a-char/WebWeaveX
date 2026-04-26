def decide_system_mode(context):
    metrics = context["meta"]["metrics"]

    if metrics.get("exploration_ratio", 0) < 0.4:
        return "explore"

    if metrics.get("decision_quality", 0) > 0.8:
        return "exploit"

    return "balanced"
