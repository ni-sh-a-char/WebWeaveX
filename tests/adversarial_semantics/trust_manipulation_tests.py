from core.internet.confidence_calibration_engine import calibrate_confidence


def test_overconfident_detected():
    r = calibrate_confidence(0.99, 0.3)
    assert r["reliable"] is False
