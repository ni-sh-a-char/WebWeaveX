import webweavex as ww


def test_extract():
    assert isinstance(ww.extract("# Hi"), dict)
