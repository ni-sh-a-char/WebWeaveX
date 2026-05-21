from core.ir.media_ir import compile_media_ir


def test_compile_media_ir():
    result = compile_media_ir({"text": "hello"})
    assert result["ir"] == "media"
    assert result["content"]["text"] == "hello"
    assert result["bounded"] is True
