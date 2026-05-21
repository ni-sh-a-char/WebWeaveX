import webweavex as ww
from core.evidence import apply_civilizational_epistemic_openness


def test_public_api():
    assert hasattr(ww, "extract")


def test_openness_export():
    assert callable(apply_civilizational_epistemic_openness)
