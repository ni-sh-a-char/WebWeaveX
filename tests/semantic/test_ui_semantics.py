from core.semantic.ui_semantics_engine import extract_ui_semantics


def test_ui_semantics_auth():
    html = """
    <html><nav><a href='/'>Home</a></nav>
    <form><input name='password'><button>Login</button></form>
    <button>Delete Account</button>
    """

    ui = extract_ui_semantics(html)

    assert ui["authentication"] is True
    assert ui["destructive_actions"]
