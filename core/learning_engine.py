def update_learning(url, score, goal_progress, progress_delta, context):
    if context["meta"]["deterministic_mode"]:
        return

    learning = context["learning"]

    if progress_delta > 0.05:
        status = "success"
    elif progress_delta <= -0.02:
        status = "failure"
    else:
        status = "neutral"

    if status == "success":
        learning["success_paths"][url] = learning["success_paths"].get(url, 0) + 1
    elif status == "failure":
        learning["failed_paths"][url] = learning["failed_paths"].get(url, 0) + 1

    old_trend = learning["trend"].get(url, 0.5)
    current = 1.0 if status == "success" else 0.5 if status == "neutral" else 0.0
    learning["trend"][url] = 0.7 * old_trend + 0.3 * current


def adjust_weights(context):
    if context["meta"]["deterministic_mode"]:
        return

    learning = context["learning"]
    weights = dict(learning["weights"])
    success = sum(learning["success_paths"].values())
    failure = sum(learning["failed_paths"].values())

    delta = 0.01
    inertia = 0.8

    if success > failure:
        new_goal = min(weights["goal"] + delta, 0.5)
        new_url = max(weights["url"] - delta, 0.1)
    else:
        new_url = min(weights["url"] + delta, 0.5)
        new_goal = max(weights["goal"] - delta, 0.1)

    weights["goal"] = inertia * weights["goal"] + (1 - inertia) * new_goal
    weights["url"] = inertia * weights["url"] + (1 - inertia) * new_url

    for key in weights:
        weights[key] = max(0.05, min(weights[key], 0.6))

    total = sum(weights.values())
    for key in weights:
        weights[key] = weights[key] / total

    learning["weights"] = weights


def get_adaptive_weights(context):
    weights = dict(context["learning"]["weights"])
    total = sum(weights.values())
    for key in weights:
        weights[key] = weights[key] / total
    context["learning"]["weights"] = weights
    return weights


def get_learning_stats(context):
    learning = context["learning"]
    success = sum(learning["success_paths"].values())
    failure = sum(learning["failed_paths"].values())
    total = success + failure + 1

    return {
        "success_paths": success,
        "failed_paths": failure,
        "adaptive_weights": get_adaptive_weights(context),
        "learning_trend": len(learning["trend"]),
        "confidence": round(success / total if total > 0 else 0, 3),
    }


def get_learning_confidence(context):
    learning = context["learning"]
    success = sum(learning["success_paths"].values())
    failure = sum(learning["failed_paths"].values())
    total = success + failure + 1
    return success / total if total > 0 else 0
