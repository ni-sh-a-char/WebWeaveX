def detect_patterns(context):
    history = list(context.get("crawl", {}).get("path_history", []))
    path_scores = dict(context.get("crawl", {}).get("path_scores", {}))

    repeated_paths = []
    high_value_patterns = []
    dead_patterns = []

    if not history:
        return {
            "repeated_paths": repeated_paths,
            "high_value_patterns": high_value_patterns,
            "dead_patterns": dead_patterns,
        }

    counts = {}
    for url in history:
        counts[url] = counts.get(url, 0) + 1

    repeated_paths = sorted([url for url, count in counts.items() if count > 1])

    for i in range(max(0, len(history) - 2)):
        seq = tuple(history[i : i + 3])
        avg_score = sum(path_scores.get(url, 0) for url in seq) / 3.0
        if avg_score >= 2.0:
            high_value_patterns.append((seq, round(avg_score, 6)))
        elif avg_score <= -1.0:
            dead_patterns.append((seq, round(avg_score, 6)))

    high_value_patterns = sorted(set(high_value_patterns), key=lambda x: (x[1], x[0]), reverse=True)
    dead_patterns = sorted(set(dead_patterns), key=lambda x: (x[1], x[0]))

    return {
        "repeated_paths": repeated_paths,
        "high_value_patterns": [
            {"path": list(seq), "avg_score": score} for seq, score in high_value_patterns
        ],
        "dead_patterns": [
            {"path": list(seq), "avg_score": score} for seq, score in dead_patterns
        ],
    }


def apply_pattern_bias(context, candidates):
    patterns = context["intelligence"].get("patterns", {})
    high_value = patterns.get("high_value_patterns", [])
    dead = patterns.get("dead_patterns", [])

    high_value_tokens = set()
    dead_tokens = set()

    for item in high_value:
        if isinstance(item, dict):
            for token in item.get("path", []):
                high_value_tokens.add(str(token))
        else:
            high_value_tokens.add(str(item))

    for item in dead:
        if isinstance(item, dict):
            for token in item.get("path", []):
                dead_tokens.add(str(token))
        else:
            dead_tokens.add(str(item))

    updated = []
    for candidate in candidates:
        current = dict(candidate)
        url = current.get("url", "")
        boost = 0.0

        for token in sorted(high_value_tokens):
            if token and token in url:
                boost += 0.2

        for token in sorted(dead_tokens):
            if token and token in url:
                boost -= 0.5

        current["score"] = round(float(current.get("score", 0.0)) + boost, 6)
        updated.append(current)

    return updated
