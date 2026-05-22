from core.browser.dom_stabilization_engine import compute_stable_dom_hash, stabilize_dom_html
from core.browser.spa_runtime_stabilizer import build_spa_stabilization
from core.memory.runtime_memory_engine import build_runtime_memory
from core.memory.stable_memory_hash import stable_memory_hash
from core.native.electron.electron_hash_engine import stable_electron_runtime_hash
from core.reconstruction.runtime_reconstruction_engine import reconstruct_runtime


def test_stable_dom_hash_repeatable():
    html = '<div data-reactid="1">A</div><time>2026-01-01T00:00:00Z</time>'
    assert compute_stable_dom_hash(html) == compute_stable_dom_hash(html)


def test_spa_stabilization_framework_detection():
    html = '<div id="app" data-v-123>__NEXT_DATA__</div>'
    spa = build_spa_stabilization(html, "https://app.example.com/dashboard")
    assert "next" in spa["spa_convergence"]["frameworks"] or "vue" in spa["spa_convergence"]["frameworks"]


def test_stable_memory_hash():
    m = build_runtime_memory(runtime_history=[{"tick": 1, "kind": "sync", "source": "a"}])
    assert m["stable_hash"] == stable_memory_hash(m)


def test_stable_electron_hash():
    payload = {
        "cdp": {"endpoints": [{"method": "Runtime.evaluate", "domain": "Runtime"}]},
        "routes": {"routes": [{"path": "/", "order": 0}]},
        "ipc": {"channels": [{"channel": "ipc:preload", "direction": "main_to_renderer"}]},
        "storage": {"indexed_db": [], "local_storage": {}},
    }
    assert stable_electron_runtime_hash(payload) == stable_electron_runtime_hash(payload)


def test_reconstruction_hash_stable():
    args = dict(
        semantic_ir={"ir": "semantic_runtime"},
        workflow_ir={"ir": "workflow_runtime"},
        runtime_type="browser",
        tick=0,
    )
    assert reconstruct_runtime(**args)["runtime_id"] == reconstruct_runtime(**args)["runtime_id"]
