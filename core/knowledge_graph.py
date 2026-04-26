def init_knowledge_graph(context):
    if "knowledge" not in context:
        raise KeyError("knowledge")
    if "graph" not in context["knowledge"]:
        context["knowledge"]["graph"] = {}


def add_entity(entity, context):
    if not entity or context["meta"]["deterministic_mode"]:
        return

    entities = context["knowledge"]["entities"]
    if len(entities) >= 500:
        entities[:] = entities[-250:]

    existing = {item.get("value") for item in entities}
    value = entity.get("value", "")
    if value and value not in existing:
        entities.append(entity)


def add_relation(source, target, relation_type, context):
    if not source or not target or context["meta"]["deterministic_mode"]:
        return

    graph = context["knowledge"]["graph"]
    current_count = sum(len(rels) for rels in graph.values())
    if current_count >= 2000:
        oldest_keys = list(graph.keys())[:10]
        for key in oldest_keys:
            del graph[key]

    if source not in graph:
        graph[source] = []

    relations = graph[source]
    existing_targets = {rel.get("target") for rel in relations}
    if target not in existing_targets:
        relations.append({"target": target, "type": relation_type})

    graph[source] = sorted(relations, key=lambda x: (x.get("target", ""), x.get("type", "")))
    context["knowledge"]["graph"] = dict(sorted(graph.items()))


def compute_knowledge_score(entities, knowledge_graph, url, topic_counts, topic_graph, context):
    if not url:
        return 0
    if not entities and not knowledge_graph:
        return 0

    score = 0
    domain = ""
    for part in url.split("/"):
        if part and "." not in part:
            domain = part
            break

    if domain and domain in knowledge_graph:
        score += len(knowledge_graph[domain]) * 0.5

    score += len(entities) * 0.2

    if topic_counts:
        common_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        score += sum(count for _, count in common_topics) * 0.1

    domain_entities = 0
    if topic_graph:
        for topic, urls in topic_graph.items():
            topic_parts = set(topic.lower().replace(".", "_").split("_"))
            if url in urls:
                domain_entities += len(urls)
            elif domain and topic_parts & {domain.lower()}:
                domain_entities += len(urls) * 0.5

    score += domain_entities * 0.3
    return max(-5, min(score, 5))


def extract_and_add_entities(text, context):
    if not text or context["meta"]["deterministic_mode"]:
        return []

    import re
    from collections import Counter

    entities = []
    seen = set()

    for match in re.finditer(r"https?://[^\s]+", text):
        value = match.group(0)[:100]
        if value and value not in seen:
            entities.append({"type": "url", "value": value})
            seen.add(value)

    for match in re.finditer(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text):
        value = match.group(0)
        if value and value not in seen:
            entities.append({"type": "email", "value": value})
            seen.add(value)

    for match in re.finditer(r"[a-zA-Z0-9_-]+\.(py|js|json|html|css|txt|md|yml|yaml|xml|csv|sql)", text):
        value = match.group(0)
        if value and value not in seen:
            entities.append({"type": "file", "value": value})
            seen.add(value)

    words = re.findall(r"\b[a-zA-Z]{5,}\b", text.lower())
    valid_words = [
        w for w in words
        if w.isalpha() and w not in {"there", "which", "where", "their", "would", "could", "should", "about", "while"}
    ]

    for kw, _ in Counter(valid_words).most_common(10):
        if kw not in seen and len(seen) < 20:
            entities.append({"type": "keyword", "value": kw})
            seen.add(kw)

    for entity in entities:
        add_entity(entity, context)

    return entities


def extract_and_add_relations(text, max_relations, context):
    if not text or context["meta"]["deterministic_mode"]:
        return []

    import re
    from collections import Counter

    normalized = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
    normalized = re.sub(r"\s+", " ", normalized)

    stopwords = {
        "about", "after", "again", "being", "below", "could", "didn", "doing", "down", "during", "each", "first", "found", "from", "further", "had", "has", "have", "having", "here", "hers", "herself", "himself", "his", "how", "however", "into", "just", "more", "most", "much", "mustn", "needn", "never", "other", "our", "ours", "ourselves", "out", "over", "own", "same", "should", "shouldn", "since", "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn", "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with", "won", "would", "you", "your"
    }

    filtered = [w for w in normalized.split() if w not in stopwords and len(w) >= 5 and w.isalpha()]
    relations = []
    for word, count in Counter(filtered).items():
        if count >= 3 and len(relations) < max_relations:
            relations.append({"source": "text_content", "target": word, "type": "strong_topic"})

    for relation in relations:
        add_relation(relation["source"], relation["target"], relation["type"], context)

    return relations
