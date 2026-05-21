from __future__ import annotations

from typing import Any, Dict

from core.runtime.runtime_proof_engine import prove_runtime_consistency
from core.runtime.runtime_reconciliation_engine import reconcile_runtime_states


def check_runtime_consistency(
    runtime_a: Dict[str, Any],
    runtime_b: Dict[str, Any],
    transitions: list | None = None,
    evidence: list | None = None,
) -> Dict[str, Any]:
    recon = reconcile_runtime_states(runtime_a, runtime_b)
    proof = prove_runtime_consistency(transitions or [], evidence or [])
    return {
        "reconciliation": recon,
        "proof": proof,
        "consistent": len(recon.get("conflicts", [])) == 0 and proof.get("valid", False),
        "deterministic": True,
    }
