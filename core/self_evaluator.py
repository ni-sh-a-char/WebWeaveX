def evaluate_performance(context):
    crawl = context["crawl"]
    intelligence = context["intelligence"]
    learning = context["learning"]

    efficiency = len(crawl["visited_urls"]) / max(len(crawl["path_history"]), 1)
    knowledge_growth = len(context["knowledge"]["entities"])

    score_values = []
    for item in context["agent"]["scores"]:
        if isinstance(item, dict):
            score_values.append(float(item.get("score", 0)))
        else:
            score_values.append(float(item))

    decision_quality = sum(score_values) / max(len(score_values), 1)
    exploration_ratio = len(set(crawl["visited_urls"])) / max(len(crawl["path_history"]), 1)

    return {
        "efficiency": round(efficiency, 4),
        "knowledge_growth": knowledge_growth,
        "decision_quality": round(decision_quality, 4),
        "exploration_ratio": round(exploration_ratio, 4),
    }
