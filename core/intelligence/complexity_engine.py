"""Complexity Engine - Structural complexity measurement."""


def compute_complexity(nodes, edges):
    n = len(nodes)
    e = len(edges)

    if n == 0:
        return 0.0

    return min(1.0, e / (n * n + 1))