from __future__ import annotations

def reconstruct_architecture(topology: dict, imports: list, routes: list, dependencies: list):
    services = sorted(set(topology.get('services', [])))
    db = sorted(set([d for d in (dependencies or []) if any(k in d.lower() for k in ['postgres','mysql','sqlite','mongo'])]))
    frontend = any(any(k in d.lower() for k in ['react','vue','angular','next']) for d in (dependencies or []))
    backend = any(any(k in d.lower() for k in ['flask','django','fastapi','express','spring']) for d in (dependencies or []))
    return {
      "services": services,
      "apis": sorted(set(routes or [])),
      "workers": [], "schedulers": [], "queues": [], "gateways": [],
      "databases": db,
      "frontend_backend_split": {"frontend": frontend, "backend": backend},
      "relationships": [{"from": services[i], "to": services[i+1]} for i in range(max(0,len(services)-1))]
    }
