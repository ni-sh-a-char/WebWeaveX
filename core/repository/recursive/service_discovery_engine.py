from __future__ import annotations


def discover_services(topology: dict, routes: dict):
    services = sorted(set(topology.get("services", [])))
    apis = sorted(set(routes.get("routes", [])))
    return {"services": services, "apis": apis, "workers": [], "schedulers": [], "queues": [], "gateways": []}

