"""One-shot generator: append the application-cognition fixture set."""
import json
import os

D = os.path.dirname(os.path.abspath(__file__))

APP_HTML = (
    "<html><head><title>Dashboard KPI</title></head><body>"
    "<nav><a href='/home'>Home</a><a href='/billing'>Billing</a></nav>"
    "<header><a href='/logout'>Logout</a></header>"
    "<div class='breadcrumb trail'>Home / Billing</div>"
    "<aside>side</aside>"
    "<div class='widget metric'>Revenue 42</div>"
    "<div class='card'>Orders 7</div>"
    "<form action='/save' id='mainForm'>"
    "<input type='text' name='search_query'>"
    "<input type='checkbox' name='active'>"
    "<input type='hidden' name='csrf_token' value='x'>"
    "<select name='region'><option>eu</option></select>"
    "<textarea name='notes'></textarea>"
    "<fieldset><input name='a' required></fieldset>"
    "<fieldset><input name='b'></fieldset>"
    "</form>"
    "<form action='/empty'></form>"
    "<table><tr><th>h1</th><th>h2</th></tr><tr><td>v</td><td>w</td></tr></table>"
    "<canvas data-live='1'></canvas><canvas></canvas>"
    "<div role='tab'>Tab One</div><div role='tab'>Tab Two</div>"
    "</body></html>"
)

INTERACTIONS = [
    {"action": "click", "selector": "#mainForm button"},
    {"type": "fill", "selector": "input[name=search_query]"},
    {"action": "open_modal_settings", "from": "/home", "to": "/settings"},
]

MEMORY = {
    "application_state": {"route": "/previous", "forms": [], "modals": [],
                          "widgets": [], "tabs": [], "authenticated": False,
                          "runtime_state": {}, "bounded": True},
    "workflows": {"seed": True},
}

STATES = [
    {"route": "/a"}, {"route": "/b"}, {"route": "/c"},
]

B = []


def fx(i, fn, args):
    B.append({"id": i, "fn": fn, "args": args})


fx("a-ui-rich", "extract_ui_semantics", [APP_HTML])
fx("a-ui-empty", "extract_ui_semantics", [""])
fx("a-forms-rich", "build_form_runtime", [APP_HTML])
fx("a-forms-empty", "build_form_runtime", [""])
fx("a-dash-rich", "build_dashboard_runtime", [APP_HTML])
fx("a-dash-empty", "build_dashboard_runtime", [""])
fx("a-nav-rich", "build_navigation_semantics", [APP_HTML, "/dash", None])
fx("a-nav-history", "build_navigation_semantics",
   [APP_HTML, "/dash", [{"path": "/a", "order": 0}, {"path": "/b", "order": 1}]])
fx("a-state-full", "build_application_state",
   ["/route/x", [{"action": "/save"}], [{"id": "m1"}], [{"text": "w"}],
    [{"label": "t"}], True])
fx("a-state-min", "build_application_state", ["/r"])
fx("a-trans-3", "build_application_transitions", [STATES])
fx("a-trans-1", "build_application_transitions", [[{"route": "/solo"}]])
fx("a-actions-3", "build_action_graph", [INTERACTIONS])
fx("a-actions-0", "build_action_graph", [[]])
fx("a-workflow", "build_workflow_graph",
   [STATES, [{"from": "/a", "to": "/b"}, {"from": "/b", "to": "/c",
              "relation": "redirect"}], INTERACTIONS])
fx("a-intent-known", "resolve_application_intent", ["login"])
fx("a-intent-unknown", "resolve_application_intent", ["wander"])
fx("a-recovery-rich", "recover_application_runtime",
   [APP_HTML, {"route": "/r", "modals": [], "authenticated": True}])
fx("a-recovery-empty", "recover_application_runtime",
   ["", {"route": "/r", "modals": [{"id": "m"}]}])
fx("a-context", "build_application_context",
   ["https://x.test/app", {"route": "/app", "authenticated": True},
    {"profile_id": "p1"}])
fx("a-memory-merge", "remember_application_runtime",
   [MEMORY, {"forms": {"f": 1}, "objectives": ["o1"]}])
fx("a-run-full", "run_application_cognition",
   ["https://x.test/dash", APP_HTML, INTERACTIONS, MEMORY,
    "extract_dashboard", True, {"profile_id": "p9"}, None,
    [{"path": "/a", "order": 0}, {"path": "/b", "order": 1}],
    [{"id": "modal1"}]])
fx("a-run-min", "run_application_cognition", ["https://x.test/", ""])

path = os.path.join(D, "fixtures.json")
existing = json.load(open(path, encoding="utf-8-sig"))
ids = {f["id"] for f in existing}
assert not ids & {f["id"] for f in B}
merged = existing + B
with open(path, "w", encoding="utf-8") as fh:
    json.dump(merged, fh, ensure_ascii=False, indent=1)
print(f"added {len(B)} application fixtures -> {len(merged)} total")
