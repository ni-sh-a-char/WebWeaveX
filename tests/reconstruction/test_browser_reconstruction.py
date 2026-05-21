from core.reconstruction.browser_reconstruction_engine import reconstruct_browser_runtime


def test_browser_replay():
    browser_ir = {"url": "https://example.com", "navigation": {"history": [{"path": "/", "order": 0}]}}
    interaction_ir = {"tab_states": {"tabs": [{"path": "/"}]}, "interactions": [{"type": "click"}]}

    first = reconstruct_browser_runtime(browser_ir=browser_ir, interaction_ir=interaction_ir)
    second = reconstruct_browser_runtime(browser_ir=browser_ir, interaction_ir=interaction_ir)

    assert first == second
    assert first["replay_safe"] is True
    assert first["tabs"]
