class Agent:
    def __init__(self, goal):
        self.goal = goal
        self.max_pages = 5

    def evaluate_page(self, knowledge, url, context):
        score = 0
        goal_words = self.goal.lower().split()
        topics = knowledge.get("topics", [])

        for topic in topics:
            for word in goal_words:
                if word in topic:
                    score += 2

        score += min(len(topics), 5)

        existing_topics = set(context["knowledge"]["topic_counts"].keys())
        score += len([topic for topic in topics if topic not in existing_topics])

        for topic in topics:
            if topic in context["knowledge"]["graph"] and len(context["knowledge"]["graph"][topic]) > 1:
                score += 1

        success = min(context["learning"]["success_paths"].get(url, 0), 5)
        failure = min(context["learning"]["failed_paths"].get(url, 0), 3)
        score += success
        score -= failure

        history = context["crawl"]["url_scores_history"].get(url, [])
        if len(history) >= 2:
            if history[-1] > history[-2]:
                score += 1
            elif history[-1] < history[-2]:
                score -= 1

        score = max(-2, min(score, 20))
        return -2 if score == 0 else score

    def should_crawl(self, url, depth, context):
        if depth >= self.max_pages:
            context["agent"]["decisions"]["analyzer"].append({"url": url, "action": "stop", "reason": "max_depth_reached"})
            return False

        if url in context["agent"]["visited"]:
            context["agent"]["decisions"]["analyzer"].append({"url": url, "action": "skip", "reason": "already_visited"})
            return False

        return True

    def select_next_urls(self, current_url, links, knowledge, context):
        top_topics = list(context["knowledge"]["topic_counts"].keys())[:5]

        scored_links = []
        for link in links:
            link_url = link.get("url", "")
            link_lower = link_url.lower()
            if link_url in context["agent"]["visited"]:
                continue

            score = 0
            for topic in top_topics:
                if topic in link_lower:
                    score += 2

            if any(keyword in link_lower for keyword in self.goal.lower().split()):
                score += 3

            scored_links.append((score, link_url))

        scored_links.sort(key=lambda item: (-item[0], item[1]))
        selected = scored_links[:3]

        context["agent"]["decisions"]["analyzer"].append({
            "current": current_url,
            "selected": [url for _, url in selected],
            "reason": "goal_aligned",
        })

        return selected

    def should_stop(self, page_count, total_score):
        if page_count >= self.max_pages:
            return True
        if page_count > 2 and total_score / page_count < 1:
            return True
        return False

    def get_decisions(self, context):
        return list(context["agent"]["decisions"]["analyzer"])
