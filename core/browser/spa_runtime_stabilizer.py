from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from core.browser.dom_stabilization_engine import compute_stable_dom_hash, stabilize_dom_html
from core.crypto.kaalka_hash_engine import compute_kaalka_hash_payload

_FRAMEWORK_MARKERS = {
    "react": [r"data-reactroot", r"__NEXT_DATA__", r"react-root"],
    "vue": [r"data-v-", r"__VUE__", r"id=\"app\""],
    "angular": [r"ng-version", r"ng-app", r"_ngcontent"],
    "next": [r"__NEXT_DATA__", r"/_next/static"],
    "nuxt": [r"__NUXT__", r"/_nuxt/"],
    "remix": [r"__remixContext", r"remix-"],
    "electron": [r"electron", r"preload"],
}


def detect_spa_framework(html: str) -> List[str]:
    detected: List[str] = []
    lower = html.lower()
    for name, patterns in sorted(_FRAMEWORK_MARKERS.items()):
        if any(re.search(pat, html, re.IGNORECASE) or pat.lower() in lower for pat in patterns):
            detected.append(name)
    return detected


def stabilize_route(url: str) -> str:
    base = url.split("#")[0].split("?")[0].rstrip("/")
    return base or url


def build_spa_stabilization(
    html: str,
    url: str,
    *,
    mutation_idle_ms: int = 0,
    network_idle: bool = True,
) -> Dict[str, Any]:
    """
    SPA convergence metadata: route freeze, framework detection, DOM stabilization.
    """
    stable_html, dom_meta = stabilize_dom_html(html)
    frameworks = detect_spa_framework(html)
    route = stabilize_route(url)

    convergence = {
        "route": route,
        "frameworks": frameworks,
        "hydration_complete": True,
        "mutation_idle_ms": mutation_idle_ms,
        "network_idle": network_idle,
        "async_rendering_converged": network_idle and mutation_idle_ms >= 0,
    }

    return {
        "stable_html": stable_html,
        "dom_stabilization": dom_meta,
        "spa_convergence": convergence,
        "stable_dom_hash": compute_stable_dom_hash(stable_html),
        "spa_fingerprint": compute_kaalka_hash_payload(
            {
                "route": route,
                "frameworks": frameworks,
                "dom_hash": dom_meta.get("stabilized_hash", ""),
            }
        ),
        "bounded": True,
    }


def apply_spa_stabilization_to_runtime(
    runtime: Dict[str, Any],
) -> Dict[str, Any]:
    html = str(runtime.get("html", ""))
    url = str(runtime.get("url", ""))
    spa = build_spa_stabilization(
        html,
        url,
        mutation_idle_ms=0,
        network_idle=bool(runtime.get("network", {}).get("bounded", True)),
    )
    return {
        **runtime,
        "html": spa["stable_html"],
        "dom_stabilization": spa["dom_stabilization"],
        "spa_stabilization": spa,
        "bounded": True,
    }
