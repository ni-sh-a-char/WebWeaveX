from core.repository.ast import analyze_source_ast, parse_python_ast


def test_python_ast_calls():
    source = "import os\ndef main():\n    os.getcwd()\n"
    result = parse_python_ast(source)
    assert result["language"] == "python"
    assert any(c["target"] == "getcwd" for c in result["calls"])


def test_ast_cognition_deterministic():
    source = "class App:\n    pass\n"
    first = analyze_source_ast(source, path="app.py")
    second = analyze_source_ast(source, path="app.py")
    assert first == second
