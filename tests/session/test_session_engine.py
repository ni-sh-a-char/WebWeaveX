from core.session.session_engine import create_session


def test_create_session():
    result = create_session()

    assert result["authenticated"] is False
    assert result["bounded"] is True
