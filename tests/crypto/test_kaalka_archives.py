from core.crypto.kaalka_archive_engine import (
    decrypt_extraction_archive,
    encrypt_extraction_archive,
)


def test_archive_replay_and_hash():
    archive = {
        "extraction": {"url": "https://example.com"},
        "browser_state": {"ir": "browser_state"},
        "bounded": True,
    }

    encrypted = encrypt_extraction_archive(archive, "archive-key")
    decrypted = decrypt_extraction_archive(encrypted, "archive-key")

    assert decrypted["archive"] == archive
    assert decrypted["content_hash"] == encrypted["content_hash"]
