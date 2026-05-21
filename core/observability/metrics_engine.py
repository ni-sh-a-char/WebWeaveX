from __future__ import annotations

def performance_metrics(durations_ms: dict):
    items=sorted((durations_ms or {}).items())
    total=sum(v for _,v in items)
    return {'total_ms': total, 'breakdown': items}
