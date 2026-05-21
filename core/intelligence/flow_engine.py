"""Flow Engine - Edge flow detection."""


def detect_flows(edges):
    flows = []

    for edge in edges:
        flows.append({
            "from": edge.get("from", ""),
            "to": edge.get("to", "")
        })

    return sorted(flows, key=lambda x: (x["from"], x["to"]))