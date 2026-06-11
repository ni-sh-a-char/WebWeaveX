"""Million-vector certification — Python runner.

Streams 1,000,000 deterministic vectors (seeded 64-bit LCG, no time/machine
state) through a battery spanning extraction / semantic IR / repository IR /
runtime IR / application(deployment) IR, folds each vector's canonical hash
(v2 contract: compute_kaalka_hash) into one rolling SHA-256, and emits
{count, family_counts, family_digests, final_digest}.

Usage: PYTHONPATH=<python-branch> python mv_python.py [count] > mv_python.json
"""
import hashlib
import json
import sys

from core.browser.html_semantic_extraction_engine import extract_semantic_html
from core.crypto.kaalka_hash_engine import compute_kaalka_hash as H
from core.evidence.uncertainty_engine import model_uncertainty
from core.graph.topology_proof_engine import prove_topology
from core.repository.api_surface_reasoning_engine import reason_api_surface
from core.repository.deployment_semantics_engine import analyze_deployment_semantics
from core.repository.infra_semantic_engine import detect_infra_signals
from core.semantic.ambiguity_pressure_engine import compute_ambiguity_pressure

MASK = (1 << 64) - 1
A = 6364136223846793005
C = 1442695040888963407
W = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta"]
F = ["Dockerfile", "k8s/deploy.yaml", "src/main.py", "README.md",
     "helm/chart.yaml", ".github/workflows/ci.yml", "infra/main.tf",
     "docs/guide.md"]
METHODS = ["get", "post", "delete"]


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    state = 20260612

    def rnd():
        nonlocal state
        state = (state * A + C) & MASK
        return (state >> 33) & 0x7FFFFFFF

    acc = hashlib.sha256()
    fam_counts = {}
    fam_acc = {k: hashlib.sha256() for k in
               ("extraction", "semantic", "repository", "runtime",
                "application")}

    for i in range(n):
        if i % 20 == 0:
            fam = "extraction"
            t = W[rnd() % 8]
            h1 = W[rnd() % 8]
            p1 = W[rnd() % 8]
            p2 = W[rnd() % 8]
            extra = rnd() % 2
            html = (f"<html><head><title>{t}</title></head><body>"
                    f"<h1>{h1}</h1><p>{p1} {p2}</p>"
                    + (f"<ul><li>{W[rnd() % 8]}</li></ul>" if extra else "")
                    + "</body></html>")
            out = extract_semantic_html(html)
        else:
            k = i % 6
            if k == 0:
                fam = "semantic"
                out = model_uncertainty(rnd() % 8, rnd() % 8, rnd() % 8)
            elif k == 1:
                fam = "semantic"
                cnt = rnd() % 5
                out = compute_ambiguity_pressure([W[rnd() % 8]
                                                  for _ in range(cnt)])
            elif k == 2:
                fam = "repository"
                cnt = rnd() % 4
                paths = {}
                for j in range(cnt):
                    # explicit order: Python evaluates assignment RHS before
                    # the subscript key, which would desync the LCG vs JS/Dart
                    key = f"/p{j}_{rnd() % 50}"
                    paths[key] = {METHODS[rnd() % 3]: {}}
                out = reason_api_surface({"paths": paths})
            elif k == 3:
                fam = "repository"
                cnt = rnd() % 6
                out = detect_infra_signals([F[rnd() % 8] for _ in range(cnt)])
            elif k == 4:
                fam = "runtime"
                cnt = rnd() % 6
                out = prove_topology({"edges": [
                    {"from": W[rnd() % 8], "to": W[rnd() % 8]}
                    for _ in range(cnt)]})
            else:
                fam = "application"
                cnt = rnd() % 6
                out = analyze_deployment_semantics(
                    [F[rnd() % 8] for _ in range(cnt)])
        h = H(out)
        b = (h + "\n").encode("ascii")
        acc.update(b)
        fam_acc[fam].update(b)
        fam_counts[fam] = fam_counts.get(fam, 0) + 1
        if (i + 1) % 100000 == 0:
            print(f"  py {i + 1}", file=sys.stderr)

    print(json.dumps({
        "count": n,
        "family_counts": {k: fam_counts.get(k, 0) for k in sorted(fam_acc)},
        "family_digests": {k: v.hexdigest() for k, v in sorted(fam_acc.items())},
        "final_digest": acc.hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
