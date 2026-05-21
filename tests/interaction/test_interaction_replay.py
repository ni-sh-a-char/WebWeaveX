from core.interaction import build_interaction_graph, replay_interactions


class _MockPage:
    def click(self, selector, timeout=None):
        self.last = selector

    def fill(self, selector, value, timeout=None):
        self.last = (selector, value)


def test_interaction_replay_order():
    actions = [
        {"action": "click", "selector": "#one"},
        {"action": "fill", "selector": "#two", "value": "abc"},
    ]

    first = replay_interactions(_MockPage(), actions)
    second = replay_interactions(_MockPage(), actions)

    assert first["replay"] == second["replay"]


def test_deterministic_graph_hash():
    actions = [
        {"id": "interaction_0", "action": "click", "selector": "#a"},
        {"id": "interaction_1", "action": "fill", "selector": "#b"},
    ]

    first = build_interaction_graph(actions)
    second = build_interaction_graph(actions)

    assert first["graph_hash"] == second["graph_hash"]
