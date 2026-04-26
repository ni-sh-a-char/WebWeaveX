def evaluate_system(context):
    crawl = context.get("crawl", {})
    knowledge = context.get("knowledge", {})
    agent = context.get("agent", {})

    visited = len(crawl.get("visited_urls", []))
    scores = list(crawl.get("path_scores", {}).values())
    entities = len(knowledge.get("entities", []))
    topic_count = len(knowledge.get("topic_counts", {}))

    avg_score = (sum(scores) / len(scores)) if scores else 0.0

    efficiency = 0.0
    if visited > 0:
        efficiency = min(max((avg_score + 5.0) / 25.0, 0.0), 1.0)

    unique_domains = set()
    for url in crawl.get("visited_urls", []):
        parts = url.split("/")
        if len(parts) > 2:
            unique_domains.add(parts[2].lower())

    exploration_balance = 0.0
    if visited > 0:
        exploration_balance = min(len(unique_domains) / visited, 1.0)

    knowledge_growth = min((entities + topic_count) / 100.0, 1.0)

    analyzer_decisions = agent.get("decisions", {}).get("analyzer", [])
    decision_quality = 0.0
    if analyzer_decisions:
        valid = [d.get("score", 0) for d in analyzer_decisions if isinstance(d, dict)]
        if valid:
            decision_quality = min(max((sum(valid) / len(valid) + 5.0) / 25.0, 0.0), 1.0)

    return {
        "efficiency": round(efficiency, 6),
        "exploration_balance": round(exploration_balance, 6),
        "knowledge_growth": round(knowledge_growth, 6),
        "decision_quality": round(decision_quality, 6),
    }
