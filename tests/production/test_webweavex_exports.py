"""Smoke-call public webweavex exports where safe."""

import inspect

import webweavex as wwx


def test_version_and_fingerprint():
    assert wwx.__version__ == "3.0.0"
    assert isinstance(wwx.fingerprint({"a": 1}), str)


def test_kernel_and_determinism():
    from core.contracts.runtime_contracts import UniversalInput

    out = wwx.run_canonical_pipeline(UniversalInput(source="hello", source_type="text"))
    assert out.get("pipeline_hash")
    fp = wwx.compute_global_runtime_fingerprint({"nodes": [], "edges": []})
    assert isinstance(fp, str)


def test_callable_exports_smoke():
    skip = {
        "extract",
        "extract_async",
        "extract_web",
        "extract_repo",
        "extract_docs",
        "extract_recursive",
        "crawl",
        "crawl_async",
        "stream_extract",
        "extract_repository",
        "extract_multimodal",
        "extract_document_runtime",
        "run_canonical_pipeline",
        "UniversalInput",
        "RuntimeKernel",
        "get_runtime_kernel",
    }
    for name in wwx.__all__:
        if name in skip or name.startswith("__"):
            continue
        obj = getattr(wwx, name)
        if not callable(obj):
            continue
        sig = inspect.signature(obj)
        if len(sig.parameters) == 0:
            try:
                obj()
            except Exception:
                pass
