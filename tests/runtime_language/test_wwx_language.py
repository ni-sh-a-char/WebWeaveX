from core.runtime_language import compile_wwx, interpret_wwx, parse_wwx, validate_wwx


def test_wwx_parse_and_validate():
    source = "EXTRACT browser.app.dashboard\nSYNC runtime.cluster\nREPLAY workflow.monitoring"
    parsed = parse_wwx(source)
    assert validate_wwx(parsed)["valid"] is True
    compiled = compile_wwx(parsed)
    assert compiled["compiled"] is True
    assert len(compiled["plan"]["steps"]) == 3


def test_wwx_interpreter_deterministic():
    source = "EXECUTE action.click"
    first = interpret_wwx(source, tick=1)
    second = interpret_wwx(source, tick=1)
    assert first == second
