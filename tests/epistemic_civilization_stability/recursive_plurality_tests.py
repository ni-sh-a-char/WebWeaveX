from core.evidence.plurality_decay_engine import resist_plurality_decay


def test_plurality_decay_resisted():
    r = resist_plurality_decay(1, 4)
    assert r["resist"] is True
