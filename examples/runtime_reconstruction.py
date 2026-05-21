"""Runtime reconstruction example."""

from webweavex import run_reconstruction_for_extraction

if __name__ == "__main__":
    out = run_reconstruction_for_extraction(
        reconstruction_runtime=True,
        sources={"semantic_ir": {"ir": "semantic_runtime", "domain": "app"}},
        fabricate_runtime=True,
    )
    print("valid:", out.get("validation", {}).get("valid"))
