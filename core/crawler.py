from .fetcher import fetch_url
from .parser import extract_all
from .canonical import canonicalize
from .kaalka_engine import encrypt_canonical
from .detector import detect_page
from .adaptive import adaptive_extract
from .ai_engine import augment_with_ai
from .config import CONFIG
from .plugins import run_plugins
from .extractor_profiles import extract_profile
from .knowledge_engine import build_knowledge
from .multi_agent import create_multi_agent_system
from .goal_engine import GoalDecomposer, GoalTracker, refine_goal
from .learning_engine import get_learning_stats
from .meta_learning import get_meta_learning_stats
from .domain_intelligence import extract_domain, detect_domain_type, get_domain_profile
from .knowledge_graph import init_knowledge_graph, extract_and_add_entities, extract_and_add_relations
from .extractor_engine import ExtractionEngine
from .context_schema import init_context, sanitize_context
from .intelligence_engine import compute_intelligence
from .self_evaluator import evaluate_performance
from .strategy_evolution import evolve_strategy
from .meta_decision import decide_system_mode
from .adaptive_memory import update_memory
from .learning_pipeline import run_learning
from extractors.generic_html_extractor import GenericHTMLExtractor
from extractors.github_extractor import GitHubExtractor
from extractors.stackoverflow_extractor import StackOverflowExtractor
from core.intelligent_extraction import build_intelligence


def add_frontier(url, priority, context):
    counter = context["crawl"]["queue_counter"]
    context["crawl"]["queue"].append((-priority, counter, url))
    context["crawl"]["queue"].sort()
    context["crawl"]["queue_counter"] = counter + 1


def get_next_url(context):
    queue = context["crawl"]["queue"]
    if not queue:
        return None
    _, _, url = queue.pop(0)
    return url


def fetch_step(url, context):
    return fetch_url(url, context)


def parse_step(html, url, context):
    parsed = extract_all(html, url)
    return {
        "parsed": parsed,
        "canonical": canonicalize(parsed),
        "detection": detect_page(html, parsed, url),
    }


def extract_step(extraction_engine, url, html, parsed_bundle, context):
    detection = parsed_bundle["detection"]
    parsed = parsed_bundle["parsed"]

    if CONFIG.get("enable_adaptive", True):
        adaptive = adaptive_extract(url, html, parsed, detection)
        adaptive = augment_with_ai(adaptive, html, url, detection)
    else:
        adaptive = {"strategy": "disabled", "data": parsed}

    profile = extract_profile(url, detection, html, parsed)
    profile = run_plugins("post_extract", profile)

    unified = {
        "type": profile.get("type"),
        "text": profile.get("content", {}).get("text"),
        "code": profile.get("content", {}).get("code"),
        "structured": profile.get("content", {}).get("structured"),
    }

    extraction = extraction_engine.extract(url, html, {})
    unified["extraction"] = extraction

    return {
        "adaptive": adaptive,
        "profile": profile,
        "unified": unified,
    }


def intelligence_step(url, content, metadata, context):
    basic = build_intelligence(content, context)
    context["knowledge"]["last_intelligence"] = basic

    intelligence = compute_intelligence(context, url, content, metadata)
    context["intelligence"]["history"].append(intelligence)
    context["intelligence"]["scores"].append(intelligence["composite_score"])
    return intelligence


def knowledge_step(text, url, context):
    extract_and_add_entities(text, context)
    extract_and_add_relations(text, 10, context)

    knowledge = build_knowledge({"text": text, "code": [], "structured": {}})

    for entity in knowledge.get("entities", []):
        if entity not in context["knowledge"]["entities"]:
            context["knowledge"]["entities"].append(entity)

    topic_counts = context["knowledge"]["topic_counts"]
    topic_graph = context["knowledge"]["topic_graph"]
    for topic in knowledge.get("topics", []):
        topic_counts[topic] = topic_counts.get(topic, 0) + 1
        topic_graph.setdefault(topic, [])
        if url not in topic_graph[topic]:
            topic_graph[topic].append(url)

    return knowledge


def scoring_step(analyzer, url, context, base_domain=None):
    details = analyzer.explain_score(url, context, base_domain=base_domain)
    score = details["score"]
    context["crawl"]["page_scores"][url] = score
    context["crawl"]["path_scores"][url] = score
    context["crawl"]["url_scores_history"].setdefault(url, []).append(score)
    context["agent"]["scores"].append(score)
    context["agent"]["decisions"]["analyzer"].append({
        "action": "analyze",
        "url": url,
        "score": score,
        "url_score": details["url_score"],
        "topic_score": details["topic_score"],
        "preview_score": details["preview_score"],
        "knowledge_score": details["knowledge_score"],
        "intelligence_score": details["intelligence"]["composite_score"],
    })
    return score


def decision_step(explorer, strategist, analyzer, links, avg_score, context, base_domain=None):
    max_links = CONFIG.get("max_links_per_page", 5)
    selected_links = explorer.select_links(links, context, max_select=max_links, base_domain=base_domain)
    scored_candidates = []

    for link in selected_links:
        link_url = link["url"]
        if link_url in context["crawl"]["page_scores"]:
            score = context["crawl"]["page_scores"][link_url]
        else:
            score = analyzer.score_page(link_url, context, base_domain=base_domain)
        scored_candidates.append({"url": link_url, "score": score})

    next_paths = strategist.decide_next(selected_links, scored_candidates, avg_score, context)
    selected_urls = [url for _, url in next_paths]
    context["intelligence"]["decision_trace"].append(
        {
            "candidates": sorted(
                [
                    {
                        "url": c.get("url", ""),
                        "score": c.get("score", 0),
                        "intelligence": c.get("intelligence", {}),
                    }
                    for c in scored_candidates
                ],
                key=lambda x: x["url"],
            ),
            "selected": sorted(selected_urls),
        }
    )
    return next_paths


class WebCrawler:
    def __init__(self):
        self.extraction_engine = ExtractionEngine()
        self.extraction_engine.register(StackOverflowExtractor())
        self.extraction_engine.register(GitHubExtractor())
        self.extraction_engine.register(GenericHTMLExtractor())

    def crawl(self, start_url, depth, goal, use_multi_agent, context):
        if context is None:
            raise ValueError("context is required")

        init_context(context)
        init_knowledge_graph(context)
        context["goal"] = goal

        deterministic = context["meta"]["deterministic_mode"]
        timestamp = 1234567890 if deterministic else 1234567891
        base_domain = start_url.split("/")[2] if len(start_url.split("/")) > 2 else ""

        decomposer = GoalDecomposer(goal)
        subgoals = decomposer.decompose()
        tracker = GoalTracker(subgoals)

        agents = create_multi_agent_system(goal)
        explorer = agents["explorer"]
        analyzer = agents["analyzer"]
        strategist = agents["strategist"]

        add_frontier(run_plugins("pre_crawl", start_url), 0, context)

        results = []
        page_count = 0
        total_score = 0.0

        while context["crawl"]["queue"] and page_count < depth:
            url = get_next_url(context)
            if not url:
                break

            if url in context["crawl"]["visited_urls"]:
                continue
            if explorer.is_visited(url, context):
                continue

            explorer.mark_visited(url, context)
            context["crawl"]["visited_urls"].append(url)

            html = fetch_step(url, context)
            if not html:
                continue

            html = run_plugins("pre_extract", html)
            parsed_bundle = parse_step(html, url, context)

            extracted = extract_step(self.extraction_engine, url, html, parsed_bundle, context)
            unified = extracted["unified"]
            parsed = parsed_bundle["parsed"]

            text_content = unified.get("text", "") or ""
            context["crawl"]["last_page_text"] = text_content

            prev_progress = tracker.get_progress()
            tracker.update(text_content)
            new_progress = tracker.get_progress()
            progress_delta = new_progress - prev_progress
            context["crawl"]["remaining_subgoals"] = tracker.get_remaining()

            for link in parsed.get("links", []):
                link_url = link.get("url", "")
                link_text = link.get("text", "")
                if link_url and link_text:
                    context["crawl"]["link_previews"][link_url] = link_text

            if len(context["crawl"]["link_previews"]) > 1000:
                preview_items = list(context["crawl"]["link_previews"].items())[-500:]
                context["crawl"]["link_previews"] = dict(preview_items)

            extraction_content = unified.get("extraction", {}).get("content", {})
            intelligence = intelligence_step(
                url=url,
                content=extraction_content,
                metadata={"detection": parsed_bundle["detection"], "profile_type": unified.get("type", "")},
                context=context,
            )
            unified["intelligence"] = intelligence

            knowledge = knowledge_step(text_content, url, context)

            page_score = scoring_step(analyzer, url, context, base_domain=base_domain)
            context["crawl"]["path_history"].append(url)

            total_score += page_score
            page_count += 1
            avg_score = round(total_score / page_count, 6)
            mode = strategist.get_mode(avg_score, context)

            domain = extract_domain(url)
            domain_type = detect_domain_type(url, text_content, parsed_bundle["detection"])
            metrics = evaluate_performance(context)
            context["meta"]["metrics"] = metrics

            result = {
                "url": url,
                "canonical": parsed_bundle["canonical"],
                "encrypted": encrypt_canonical(parsed_bundle["canonical"], timestamp),
                "timestamp": timestamp,
                "detection": parsed_bundle["detection"],
                "adaptive": extracted["adaptive"],
                "profile": extracted["profile"],
                "unified": unified,
                "knowledge": knowledge,
                "intelligence": {
                    "confidence": intelligence["confidence"],
                    "relevance": intelligence["relevance"],
                    "novelty": intelligence["novelty"],
                    "authority": intelligence["authority"],
                    "semantic_score": intelligence["semantic_score"],
                    "composite_score": intelligence["composite_score"],
                },
                "goal": {
                    "original": goal,
                    "subgoals": subgoals,
                    "progress": tracker.get_progress(),
                    "remaining": tracker.get_remaining(),
                    "completed": tracker.get_completed(),
                },
                "learning": get_learning_stats(context),
                "meta": get_meta_learning_stats(context),
                "system_metrics": context["meta"]["metrics"],
                "domain": {
                    "name": domain,
                    "type": domain_type,
                    "profile": get_domain_profile(domain, context) if domain else {},
                },
                "memory": {
                    "context": sanitize_context(context),
                    "top_topics": sorted(context["knowledge"]["topic_counts"].items(), key=lambda x: (-x[1], x[0]))[:5],
                    "visited_urls": sorted(context["crawl"]["visited_urls"]),
                },
                "agent": {
                    "decisions": list(context["agent"]["decisions"]["analyzer"]),
                    "page_score": page_score,
                    "total_score": total_score,
                },
            }

            if use_multi_agent:
                result["multi_agent"] = {
                    "explorer": {
                        "decisions": list(context["agent"]["decisions"]["explorer"]),
                        "selected_count": len(context["agent"]["visited"]),
                    },
                    "analyzer": {
                        "decisions": list(context["agent"]["decisions"]["analyzer"]),
                        "avg_score": avg_score,
                    },
                    "strategist": {
                        "decisions": list(context["agent"]["decisions"]["strategist"]),
                        "mode": mode,
                    },
                }

            results.append(result)

            if tracker.is_complete():
                break

            next_paths = decision_step(
                explorer,
                strategist,
                analyzer,
                parsed.get("links", []),
                avg_score,
                context,
                base_domain=base_domain,
            )

            for score, next_url in next_paths:
                add_frontier(next_url, score, context)

            if not context["meta"]["deterministic_mode"]:
                evolve_strategy(context)
                refine_goal(context)
                update_memory(context)

            mode = decide_system_mode(context)
            context["agent"]["mode"] = mode
            context["meta"]["mode"] = mode

            analyzer.goal = context["goal"]
            strategist.goal = context["goal"]
            explorer.goal = context["goal"]

            if not context["meta"]["deterministic_mode"]:
                if len(context["crawl"]["visited_urls"]) % 3 == 0:
                    run_learning(context)

        return run_plugins("post_crawl", results)
