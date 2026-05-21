import json

from core.crypto.kaalka_runtime_engine import decrypt_value, encrypt_value


def test_kaalka_roundtrip_deterministic():
    payload = {"runtime": "test", "values": [1, 2, 3]}
    key = "production-validation-key"
    serialized = json.dumps(payload, sort_keys=True)

    first_enc = encrypt_value(serialized, key)
    second_enc = encrypt_value(serialized, key)

    assert first_enc["encrypted"] == second_enc["encrypted"]

    first_dec = decrypt_value(first_enc["encrypted"], key)
    second_dec = decrypt_value(second_enc["encrypted"], key)

    assert first_dec["decrypted"] == second_dec["decrypted"]
    assert json.loads(first_dec["decrypted"]) == payload
