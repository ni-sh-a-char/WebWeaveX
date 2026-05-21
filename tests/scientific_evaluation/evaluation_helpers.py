def assert_substrate_ir(ir: dict, keys: list) -> None:
    for k in keys:
        assert k in ir, f"missing IR key: {k}"
