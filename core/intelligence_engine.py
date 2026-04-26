from .domain_intelligence import extract_domain, get_domain_profile, compute_domain_score
from .semantic_engine import semantic_score


def _safe_text(content):
    if not isinstance(content, dict):
        return ""
    return str(content.get("text", "") or "")


def _safe_code_blocks(content):
    if not isinstance(content, dict):
        return []
    code = content.get("code", []) or []
    return list(code) if isinstance(code, list) else []


def _safe_structured(content):
    if not isinstance(content, dict):
        return {}
    structured = content.get("structured", {}) or {}
    return structured if isinstance(structured, dict) else {}


def _tokenize(text):
    import re

    return sorted([token for token in re.findall(r"[a-zA-Z]+", text.lower()) if len(token) > 2])


def compute_cross_page_intelligence(context, url, content):
    topic_graph = context.get("knowledge", {}).get("topic_graph", {})
    entities = context.get("knowledge", {}).get("entities", [])

    if isinstance(content, dict):
        content_text = str(content.get("text", "") or "")
    else:
        content_text = str(content or "")

    score = 0.0
    tokens = sorted(set(content_text.lower().split()))

    for topic, urls in sorted(topic_graph.items(), key=lambda x: x[0]):
        if url in sorted(urls):
            score += len(sorted(urls)) * 0.1

    entity_values = sorted(
        [
            str(entity.get("value", "")).lower()
            for entity in entities
            if isinstance(entity, dict) and "value" in entity
        ]
    )

    overlap = len(set(tokens) & set(entity_values))
    score += overlap * 0.05

    return min(score, 1.0)


def compute_intelligence(context, url, content, metadata):
    text = _safe_text(content)
    code_blocks = _safe_code_blocks(content)
    structured = _safe_structured(content)

    tokens = _tokenize(text)
    token_count = len(tokens)
    unique_tokens = sorted(set(tokens))

    text_length = len(text)
    structure_richness = len(sorted(structured.keys()))
    code_block_count = len(code_blocks)
    semantic_density = (len(unique_tokens) / token_count) if token_count else 0.0

    depth_score = (
        min(text_length / 4000.0, 1.0) * 0.4
        + min(structure_richness / 8.0, 1.0) * 0.2
        + min(code_block_count / 10.0, 1.0) * 0.2
        + min(semantic_density, 1.0) * 0.2
    )

    known_entities = sorted(
        {
            str(entity.get("value", "")).lower()
            for entity in context.get("knowledge", {}).get("entities", [])
            if isinstance(entity, dict)
        }
    )
    known_topics = sorted(context.get("knowledge", {}).get("topic_graph", {}).keys())

    known_set = set(known_entities) | set([topic.lower() for topic in known_topics])
    novel_tokens = [token for token in unique_tokens if token not in known_set]
    novelty = (len(novel_tokens) / max(1, len(unique_tokens)))

    goal = str(context.get("goal", "") or "")
    relevance = semantic_score(text, goal) / 10.0 if goal else 0.0

    domain = extract_domain(url)
    profile = get_domain_profile(domain, context) if domain else {}
    authority = (compute_domain_score(profile) + 10.0) / 20.0 if profile else 0.0

    topic_overlap = 0.0
    topic_tokens = sorted([topic.lower() for topic in known_topics])
    if unique_tokens:
        overlap_count = len([token for token in unique_tokens if token in topic_tokens])
        topic_overlap = overlap_count / len(unique_tokens)

    semantic_score_value = (
        min(semantic_density, 1.0) * 0.6
        + min(topic_overlap, 1.0) * 0.4
    )

    confidence = (
        min(depth_score, 1.0) * 0.4
        + min(relevance, 1.0) * 0.3
        + min(semantic_score_value, 1.0) * 0.3
    )

    base_composite = (
        min(depth_score, 1.0) * 0.15
        + min(novelty, 1.0) * 0.2
        + min(relevance, 1.0) * 0.25
        + min(authority, 1.0) * 0.2
        + min(semantic_score_value, 1.0) * 0.2
    )
    cross_score = compute_cross_page_intelligence(context, url, text)
    composite_score = (base_composite * 0.8) + (cross_score * 0.2)

    return {
        "confidence": round(max(0.0, min(confidence, 1.0)), 6),
        "relevance": round(max(0.0, min(relevance, 1.0)), 6),
        "novelty": round(max(0.0, min(novelty, 1.0)), 6),
        "authority": round(max(0.0, min(authority, 1.0)), 6),
        "semantic_score": round(max(0.0, min(semantic_score_value, 1.0)), 6),
        "composite_score": round(max(0.0, min(composite_score, 1.0)), 6),
    }
