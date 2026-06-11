"""Phase 13: micro-benchmark — canonical serialize + hash + encrypt throughput."""
import json
import sys
import time

sys.path.insert(0, r"C:\Projects\wwx_cert_py")
from core.determinism.normalization import stable_serialize
from core.crypto.kaalka_runtime_engine import compute_deterministic_hash, encrypt_value

PAYLOAD = {"title": "Benchmark payload — café 中文 🚀", "items": [{"id": i, "score": i / 7.0, "tags": ["a", "b", "c"]} for i in range(50)], "nested": {"depth": {"x": [1, 2.5, None, True]}}}
N = 2000

t0 = time.perf_counter()
for i in range(N):
    stable_serialize({**PAYLOAD, "i": i})
t1 = time.perf_counter()
for i in range(N):
    compute_deterministic_hash({**PAYLOAD, "i": i})
t2 = time.perf_counter()
for i in range(N // 10):
    encrypt_value({**PAYLOAD, "i": i}, "bench-key")
t3 = time.perf_counter()

print(json.dumps({
    "language": "python",
    "serialize_ops_per_s": round(N / (t1 - t0)),
    "hash_ops_per_s": round(N / (t2 - t1)),
    "encrypt_ops_per_s": round((N // 10) / (t3 - t2)),
}))
