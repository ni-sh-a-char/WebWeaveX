from core.application.dashboard_runtime_engine import build_dashboard_runtime


def test_dashboard_detection():
    html = """
    <div class='widget'>Revenue: 100</div>
    <table><tr><th>A</th></tr><tr><td>1</td></tr></table>
    <canvas></canvas>
    """

    first = build_dashboard_runtime(html)
    second = build_dashboard_runtime(html)

    assert len(first["widgets"]) == len(second["widgets"])
    assert first["tables"]
