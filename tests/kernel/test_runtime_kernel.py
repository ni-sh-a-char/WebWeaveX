from core.kernel import RuntimeKernel, get_runtime_kernel
from core.ir.unified_runtime_ir import compile_unified_runtime_ir


def test_kernel_initialization():
    kernel = RuntimeKernel(runtime_type="browser")
    result = kernel.run_pipeline(tick=0, options={"semantic": False, "sync": False, "memory": False, "execution": False, "reconstruction": False})
    assert result["bounded"] is True
    assert "unified_ir" in result


def test_unified_ir_determinism():
    ir = compile_unified_runtime_ir(registry={"phases": {}}, graph={"nodes": [], "edges": []})
    ir2 = compile_unified_runtime_ir(registry={"phases": {}}, graph={"nodes": [], "edges": []})
    assert ir == ir2


def test_get_runtime_kernel_singleton():
    a = get_runtime_kernel("browser")
    b = get_runtime_kernel("browser")
    assert a is b
