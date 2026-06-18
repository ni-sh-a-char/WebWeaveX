#!/usr/bin/env python3
"""Session-7 cross-language golden vectors from canonical Python 2.1.0.

Run from a materialized Python-branch checkout (so `core` is importable):

    python tools/gen_java_parity_vectors_s7.py <out.json>

Covers the remaining dependency-clean connector-runtime cluster (manifest Complete +
executable_proven): extract_container_runtime / extract_ide_runtime /
extract_kubernetes_runtime. Each entry stores the inputs plus the canonical
`stable_serialize` of the Python output and its `compute_kaalka_hash`.
"""
from __future__ import annotations

import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.connectors.container_connector_engine import extract_container_runtime
from core.connectors.ide_connector_engine import extract_ide_runtime
from core.connectors.kubernetes_connector_engine import extract_kubernetes_runtime


def entry(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def container(name, runtime, snapshot):
    return entry(name, {"runtime": runtime, "snapshot": snapshot},
                 extract_container_runtime(runtime=runtime, snapshot=snapshot))


def ide(name, ide_name, snapshot):
    return entry(name, {"ide": ide_name, "snapshot": snapshot},
                 extract_ide_runtime(ide=ide_name, snapshot=snapshot))


def k8s(name, snapshot):
    return entry(name, {"snapshot": snapshot}, extract_kubernetes_runtime(snapshot=snapshot))


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 7: container/ide/kubernetes connectors)"}

    out["extract_container_runtime"] = [
        container("ct_docker_default", "docker", None),                       # empty/default
        container("ct_docker_full", "docker", {                              # full + ordering
            "containers": [{"id": "c1"}], "images": ["img-z", "img-a", "Img-M"],
            "volumes": ["v1"], "networks": ["n1"], "states": {"c1": "running"},
            "health": {"c1": "healthy"}, "degraded": False}),
        container("ct_podman_alias", "podman", {"images": ["z", "a"]}),       # alias -> runtime=podman
        container("ct_oci_alias", "OCI", {}),                                # alias + upper-case
        container("ct_unknown_degraded", "containerd", None),                # unknown -> degraded
        container("ct_unicode_images", "docker", {                           # unicode ordering
            "images": ["镜像", "\U0001F600img", "aaa"]}),
        container("ct_degraded_passthrough", "docker", {"degraded": "partial"}),  # non-bool passthrough
    ]

    out["extract_ide_runtime"] = [
        ide("ide_default", "vscode", None),                                  # empty/default
        ide("ide_full", "intellij", {                                        # full + ordering + nested
            "open_files": ["z.py", "a.py", "M.py"], "terminals": [{"id": 1}],
            "tabs": ["tab1", "tab2"], "workspace": {"root": "/proj", "name": "x"},
            "debug_sessions": [{"session": "s1"}], "degraded": False}),
        ide("ide_degraded_passthrough", "vscode", {"degraded": "partial"}),  # malformed/passthrough
        ide("ide_unicode", "vscode", {                                       # unicode sort
            "open_files": ["文件.py", "a.py", "\U0001F600.py"]}),
        ide("ide_empty_snapshot", "neovim", {}),                            # edge: empty dict
    ]

    out["extract_kubernetes_runtime"] = [
        k8s("k8s_default", None),                                            # default namespaces=["default"]
        k8s("k8s_full", {                                                    # full + ordering + nested
            "namespaces": ["prod", "default", "Dev"],
            "pods": [{"name": "zeta"}, {"name": "alpha"}, {"name": "Mu"}],
            "deployments": [{"name": "d2"}, {"name": "d1"}],
            "services": [{"name": "svc"}], "ingress": [{"host": "h"}],
            "topology": {"prod": ["zeta"]}, "events": [{"e": 1}, {"e": 2}], "degraded": False}),
        k8s("k8s_nameless_pod", {                                            # mutation: nameless pod -> str(dict) sort key
            "pods": [{"name": "b"}, {"x": 1}, {"name": "a"}]}),
        k8s("k8s_unicode_ns", {"namespaces": ["命名", "alpha", "\U0001F600"]}),
        k8s("k8s_degraded", {"degraded": True}),                            # boundary
        k8s("k8s_empty_snapshot", {}),                                       # edge: empty dict
    ]

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s7.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors {counts}\n")


if __name__ == "__main__":
    main()
