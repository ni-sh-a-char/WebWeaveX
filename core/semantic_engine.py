from .config import CONFIG


def normalize_text(text):
    if not text:
        return ""
    text = text.lower()
    import re
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def get_ngrams(text, n=2):
    words = text.split()
    if len(words) < n:
        return set()
    ngrams = set()
    for i in range(len(words) - n + 1):
        ngram = ' '.join(words[i:i+n])
        ngrams.add(ngram)
    return ngrams


def semantic_score(text, goal, weights=None):
    if weights is None:
        weights = {"unigrams": 1, "bigrams": 3, "trigrams": 5, "exact_phrase": 10}
    
    if not text or not goal:
        return 0
    
    text_norm = normalize_text(text)
    goal_norm = normalize_text(goal)
    
    if not text_norm or not goal_norm:
        return 0
    
    text_words = set(text_norm.split())
    goal_words = set(goal_norm.split())
    
    unigrams = text_words & goal_words
    unigram_score = len(unigrams) * weights.get("unigrams", 1)
    
    text_bigrams = get_ngrams(text_norm, 2)
    goal_bigrams = get_ngrams(goal_norm, 2)
    bigrams = text_bigrams & goal_bigrams
    bigram_score = len(bigrams) * weights.get("bigrams", 3)
    
    text_trigrams = get_ngrams(text_norm, 3)
    goal_trigrams = get_ngrams(goal_norm, 3)
    trigrams = text_trigrams & goal_trigrams
    trigram_score = len(trigrams) * weights.get("trigrams", 5)
    
    exact_score = 0
    if goal_norm in text_norm:
        exact_score = weights.get("exact_phrase", 10)
    
    total = unigram_score + bigram_score + trigram_score + exact_score
    
    max_possible = len(goal_words) * weights.get("unigrams", 1)
    max_possible += max(0, len(goal_bigrams)) * weights.get("bigrams", 3)
    max_possible += max(0, len(goal_trigrams)) * weights.get("trigrams", 5)
    max_possible += weights.get("exact_phrase", 10)
    
    if max_possible > 0:
        normalized = total / max_possible
        return round(min(normalized * 10, 10), 2)
    
    return 0


def score_urls_by_content(urls, content, goal, base_score=0):
    if not urls or not content:
        return [(base_score, url) for url in urls]
    
    content_norm = normalize_text(content)
    
    results = []
    for url in urls:
        url_norm = normalize_text(url)
        url_score = semantic_score(url_norm, goal)
        
        combined = (base_score * 0.4) + (url_score * 0.6)
        results.append((combined, url))
    
    results.sort(key=lambda x: (-x[0], x[1]))
    return results


def get_topic_relevance(topics, goal):
    if not topics or not goal:
        return 0
    
    total = 0
    for topic, count in topics.items():
        topic_score = semantic_score(topic, goal)
        total += topic_score * count
    
    return round(total, 2)