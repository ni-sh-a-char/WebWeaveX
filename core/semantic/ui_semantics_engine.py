from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup


UI_INTENT_RULES = {
    "destructive": re.compile(r"\b(delete|remove|destroy|revoke)\b", re.I),
    "authentication": re.compile(r"\b(login|sign\s*in|password|oauth)\b", re.I),
    "billing": re.compile(r"\b(billing|invoice|payment|subscription)\b", re.I),
    "monitoring": re.compile(r"\b(monitor|alert|metric|status)\b", re.I),
    "settings": re.compile(r"\b(settings|preferences|configuration)\b", re.I),
    "admin_panel": re.compile(r"\b(admin|manage users|permissions)\b", re.I),
}


def extract_ui_semantics(
    html: str = "",
    actions: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    soup = BeautifulSoup(html or "", "html.parser")
    text = soup.get_text(" ", strip=True)[:50000]
    actions = actions or []

    intents: Dict[str, bool] = {key: False for key in UI_INTENT_RULES}
    for intent, pattern in UI_INTENT_RULES.items():
        if pattern.search(text):
            intents[intent] = True

    buttons = []
    for button in soup.find_all(["button", "a", "input"])[:2000]:
        label = str(button.get_text(strip=True) or button.get("value", ""))[:200]
        if not label:
            continue
        role = "primary_workflow"
        if UI_INTENT_RULES["destructive"].search(label):
            role = "destructive"
        buttons.append({"label": label, "role": role})

    return {
        "destructive_actions": [b for b in buttons if b["role"] == "destructive"],
        "primary_workflows": [b for b in buttons if b["role"] == "primary_workflow"][:500],
        "navigation_intent": bool(soup.find_all("nav")),
        "dashboards": bool(re.search(r"dashboard|kpi|metrics", text, re.I)),
        "forms": len(soup.find_all("form")),
        "admin_panels": intents["admin_panel"],
        "settings": intents["settings"],
        "authentication": intents["authentication"],
        "billing": intents["billing"],
        "monitoring": intents["monitoring"],
        "actions": actions[:1000],
        "bounded": True,
    }
