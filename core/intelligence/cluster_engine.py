"""Cluster Engine - Graph clustering detection using sets."""


def detect_clusters(nodes, edges):
    adj = {}
    for node in nodes:
        adj[node["id"]] = set()

    for edge in edges:
        f = edge.get("from", "")
        t = edge.get("to", "")
        if f not in adj:
            adj[f] = set()
        if t not in adj:
            adj[t] = set()
        adj[f].add(t)
        adj[t].add(f)

    visited = set()
    clusters = []

    for node in adj:
        if node not in visited:
            stack = [node]
            cluster = []

            while stack:
                n = stack.pop()
                if n not in visited:
                    visited.add(n)
                    cluster.append(n)
                    for neighbor in adj.get(n, set()):
                        if neighbor not in visited:
                            stack.append(neighbor)

            if cluster:
                clusters.append(sorted(cluster))

    return sorted(clusters)