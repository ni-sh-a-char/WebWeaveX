import pytest

import webweavex


def test_version_alias():
    assert webweavex.version == "2.1.0"


def test_compute_global_fingerprint_export():
    assert callable(webweavex.compute_global_runtime_fingerprint)


def test_validate_replay_export():
    assert callable(webweavex.validate_replay_equivalence)


def test_query_helpers_empty():
    assert isinstance(webweavex.query_graph(node="n"), dict)
    assert isinstance(webweavex.query_documents(text="hi"), dict)


def test_compile_helpers():
    doc = webweavex.compile_document("# Title")
    assert doc is not None
