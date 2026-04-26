def update_strategy_performance(mode, progress_delta, context):
    if context["meta"]["deterministic_mode"]:
        return

    performance = context["agent"]["strategy_performance"]
    if progress_delta > 0.05:
        status = "success"
    elif progress_delta <= -0.02:
        status = "failure"
    else:
        return

    if mode in performance:
        performance[mode][status] += 1


def get_strategy_confidence(mode, context):
    perf = context["agent"]["strategy_performance"].get(mode, {"success": 0, "failure": 0})
    total = perf["success"] + perf["failure"] + 1
    return perf["success"] / total


def get_all_strategy_confidences(context):
    return {
        "explore": round(get_strategy_confidence("explore", context), 3),
        "balanced": round(get_strategy_confidence("balanced", context), 3),
        "exploit": round(get_strategy_confidence("exploit", context), 3),
    }


def get_best_strategy(context):
    confidences = {
        "explore": get_strategy_confidence("explore", context),
        "balanced": get_strategy_confidence("balanced", context),
        "exploit": get_strategy_confidence("exploit", context),
    }
    return max(confidences, key=confidences.get)


def add_self_reflection(reflection_text, context):
    if not isinstance(reflection_text, (dict, str)):
        return

    reflections = context["agent"]["self_reflection"]
    reflections.append(reflection_text)
    if len(reflections) > 100:
        context["agent"]["self_reflection"] = reflections[-50:]


def get_recent_reflections(count, context):
    return context["agent"]["self_reflection"][-count:]


def get_meta_learning_stats(context):
    return {
        "strategy_performance": context["agent"]["strategy_performance"],
        "strategy_confidences": get_all_strategy_confidences(context),
        "best_strategy": get_best_strategy(context),
        "self_reflection_count": len(context["agent"]["self_reflection"]),
    }
