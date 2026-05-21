from core.evidence.recursive_exploration_decay_engine import resist_exploration_decay
from core.evidence import structure_cognition
from tests.civilizational_epistemic_openness.openness_helpers import assert_openness_bundle


def test_exploration_decay_resisted():
    r = resist_exploration_decay(exploratory=True, depth=3)
    assert r["resist"] is True


def test_bundle_exploration_decay():
    r = structure_cognition({"a": 1}, {"b": 2}, {"a": 1}, ambiguities=["q"])
    assert_openness_bundle(r)
    assert r["exploration_decay_resisted"] is True
