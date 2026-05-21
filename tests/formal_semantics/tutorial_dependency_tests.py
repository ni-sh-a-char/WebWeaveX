from core.documents.tutorial_dependency_engine import reconstruct_tutorial_dependencies


def test_tutorial_deps():
    r = reconstruct_tutorial_dependencies("# Step 1\n\n## Step 2\n")
    assert isinstance(r, dict)
