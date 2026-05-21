from __future__ import annotations

def summarize_repository(parts: dict):
    return {
      "languages": sorted(set(parts.get('languages', []))),
      "frameworks": sorted(set(parts.get('frameworks', []))),
      "service_count": len(parts.get('architecture', {}).get('services', [])),
      "route_count": len(parts.get('api_contract', {}).get('routes', [])),
      "symbol_count": len(parts.get('ast', {}).get('symbols', [])),
    }
