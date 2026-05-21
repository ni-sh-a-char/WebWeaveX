import webweavex as ww
from core.evidence import apply_formal_semantic_foundation


def test_exports():
    assert hasattr(ww, "extract")
    assert callable(apply_formal_semantic_foundation)
