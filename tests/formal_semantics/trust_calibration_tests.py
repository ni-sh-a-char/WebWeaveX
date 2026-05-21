from core.internet.trust_calibration_engine import calibrate_trust


def test_trust_not_opaque():
    r = calibrate_trust("https://docs.python.org/3/", corroboration_count=2)
    assert r["opaque_heuristic"] is False
    assert "calibration_error" in r
