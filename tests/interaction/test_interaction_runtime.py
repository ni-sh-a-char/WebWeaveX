from core.interaction import build_interaction_plan, record_interaction


def test_interaction_plan():
    plan = build_interaction_plan([
        {
            "type": "click",
            "selector": "#submit",
        }
    ])

    assert len(plan["interaction_plan"]) == 1
    assert plan["interaction_plan"][0]["action"] == "click"


def test_record_interaction_deterministic():
    first = record_interaction("click", "#a", step=0)
    second = record_interaction("click", "#a", step=0)

    assert first == second
