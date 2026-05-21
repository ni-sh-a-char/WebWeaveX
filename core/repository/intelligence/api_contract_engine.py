from __future__ import annotations

def extract_api_contract(api_surface: dict):
    routes = sorted(set(api_surface.get('routes', [])))
    methods = sorted(set(api_surface.get('methods', [])))
    handlers = sorted(set(api_surface.get('handlers', [])))
    return {"routes": routes, "methods": methods, "handlers": handlers}
