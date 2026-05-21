from core.evidence.inference_validation_engine import validate_inference


def test_poisoned_inference_blocked():
    r = validate_inference({"malicious": True}, [])
    assert r["valid"] is False
