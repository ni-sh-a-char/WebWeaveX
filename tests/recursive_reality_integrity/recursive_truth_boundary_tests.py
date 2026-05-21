from core.evidence.recursive_truth_boundary_engine import model_recursive_truth_boundaries


def test_closure_not_allowed():
    b = model_recursive_truth_boundaries(5, 0)
    assert b["closure_allowed"] is False
