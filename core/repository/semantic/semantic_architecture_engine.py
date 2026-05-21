from __future__ import annotations

from typing import Dict, List


def reconstruct_semantic_architecture(services: Dict[str, List[str]], dependencies: List[str], imports: List[str], routes: List[str]) -> Dict[str, List[str]]:
    deps = {d.lower() for d in dependencies or []}
    svc_count = len((services or {}).get("services", []))
    route_count = len(routes or [])

    styles = ["monolith"]
    if svc_count >= 5:
        styles.append("microservices")
    if {"kafka", "rabbitmq", "celery", "rq"} & deps:
        styles.append("event-driven")
    if route_count > 0 and svc_count > 0:
        styles.append("layered")
    if any("command" in i.lower() or "query" in i.lower() for i in imports or []):
        styles.append("cqrs")
    if {"aws-lambda", "serverless"} & deps:
        styles.append("serverless")

    relationships = []
    for api in (services or {}).get("apis", []):
        relationships.append({"from": "api", "to": api})
    for db in (services or {}).get("databases", []):
        relationships.append({"from": "service", "to": db})

    return {
        "styles": sorted(set(styles)),
        "relationships": sorted(relationships, key=lambda x: (x["from"], x["to"])),
    }
