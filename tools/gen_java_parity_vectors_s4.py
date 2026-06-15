#!/usr/bin/env python3
"""Session-4 cross-language golden vectors from canonical Python 2.1.0.

Run from a materialized Python-branch checkout (so `core` is importable):

    python tools/gen_java_parity_vectors_s4.py <out.json>

Covers the connector-runtime extraction family (the deterministic, portable subset
of the Extraction layer): extract_database_runtime / extract_api_runtime /
extract_runtime_streams / extract_telemetry_runtime. Each entry stores the inputs
plus the canonical `stable_serialize` of the Python output and its
`compute_kaalka_hash`; the Java test reconstructs inputs, recomputes, and asserts
byte-equality.
"""
from __future__ import annotations

import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.connectors.api_connector_engine import extract_api_runtime
from core.connectors.database_connector_engine import extract_database_runtime
from core.connectors.runtime_stream_connector_engine import extract_runtime_streams
from core.connectors.telemetry_connector_engine import extract_telemetry_runtime


def entry(name, inputs, value):
    return {
        "name": name,
        "inputs": inputs,
        "serialized": stable_serialize(value),
        "hash": compute_kaalka_hash(value),
    }


def db(name, database_type, snapshot):
    return entry(name, {"database_type": database_type, "snapshot": snapshot},
                 extract_database_runtime(database_type=database_type, snapshot=snapshot))


def api(name, api_type, snapshot):
    return entry(name, {"api_type": api_type, "snapshot": snapshot},
                 extract_api_runtime(api_type=api_type, snapshot=snapshot))


def streams(name, stream_types, snapshot):
    return entry(name, {"stream_types": stream_types, "snapshot": snapshot},
                 extract_runtime_streams(stream_types=stream_types, snapshot=snapshot))


def telemetry(name, backends, snapshot):
    return entry(name, {"backends": backends, "snapshot": snapshot},
                 extract_telemetry_runtime(backends=backends, snapshot=snapshot))


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 4: connector-runtime extraction)"}

    pg_full = {
        "schemas": ["public", "audit"],
        "tables": ["zeta", "alpha", "Mu", "alpha"],
        "indexes": [{"name": "ix_a"}],
        "metrics": {"qps": 12, "cache_hit": 0.9},
        "active_connections": 7,
        "replication_state": "streaming",
        "degraded": False,
    }
    out["extract_database_runtime"] = [
        db("db_pg_default", "postgresql", None),
        db("db_pg_alias", "postgres", pg_full),
        db("db_mysql", "mysql", {"tables": ["t2", "t10", "t1"], "active_connections": 3,
                                 "replication_state": "semi-sync"}),
        db("db_sqlite", "sqlite", {"tables": ["b", "a"], "indexes": [{"name": "x"}]}),
        db("db_redis", "redis", {"keys": ["k2", "k1"], "clients": 4, "role": "replica",
                                 "streams": ["s1"], "metrics": {"mem": 100}}),
        db("db_redis_floatconn", "redis", {"clients": 4.9}),  # int() truncation
        db("db_unknown", "MongoDB", None),                    # -> degraded
        db("db_empty_snap", "postgresql", {}),
    ]

    out["extract_api_runtime"] = [
        api("api_rest_default", "rest", None),
        api("api_rest_full", "REST", {
            "endpoints": ["/z", "/a", "/m"],
            "schemas": [{"name": "S"}],
            "auth": {"type": "oauth"},
            "rate_limits": {"rpm": 600},
            "responses": [{"code": 200}],
            "pagination": [{"kind": "cursor"}],
        }),
        api("api_graphql", "graphql", {
            "endpoints": ["/gql", "/graphql"],
            "graphql": {"endpoints": ["/v2/graphql"], "schemas": [{"t": 1}],
                        "types": ["User", "Account", "user"]},
        }),
        api("api_graphql_default_sub", "graphql", None),
        api("api_grpc", "grpc", {
            "grpc": {"services": ["Svc.B", "Svc.A"], "methods": ["m2", "m1"],
                     "protobuf": ["a.proto"]},
        }),
    ]

    full_stream_snap = {
        "kafka": {"topics": ["t-b", "t-a"], "consumers": [{"g": "c1"}],
                  "offsets": {"t-a": 5}, "state": "rebalancing", "lineage": [{"e": 1}]},
        "redis": {"streams": ["rs1", "rs2"]},
        "websocket": {"connections": [{"id": "w1"}], "frames": 12},
    }
    out["extract_runtime_streams"] = [
        streams("st_default", None, full_stream_snap),
        streams("st_kafka_only", ["kafka"], {"kafka": {"topics": ["b", "a"]}}),
        streams("st_sse_queue", ["sse", "queue"],
                {"sse": {"topics": ["e1"]}, "queue": {"topics": ["q1", "q2"]}}),
        streams("st_unknown", ["mqtt", "amqp"], None),   # nothing appended
        streams("st_empty_param", [], full_stream_snap),  # [] -> default order
        streams("st_ws_default", ["websocket"], None),
    ]

    out["extract_telemetry_runtime"] = [
        telemetry("tel_default", None, None),
        telemetry("tel_full", ["jaeger", "prometheus", "datadog"], {
            "metrics": [{"m": 1}], "traces": [{"t": 1}],
            "spans": [{"s": 1}, {"s": 2}], "logs": [{"l": 1}],
            "correlations": [{"c": 1}], "degraded": False,
        }),
        telemetry("tel_empty_backends", [], None),       # [] -> default backends
        telemetry("tel_degraded", ["prometheus"], {"degraded": True}),
    ]

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s4.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors {counts}\n")


if __name__ == "__main__":
    main()
