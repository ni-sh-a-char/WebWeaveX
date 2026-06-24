#!/usr/bin/env python3
"""Session-28 cross-language golden vectors from canonical Python 2.1.0.

    python tools/gen_java_parity_vectors_s28.py <out.json>

Covers the frontier-reduced portable APIs proven in Session 28:
  - version / __version__            (module constant "2.1.0")
  - query_repo(result)               (pure dict passthrough content.repository)
  - compile_document(text)           (= compile_document_ir; pure document semantic IR)
  - capture_websocket_frames(page)   (stub-page contract; pure stream events)
  - track_websocket_connections(page)
  - capture_dom_mutations(page)      (stub-page contract; pure events + kaalka dom_hash)
  - extract_infinite_scroll(page)    (stub-page _test_scroll contract; pure loop)
  - replay_interactions(page, log)   (pure record_interaction output; handlers side-effect only)

Python is the oracle. Every vector is browser-free / bs4-free / network-free:
the page is a deterministic test double exposing only _test_* attributes, exactly
as the canonical Python unit tests drive these engines.
"""
from __future__ import annotations

import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

import webweavex
from webweavex import (
    query_repo,
    compile_document,
    capture_websocket_frames,
    capture_dom_mutations,
    extract_infinite_scroll,
    replay_interactions,
)
from core.streaming.websocket_runtime_engine import track_websocket_connections


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


# ---- deterministic page test doubles (mirror canonical Python unit tests) ----
class _ScrollPage:
    """Mirror tests/interaction/test_infinite_scroll.py::_ScrollPage (stabilizes after 2)."""

    def __init__(self):
        self._test_html = "<html>start</html>"
        self._test_dom_hash = compute_kaalka_hash(self._test_html)
        self._count = 0

    def _test_scroll(self):
        self._count += 1
        if self._count > 2:
            return
        self._test_html += f"<div>{self._count}</div>"
        self._test_dom_hash = compute_kaalka_hash(self._test_html)


class _WsPage:
    def __init__(self, frames, connections=None):
        if frames is not None:
            self._test_websocket_frames = frames
        if connections is not None:
            self._test_websocket_connections = connections


class _DomPage:
    def __init__(self, html, mutations):
        if html is not None:
            self._test_html = html
        if mutations is not None:
            self._test_dom_mutations = mutations


WS_FRAMES = [
    {"connection_id": "ws1", "url": "wss://example.com/socket", "direction": "incoming", "payload": "hello"},
    {"connection_id": "ws1", "direction": "outgoing", "payload": "ack"},
    {"connection_id": "ws2", "url": "wss://x/2", "direction": "incoming", "payload": "p2"},
]
DOM_MUTATIONS = [
    {"type": "add", "node_id": "n1", "payload": "<div>a</div>"},
    {"type": "text", "node_id": "n1", "payload": "updated"},
]
REPLAY_ACTIONS = [
    {"action": "click", "selector": "#one"},
    {"action": "fill", "selector": "#two", "value": "abc"},
    {"action": "hover", "selector": "#three", "metadata": {"k": "v"}},
    {"type": "wait", "selector": "#four"},
    {"action": "noop_unknown", "selector": "#five"},
]


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 28: frontier-reduced portable APIs)"}

    # ---- trivial constants ----
    out["version"] = [ev("version", {}, webweavex.version)]
    out["__version__"] = [ev("dunder_version", {}, webweavex.__version__)]

    # ---- query_repo: pure passthrough content.repository ----
    out["query_repo"] = [
        ev("full", {"result": {"content": {"repository": {"files": ["a.py", "b.py"], "loc": 12}}}},
           query_repo({"content": {"repository": {"files": ["a.py", "b.py"], "loc": 12}}})),
        ev("empty", {"result": {}}, query_repo({})),
        ev("content_no_repo", {"result": {"content": {"documents": {"x": 1}}}},
           query_repo({"content": {"documents": {"x": 1}}})),
        ev("nested", {"result": {"content": {"repository": {"tree": {"src": ["m.py"]}, "languages": ["py"]}}}},
           query_repo({"content": {"repository": {"tree": {"src": ["m.py"]}, "languages": ["py"]}}})),
    ]

    # ---- compile_document(text) = compile_document_ir(text) ----
    DOCS = {
        "empty": "",
        "single": "Install the package. Then run the build.",
        "tutorial": ("First, clone the repository. Next, install dependencies. "
                     "Finally, run the tests. Therefore the project is ready."),
        "argument": ("The system is fast because it caches results. "
                     "However, caching increases memory. Thus a tradeoff exists."),
        "headings": "# Setup\nDo the setup.\n## Details\nMore details here.\nThe reason is clarity.",
    }
    out["compile_document"] = [ev(n, {"text": t}, compile_document(t)) for n, t in DOCS.items()]

    # ---- capture_websocket_frames / track_websocket_connections ----
    out["capture_websocket_frames"] = [
        ev("frames", {"_test_websocket_frames": WS_FRAMES}, capture_websocket_frames(_WsPage(WS_FRAMES))),
        ev("none_page", {"page": None}, capture_websocket_frames(None)),
        ev("no_attr", {"page": "object()"}, capture_websocket_frames(object())),
        ev("empty_frames", {"_test_websocket_frames": []}, capture_websocket_frames(_WsPage([]))),
    ]
    out["track_websocket_connections"] = [
        ev("from_frames", {"_test_websocket_frames": WS_FRAMES}, track_websocket_connections(_WsPage(WS_FRAMES))),
        ev("explicit", {"_test_websocket_connections": [{"connection_id": "c2"}, {"connection_id": "c1"}]},
           track_websocket_connections(_WsPage(None, [{"connection_id": "c2"}, {"connection_id": "c1"}]))),
        ev("none_page", {"page": None}, track_websocket_connections(None)),
    ]

    # ---- capture_dom_mutations ----
    out["capture_dom_mutations"] = [
        ev("mutations", {"_test_html": "<html><body>one</body></html>", "_test_dom_mutations": DOM_MUTATIONS},
           capture_dom_mutations(_DomPage("<html><body>one</body></html>", DOM_MUTATIONS))),
        ev("none_page", {"page": None}, capture_dom_mutations(None)),
        ev("html_no_mut", {"_test_html": "<p>x</p>", "_test_dom_mutations": None},
           capture_dom_mutations(_DomPage("<p>x</p>", None))),
    ]

    # ---- extract_infinite_scroll (stub _ScrollPage contract) ----
    out["extract_infinite_scroll"] = [
        ev("scroll_page", {"contract": "_ScrollPage"}, extract_infinite_scroll(_ScrollPage())),
    ]

    # ---- replay_interactions (pure record_interaction output) ----
    out["replay_interactions"] = [
        ev("actions", {"interaction_log": REPLAY_ACTIONS}, replay_interactions(None, REPLAY_ACTIONS)),
        ev("empty", {"interaction_log": []}, replay_interactions(None, [])),
    ]

    path = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s28.json"
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    total = sum(len(v) for k, v in out.items() if isinstance(v, list))
    print(f"wrote {path} ({total} vectors across {sum(1 for k,v in out.items() if isinstance(v,list))} sections)")


if __name__ == "__main__":
    main()
