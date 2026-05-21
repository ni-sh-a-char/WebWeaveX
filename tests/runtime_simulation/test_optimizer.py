from core.optimizer import optimize_semantic_ir


def test_optimizer_dedup():

    ir = {
        "execution_paths": {
            "paths": [
                ["a"],
                ["a"],
            ]
        }
    }

    r = optimize_semantic_ir(ir)

    assert (
        len(
            r["optimized_ir"][
                "execution_paths"
            ]["paths"]
        )
        == 1
    )
