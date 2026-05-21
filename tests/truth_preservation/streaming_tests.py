import webweavex as ww


def test_stream():
    assert isinstance(ww.stream_extract("# Hi"), dict)
