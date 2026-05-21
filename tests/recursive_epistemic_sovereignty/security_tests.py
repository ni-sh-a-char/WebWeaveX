from core.security.remote_target import is_safe_remote_target


def test_localhost():
    assert is_safe_remote_target("http://127.0.0.1/") is False
