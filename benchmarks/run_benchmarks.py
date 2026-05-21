from __future__ import annotations

import time
import tracemalloc
from webweavex import extract, extract_async, fingerprint
from core.crypto.kaalka_engine import hex_fingerprint
from core.repository.repository_intelligence import analyze_repository
from core.repository.dependency_graph_engine import build_dependency_graph
from core.serialize.deterministic_serializer import dumps_deterministic
from webweavex import crawl, query_graph
import asyncio


def run_sync():
    sample = "Hello\n```py\nimport os\n```"
    tracemalloc.start()
    t0 = time.perf_counter()
    out = extract(sample)
    t1 = time.perf_counter()
    g0 = time.perf_counter()
    _ = out.get("relationships", {}).get("execution_graph", {})
    g1 = time.perf_counter()
    f0 = time.perf_counter()
    _ = hex_fingerprint(out)
    _ = fingerprint(out)
    f1 = time.perf_counter()
    r0 = time.perf_counter()
    _ = analyze_repository(sample)
    r1 = time.perf_counter()
    d0 = time.perf_counter()
    _ = build_dependency_graph(sample)
    d1 = time.perf_counter()
    s0 = time.perf_counter()
    _ = dumps_deterministic(out)
    s1 = time.perf_counter()
    c0 = time.perf_counter()
    crawled = crawl("https://example.com", max_pages=1)
    c1 = time.perf_counter()
    q0 = time.perf_counter()
    _ = query_graph(out)
    q1 = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "extraction_s": t1 - t0,
        "graph_s": g1 - g0,
        "fingerprint_s": f1 - f0,
        "repository_extraction_s": r1 - r0,
        "dependency_graph_s": d1 - d0,
        "serializer_s": s1 - s0,
        "recursive_crawl_s": c1 - c0,
        "graph_query_s": q1 - q0,
        "crawl_pages": len(crawled.get("visited", [])),
        "memory_peak_bytes": peak,
    }


async def run_async():
    t0 = time.perf_counter()
    await asyncio.gather(*[extract_async(f"quick async check {i}") for i in range(8)])
    dt = time.perf_counter() - t0
    return {"async_s": dt, "async_throughput_per_s": round(8 / dt, 3) if dt else 0.0}


if __name__ == "__main__":
    print(run_sync())
    print(asyncio.run(run_async()))
