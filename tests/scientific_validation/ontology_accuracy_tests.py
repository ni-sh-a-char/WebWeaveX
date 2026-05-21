from benchmarks.evaluators import eval_ontology_consistency


def test_ontology_benchmark_case():
    case = {"input": {"edges": [{"from": "a", "to": "b", "evidence": ["e"]}]}, "expected": {"consistent": True}}
    assert eval_ontology_consistency(case)["predicted"] is True
