<p align="center">
  <img src="https://img.shields.io/badge/WebWeaveX-v2.0.0-0f172a?style=for-the-badge&logo=python&logoColor=white" alt="WebWeaveX v2.0.0"/>
</p>

<p align="center">
  <strong>Deterministic Universal Runtime Extraction &amp; Cognition Infrastructure</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/webweavex/"><img src="https://img.shields.io/pypi/v/webweavex?style=flat-square" alt="PyPI"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-2ea44f?style=flat-square" alt="Apache 2.0"/></a>
  <img src="https://img.shields.io/badge/tests-671%20passed-22c55e?style=flat-square" alt="Tests"/>
  <img src="https://img.shields.io/badge/build-passing-22c55e?style=flat-square" alt="Build"/>
  <img src="https://img.shields.io/badge/coverage-meaningful%20suite-6366f1?style=flat-square" alt="Coverage"/>
  <img src="https://img.shields.io/badge/runtime-deterministic-2563eb?style=flat-square" alt="Deterministic"/>
  <img src="https://img.shields.io/badge/persistence-Kaalka-7c3aed?style=flat-square" alt="Kaalka"/>
  <img src="https://img.shields.io/badge/open%20source-Apache%202.0-f97316?style=flat-square" alt="Open Source"/>
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-64748b?style=flat-square" alt="Platforms"/>
</p>

<p align="center">
  <a href="https://buymeacoffee.com/piyushmishra00"><img src="https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support%20WebWeaveX-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me A Coffee"/></a>
</p>

---

# WebWeaveX v2.0.0

**Extract runtimes — not just pages.**  
WebWeaveX is open infrastructure that turns live systems into **structured, replay-safe operational cognition** — then rebuilds portable runtime reality from that cognition.

> **For developers:** deterministic APIs, bounded graphs, Kaalka-encrypted persistence.  
> **For teams:** SaaS monitoring, workflow extraction, distributed runtime federation.  
> **For AI systems:** stable schemas, sorted graphs, explicit phase IR — no hidden probabilistic state.

---

## What WebWeaveX is not

| | |
|---|---|
| ❌ A scraper | You get cognition graphs and replay packages — not raw HTML hoarding |
| ❌ A browser bot | Playwright is optional; the product is the **runtime fabric** |
| ❌ An OCR utility | Documents are one ingress channel among many |
| ❌ An AI wrapper | **No LLM required** for core extraction, memory, or execution |

## What WebWeaveX is

| | |
|---|---|
| ✅ Universal extraction engine | Web, SaaS, repos, native, streams, connectors |
| ✅ Runtime cognition system | Semantic → workflow → sync → evolution → memory |
| ✅ Deterministic replay engine | Same inputs → identical graphs and lineage |
| ✅ Cross-runtime operational graph | One merged `build_runtime_graph()` substrate |
| ✅ Runtime reconstruction fabric | Cognition → portable operational twins |
| ✅ Foundation for Anything OS | Portable realities from structured runtime IR |

---

## Why WebWeaveX exists

Most tools extract **pages**, **screenshots**, or **HTML**.

WebWeaveX extracts **runtimes**:

| Extracted | Meaning |
|-----------|---------|
| Workflows | What the system actually does over time |
| Applications | Forms, dashboards, modals, action graphs |
| Live streams | WebSockets, SSE, DOM mutation timelines |
| Operational state | Sessions, sync deltas, execution queues |
| Runtime cognition | Unified IR across every phase |

**Sources WebWeaveX understands:**

- Websites & JS-rendered SaaS dashboards  
- Authenticated multi-tenant applications  
- Git repositories (AST-level cognition)  
- PDFs, images & multimodal documents  
- Electron, native desktop & terminal runtimes  
- APIs, databases, containers & Kubernetes  
- Distributed worker meshes & federated memory  

---

## Install

```bash
pip install webweavex
```

```bash
pip install "webweavex[browser]"
pip install "webweavex[full]"
```

---

## Real usage (actual APIs)

### Browser extraction

```python
from webweavex import extract_web

result = extract_web("https://example.com")
graph = result["unified_runtime_graph"]
print(len(graph.get("nodes", [])), "nodes")
```

### Authenticated SaaS extraction

```python
from webweavex import extract_web

result = extract_web(
    "https://app.example.com",
    authenticated=True,
    session_path="session.enc",
    encryption_key="master-key",
    semantic_runtime=True,
)
print(result["authenticated"], result["bounded"])
```

### Repository cognition

```python
from webweavex import extract_repository

repo = extract_repository("./project")
print(repo.get("bounded", True))
```

### Runtime reconstruction

```python
from webweavex import reconstruct_runtime

runtime = reconstruct_runtime(
    semantic_ir={"ir": "semantic_runtime", "domain": "app"},
    workflow_ir={"ir": "workflow_runtime", "objective": "monitor"},
    runtime_type="browser",
    tick=0,
)
print(runtime["runtime_id"], runtime["reconstructed"])
```

### Distributed extraction

```python
from webweavex import run_autonomous_extraction

payload = run_autonomous_extraction(
    tasks=[{"task_id": "worker-1", "url": "https://example.com"}],
    distributed_runtime=True,
    federated_memory=True,
    execution_runtime=True,
    reconstruction_runtime=True,
)
print(payload["autonomous"], payload["bounded"])
```

### Runtime kernel (full pipeline)

```python
from webweavex import RuntimeKernel

kernel = RuntimeKernel(runtime_type="browser")
out = kernel.run_pipeline(
    tick=0,
    options={
        "semantic": True,
        "memory": True,
        "execution": True,
        "reconstruction": True,
    },
)
print(out["unified_ir"]["ir"])
```

More examples: [`examples/`](examples/)

---

## Architecture

```
┌──────────────┐
│    Input     │  URL · repo · native · stream · connector
└──────┬───────┘
       ▼
┌──────────────────────────────────────────────────┐
│           Universal Runtime Kernel               │
│                  core/kernel/                    │
└──────┬───────────────────────────────────────────┘
       │
       ├─► Extraction (browser / native / repo / multimodal)
       ├─► Cognition (semantic · workflow · causality)
       ├─► Synchronization (continuous sync · evolution)
       ├─► Memory (federated knowledge fabric)
       ├─► Execution (bounded action sandbox)
       └─► Reconstruction (portable operational reality)
       │
       ▼
┌──────────────────────────────────────────────────┐
│         Unified Runtime Graph (deterministic)     │
└──────────────────────────────────────────────────┘
```

Deep dive: [docs/architecture.md](docs/architecture.md) · [docs/kernel.md](docs/kernel.md)

---

## Powered by Kaalka

WebWeaveX persists operational state with the **[Kaalka Encryption Algorithm](https://github.com/PIYUSH-MISHRA-00/Kaalka-Encryption-Algorithm)**.

| Property | Benefit |
|----------|---------|
| Deterministic encryption | Same JSON + same key → **same ciphertext** |
| Canonical normalization | `sort_keys=True` before encrypt |
| Cross-language consistency | Python, JS, Go, Rust, Java, WASM fixtures |
| Replay-safe persistence | Sessions, checkpoints, memory survive restore |

```python
from webweavex import encrypt_value, decrypt_value
```

[docs/kaalka.md](docs/kaalka.md)

---

## Determinism & safety

**No** LLM-dependent extraction · **No** probabilistic agents · **No** `eval` / `exec` in the execution sandbox · **No** unbounded graph growth without policy caps.

**Yes** SHA-256 runtime IDs · sorted edges · tick-indexed history · bounded queues (100k actions) · Kaalka checkpoints.

---

## Performance & quality

| Metric | v2.0.0 |
|--------|--------|
| Tests | **671 passing** |
| Runtime graphs | Bounded (policy-enforced) |
| Replay | Identical on canonical inputs |
| Distributed | Worker federation + sync-aware execution |

```bash
pytest -q
python -m build
```

---

## Enterprise use cases

- **SaaS monitoring** — authenticated dashboard cognition & replay  
- **Security runtime analysis** — structural graphs without unsafe automation  
- **Distributed operations** — federated extraction across workers  
- **Runtime observability** — streams, mutations, connector topology  
- **Workflow extraction** — autonomous objectives & execution plans  
- **Platform intelligence** — repository AST + dependency surfaces  
- **Runtime reconstruction** — operational twins for staging & DR  
- **Automation infrastructure** — deterministic execution fabric under policy  

---

## Open source

WebWeaveX v2.0.0 is licensed under **[Apache License 2.0](LICENSE)**.

Commercial use, modification, and distribution are **explicitly allowed**.

---

## Documentation

| Document | Description |
|----------|-------------|
| [architecture.md](docs/architecture.md) | System design |
| [kernel.md](docs/kernel.md) | Runtime kernel |
| [extraction.md](docs/extraction.md) | Extraction entry points |
| [api-reference.md](docs/api-reference.md) | Public API surface |
| [security.md](docs/security.md) | Security model |
| [kaalka.md](docs/kaalka.md) | Encryption layer |
| [ROADMAP.md](ROADMAP.md) | Release roadmap |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guide |
| [SECURITY.md](SECURITY.md) | Report vulnerabilities |

---

## Roadmap

- Native bindings (UIA, AX, AT-SPI, Electron DevTools)  
- Distributed mesh quorum & checkpoint replication  
- WWX declarative runtime language CLI  
- **Anything OS** — portable operational reality packaging  

See [ROADMAP.md](ROADMAP.md).

---

## Support WebWeaveX

If this project saves you weeks of fragile scraping and non-replayable automation:

**☕ [Buy Me A Coffee](https://buymeacoffee.com/piyushmishra00)**

---

<p align="center">
  <sub><strong>WebWeaveX v2.0.0</strong> — Truth from systems, not guesses.</sub>
</p>
