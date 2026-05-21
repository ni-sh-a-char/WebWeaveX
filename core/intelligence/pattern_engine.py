"""Pattern Engine - Structural pattern detection."""


def detect_patterns(analysis):
    signals = []

    density = analysis.get("density", 0)
    n = analysis.get("node_count", 0)
    e = analysis.get("edge_count", 0)

    if 0.3 < density < 0.8:
        signals.append("balanced_graph")

    if density >= 0.8:
        signals.append("dense_graph")

    if n >= 10:
        signals.append("large_graph")

    if e < n:
        signals.append("sparse_graph")

    return sorted(signals)