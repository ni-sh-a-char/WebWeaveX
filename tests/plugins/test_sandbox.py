from core.plugins import SemanticExecutionSandbox


def test_sandbox_blocks_dunder_keys():
    sb = SemanticExecutionSandbox()
    assert sb.put("__proto__", {}) is False
    assert sb.put("ok", 1) is True
