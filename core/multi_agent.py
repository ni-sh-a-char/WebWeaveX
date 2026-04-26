from .semantic_engine import semantic_score, get_topic_relevance
from .meta_learning import get_strategy_confidence
from .domain_intelligence import extract_domain, get_domain_profile, compute_domain_score, compute_exploration_priority, compute_pattern_score
from .knowledge_graph import compute_knowledge_score
from .intelligence_engine import compute_intelligence
from .pattern_engine import apply_pattern_bias


def _agent_state(context):
    return context["agent"]


def _crawl_state(context):
    return context["crawl"]


def _knowledge_state(context):
    return context["knowledge"]


def _learning_state(context):
    return context["learning"]


def intelligence_override(context, candidates, goal):
    high_priority = []
    filtered = []

    for candidate in candidates:
        intel = candidate.get("intelligence", {})
        relevance = float(intel.get("relevance", 0))
        novelty = float(intel.get("novelty", 0))
        authority = float(intel.get("authority", 0))

        if relevance > 0.85 and novelty > 0.7:
            high_priority.append(candidate)
            continue

        if authority > 0.9 and relevance > 0.6:
            high_priority.append(candidate)
            continue

        filtered.append(candidate)

    if high_priority:
        ordered = sorted(
            high_priority,
            key=lambda x: (-x.get("intelligence", {}).get("composite_score", 0), x.get("url", "")),
        )
        context["intelligence"]["overrides"].append(
            {
                "goal": goal,
                "type": "high_priority",
                "selected": [c.get("url", "") for c in ordered],
            }
        )
        return ordered

    ordered = sorted(filtered, key=lambda x: (-x.get("score", 0), x.get("url", "")))
    return ordered


def exploration_adjustment(context, candidates):
    history = context["crawl"]["path_history"]

    seen_domains = set()
    for item in history:
        if isinstance(item, str) and "://" in item:
            parts = item.split("/")
            if len(parts) > 2:
                seen_domains.add(parts[2])

    adjusted = []
    for candidate in candidates:
        current = dict(candidate)
        url = current.get("url", "")
        domain = ""
        if "://" in url:
            parts = url.split("/")
            if len(parts) > 2:
                domain = parts[2]
        if domain and domain not in seen_domains:
            current["score"] = round(float(current.get("score", 0)) + 0.15, 6)
        adjusted.append(current)

    return adjusted


class BaseAgent:
    def __init__(self, goal):
        self.goal = goal

    def get_decisions(self, context, role):
        return list(_agent_state(context)["decisions"][role])

    def get_avg_score(self, context):
        scores = _agent_state(context)["scores"]
        if not scores:
            return 0
        return sum(scores) / len(scores)


class ExplorerAgent(BaseAgent):
    def select_links(self, links, context, max_select=5, base_domain=None):
        crawl = _crawl_state(context)
        visited_urls = set(crawl["visited_urls"])
        agent_visited = _agent_state(context)["visited"]
        agent_visited_set = set(agent_visited)

        candidates = []
        for link in links:
            url = link.get("url", "")
            if not url or url in visited_urls or url in agent_visited_set:
                continue
            parsed = url.split("/")
            domain = parsed[2] if len(parsed) > 2 else url
            candidates.append({"url": url, "domain": domain, "path": "/".join(parsed[3:]) if len(parsed) > 3 else ""})

        domain_counts = {}
        for cand in candidates:
            domain_counts[cand["domain"]] = domain_counts.get(cand["domain"], 0) + 1

        deterministic = context["meta"]["deterministic_mode"]
        for cand in candidates:
            cand["domain_diversity"] = domain_counts[cand["domain"]]
            if deterministic:
                cand["domain_priority"] = 0
            else:
                profile = get_domain_profile(cand["domain"], context)
                cand["domain_priority"] = compute_exploration_priority(profile)

        if base_domain:
            candidates.sort(key=lambda x: (x["domain"] != base_domain, -x["domain_priority"], x["domain_diversity"], x["url"]))
        else:
            candidates.sort(key=lambda x: (-x["domain_priority"], x["domain_diversity"], x["url"]))

        selected = candidates[:max_select]
        for item in selected:
            if item["url"] not in agent_visited_set:
                agent_visited.append(item["url"])

        _agent_state(context)["decisions"]["explorer"].append({
            "action": "explore",
            "selected": [item["url"] for item in selected],
            "candidates": len(candidates),
        })

        return selected

    def mark_visited(self, url, context):
        visited = _agent_state(context)["visited"]
        if url not in visited:
            visited.append(url)

    def is_visited(self, url, context):
        return url in _agent_state(context)["visited"]


class AnalyzerAgent(BaseAgent):
    def _compute_signals(self, url, context, base_domain=None):
        crawl = _crawl_state(context)
        knowledge = _knowledge_state(context)

        preview_text = crawl["link_previews"].get(url, "")

        url_score = 0.0
        url_lower = url.lower()
        parsed = url.split("/")
        path_parts = [part for part in parsed[3:] if part]
        path_depth = len(path_parts)

        if path_depth <= 1:
            url_score += 3
        elif path_depth == 2:
            url_score += 1
        elif path_depth >= 5:
            url_score -= 2

        for keyword in ["/docs/", "/api/", "/guide/", "/reference/", "/v1/", "/auth/", "/login/"]:
            if keyword in url_lower:
                url_score += 3
        for keyword in ["/blog/", "/posts/", "/news/", "/tutorial/", "/help/"]:
            if keyword in url_lower:
                url_score += 1
        for keyword in ["/tag/", "/category/", "/archive/", "/page/", "/feed/"]:
            if keyword in url_lower:
                url_score -= 1

        if len(url) > 200:
            url_score -= 2
        elif len(url) > 150:
            url_score -= 1

        if base_domain:
            url_domain = parsed[2] if len(parsed) > 2 else ""
            if url_domain == base_domain:
                url_score += 2

        path_history = crawl["path_history"]
        url_count = path_history.count(url)
        recent_window = path_history[-3:] if len(path_history) >= 3 else path_history
        if url in recent_window:
            url_score -= 2
        elif url_count > 2:
            url_score -= 1
        elif url_count > 0:
            url_score -= 0.5

        preview_score = semantic_score(preview_text, self.goal) if preview_text else 0
        topic_score = get_topic_relevance(knowledge["topic_counts"], url)

        deterministic = context["meta"]["deterministic_mode"]
        if deterministic:
            knowledge_score = 0.0
        else:
            knowledge_score = compute_knowledge_score(
                knowledge["entities"],
                knowledge["graph"],
                url,
                knowledge["topic_counts"],
                knowledge["topic_graph"],
                context,
            )

        intelligence = compute_intelligence(
            context=context,
            url=url,
            content={"text": preview_text, "code": [], "structured": {}},
            metadata={"base_domain": base_domain or "", "source": "preview"},
        )

        return {
            "url_score": float(url_score),
            "preview_score": float(preview_score),
            "topic_score": float(topic_score),
            "knowledge_score": float(knowledge_score),
            "intelligence": intelligence,
        }

    def score_page(self, url, context, base_domain=None):
        weights = _learning_state(context)["weights"]
        signals = self._compute_signals(url, context, base_domain=base_domain)

        final_score = (
            weights.get("url", 0.25) * signals["url_score"]
            + weights.get("preview", 0.2) * signals["preview_score"]
            + weights.get("topic", 0.15) * signals["topic_score"]
            + weights.get("knowledge", 0.1) * signals["knowledge_score"]
            + weights.get("intelligence", 0.1) * signals["intelligence"]["composite_score"]
        )

        final_score = round(max(-5, min(final_score, 20)), 6)
        return -2 if final_score == 0 else final_score

    def explain_score(self, url, context, base_domain=None):
        signals = self._compute_signals(url, context, base_domain=base_domain)
        score = self.score_page(url, context, base_domain=base_domain)
        return {
            "url": url,
            "score": score,
            "url_score": signals["url_score"],
            "topic_score": signals["topic_score"],
            "preview_score": signals["preview_score"],
            "knowledge_score": signals["knowledge_score"],
            "intelligence": signals["intelligence"],
        }


class StrategistAgent(BaseAgent):
    def decide_next(self, selected_links, scored_candidates, avg_score, context):
        if not scored_candidates:
            _agent_state(context)["decisions"]["strategist"].append({"action": "strategize", "selected_paths": [], "reason": "no_candidates"})
            return []

        crawl = _crawl_state(context)
        knowledge = _knowledge_state(context)
        deterministic = context["meta"]["deterministic_mode"]

        for candidate in scored_candidates:
            url = candidate["url"]
            preview_text = crawl["link_previews"].get(url, "")
            candidate["preview_score"] = semantic_score(preview_text, self.goal) if preview_text else 0
            candidate["score"] = round(float(candidate.get("score", 0)) + (candidate["preview_score"] * 0.5), 6)

            goal_relevance = 0
            for subgoal in crawl["remaining_subgoals"]:
                goal_relevance += semantic_score(url, subgoal)
            candidate["goal_relevance"] = goal_relevance

            candidate["visited_penalty"] = -crawl["path_history"].count(url)
            candidate["learning_score"] = crawl["path_scores"].get(url, 0)

            if deterministic:
                candidate["domain_score"] = 0
                candidate["pattern_score"] = 0
                candidate["knowledge_score"] = 0
            else:
                domain = extract_domain(url)
                profile = get_domain_profile(domain, context)
                candidate["domain_score"] = compute_domain_score(profile) if profile else 0
                candidate["pattern_score"] = compute_pattern_score(crawl["path_history"], context)
                candidate["knowledge_score"] = compute_knowledge_score(
                    knowledge["entities"],
                    knowledge["graph"],
                    url,
                    knowledge["topic_counts"],
                    knowledge["topic_graph"],
                    context,
                )

        mode = self.get_mode(avg_score, context)

        for candidate in scored_candidates:
            preview_text = crawl["link_previews"].get(candidate["url"], "")
            candidate["intelligence"] = compute_intelligence(
                context=context,
                url=candidate["url"],
                content={"text": preview_text, "code": [], "structured": {}},
                metadata={"source": "decision"},
            )

        scored_candidates = apply_pattern_bias(context, scored_candidates)
        scored_candidates = exploration_adjustment(context, scored_candidates)
        sorted_candidates = intelligence_override(context, scored_candidates, self.goal)

        top_paths = sorted_candidates[:3]
        _agent_state(context)["decisions"]["strategist"].append({
            "action": "strategize",
            "selected_paths": [p["url"] for p in top_paths],
            "best_score": top_paths[0]["score"] if top_paths else 0,
            "avg_score": avg_score,
            "mode": mode,
        })

        return [(p["score"], p["url"]) for p in top_paths]

    def get_mode(self, avg_score, context):
        base_mode = "explore" if avg_score < 2 else "balanced" if avg_score <= 8 else "exploit"
        conf = {
            "explore": get_strategy_confidence("explore", context),
            "balanced": get_strategy_confidence("balanced", context),
            "exploit": get_strategy_confidence("exploit", context),
        }
        best = max(conf, key=conf.get)
        if conf[best] > conf[base_mode] + 0.1:
            return best
        return base_mode

    def should_stop(self, page_count, avg_score, max_pages=5):
        return page_count >= max_pages or (page_count >= 3 and avg_score < -2)


def create_multi_agent_system(goal):
    return {
        "explorer": ExplorerAgent(goal),
        "analyzer": AnalyzerAgent(goal),
        "strategist": StrategistAgent(goal),
    }
