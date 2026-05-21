from core.evidence.truth_boundary_engine import model_truth_boundaries


def test_coherence_normalization_blocked():
    b = model_truth_boundaries([])
    assert b["coherence_normalization_allowed"] is False
