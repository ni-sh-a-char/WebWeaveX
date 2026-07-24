<p align="center">
  <br/>
  <img src="https://img.shields.io/badge/WebWeaveX-v3.0.1-0f172a?style=for-the-badge&logo=python&logoColor=white" alt="WebWeaveX v3.0.1"/>
  <br/><br/>
  <strong>Production-grade deterministic runtime cognition infrastructure<br/>for humans and AI agents</strong>
  <br/>
  <em>Operational runtime substrate · PyPI · replay-safe · Kaalka v5 parity</em>
  <br/><br/>
</p>

<p align="center">
  <a href="https://pypi.org/project/webweavex/"><img src="https://img.shields.io/pypi/v/webweavex?style=flat-square&logo=pypi&logoColor=white" alt="PyPI version"/></a>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+"/>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-2EA44F?style=flat-square" alt="Apache 2.0"/></a>
  <img src="https://img.shields.io/badge/tests-815%20passing-22c55e?style=flat-square" alt="Tests passing"/>
  <img src="https://img.shields.io/badge/coverage-88%25%2B%20scoped-6366f1?style=flat-square" alt="Coverage 90%+"/>
  <img src="https://img.shields.io/badge/build-passing-22c55e?style=flat-square" alt="Build passing"/>
  <img src="https://img.shields.io/badge/deterministic%20runtime-0ea5e9?style=flat-square" alt="Deterministic runtime"/>
  <img src="https://img.shields.io/badge/replay--safe-14b8a6?style=flat-square" alt="Replay-safe"/>
  <img src="https://img.shields.io/badge/Kaalka-verified-7c3aed?style=flat-square" alt="Kaalka verified"/>
  <img src="https://img.shields.io/badge/production%20ready-15803d?style=flat-square" alt="Production ready"/>
  <img src="https://img.shields.io/badge/OSS-infrastructure-64748b?style=flat-square" alt="Open Source"/>
</p>

<p align="center">
  <a href="https://buymeacoffee.com/piyushmishra00"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Support%20WebWeaveX-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee"/></a>
</p>

<p align="center">
  <br/>
</p>

---

## Contents

- [What is WebWeaveX?](#what-is-webweavex)
- [Humans and AI agents](#humans-and-ai-agents)
- [Why AI agents need this](#why-ai-agents-need-deterministic-runtime-infrastructure)
- [What WebWeaveX is NOT](#what-webweavex-is-not)
- [Why existing systems fail](#why-existing-systems-fail)
- [Core capabilities](#core-capabilities)
- [Authenticated runtime continuation](#authenticated-runtime-continuation)
- [Architecture](#architecture)
- [Canonical pipeline](#canonical-pipeline)
- [Quick start](#quick-start)
- [Code examples](#real-code-examples)
- [Determinism](#determinism)
- [Validation](#real-validation)
- [Security](#security-model)
- [Architecture guarantees](#architecture-guarantees)
- [Contributing](#contributing)

---

## What is WebWeaveX?

> **WebWeaveX is to runtime state what Git is to source code: deterministic, replayable, reconstructable, and auditable.**
>
> Modern operational systems generate runtime state that is typically lost, difficult to reproduce, and impossible to validate. WebWeaveX transforms that runtime state into deterministic artifacts that humans and AI agents can continue, reconstruct, replay, and verify.

**WebWeaveX** is **deterministic runtime cognition infrastructure** for **humans and AI agents** operating on authenticated software. It captures how systems actually run—browser DOM, sessions, Electron, native UI, workflows, connectors—and compiles **replay-safe runtime graphs** with **Kaalka-encrypted persistence** (`webweavex-formula+kaalka@5.0.0`).

This is **not** a scraping library or LLM wrapper. It is an **operational runtime substrate** for extraction, memory, execution, reconstruction, and replay equivalence.

Ecosystem portal: [`main`](https://github.com/ni-sh-a-char/WebWeaveX) · npm sibling: [`javascript`](https://github.com/ni-sh-a-char/WebWeaveX/tree/javascript)

### Why it exists

Modern systems are **authenticated**, **stateful**, **runtime-driven**, **SPA-based**, **Electron-based**, **synchronized**, and **operationally dynamic**. Operators need continuity across runs, not another HTML snapshot.

Traditional extraction fails because it is:

| Failure mode | Consequence |
|--------------|-------------|
| HTML-only parsing | Misses hydration, storage, IPC, native UI |
| Stateless requests | Loses session and workflow continuity |
| No authenticated persistence | Re-login and drift between runs |
| No replay contract | Cannot prove equivalence after rebuild |
| No reconstruction | Cannot rebuild operational topology from IR |
| Weak SPA/Electron support | Unstable IDs, routes, and storage break diffs |

WebWeaveX exists to deliver **deterministic runtime extraction** and **replay-safe operational reconstruction** through one **canonical pipeline**.

---

## Universal Runtime Extraction

WebWeaveX is not merely a scraping library — it is a **runtime extraction and cognition substrate**. It transforms heterogeneous operational sources into deterministic runtime representations through one canonical pipeline.

| Source | Runtime Representation |
|--------|------------------------|
| Websites | Runtime graph |
| SPAs | Stabilized runtime state |
| Browser sessions | Replay-safe artifacts |
| APIs | Operational topology |
| Documents | Unified IR |
| Repositories | Dependency intelligence |
| Runtime systems | Memory fabric |

Every source converges on the same bounded, hashable, replayable runtime IR.

---

## Web Extraction Without Fragility

Most extraction systems focus on collecting content. WebWeaveX focuses on preserving runtime state. Traditional scraping breaks when authentication expires, SPA frameworks re-render, runtime identifiers change, workflows span sessions, or replay must be validated later.

| Extraction Challenge | Traditional Approach | WebWeaveX |
|----------------------|----------------------|-----------|
| SPA instability | Re-scrape repeatedly | Runtime stabilization |
| Authenticated workflows | Start over | Runtime continuation |
| Session portability | Manual export | Encrypted runtime persistence |
| Validation | Manual inspection | Replay equivalence |
| Recovery | Re-run workflow | Runtime reconstruction |

The result is extraction that can be continued, replayed, reconstructed, and verified.

---

## Humans and AI agents

**WebWeaveX is designed for both humans and AI agents.**

| Audience | Use |
|----------|-----|
| **Engineers** | Inspect authenticated systems, preserve workflows, audit runtime behavior |
| **AI agents** | Maintain continuity, deterministic state, replay-safe memory, environment reconstruction |

Same APIs, same determinism contract, same honesty about authorization.

---

## Why AI Agents Need WebWeaveX

Browser and operational agents interact with systems that change continuously. Without deterministic runtime infrastructure, agents lose context between actions.

| Agent Failure Mode | Operational Impact | WebWeaveX Capability |
|--------------------|--------------------|----------------------|
| Lost browser state | Re-authentication | Runtime continuation |
| Lost workflow context | Restart execution | Runtime memory fabric |
| DOM instability | Broken selectors | DOM stabilization |
| Replay drift | Non-repeatable behavior | Replay equivalence |
| Session expiration | Lost progress | Encrypted persistence |
| Workflow interruption | Incomplete execution | Runtime reconstruction |

WebWeaveX provides a deterministic runtime layer beneath agents so operational state becomes persistent, replayable, and auditable.

---

## Why AI agents need deterministic runtime infrastructure

| Problem | Without substrate | With WebWeaveX |
|---------|-------------------|----------------|
| LLMs lose state | Re-plan from scratch each turn | Stable runtime memory + graph identity |
| Browser agents lose auth | Re-login drift | Authorized session continuation (Kaalka) |
| Workflows go nondeterministic | Unauditable actions | Replay equivalence + fingerprints |
| Operational systems are opaque | HTML-only views | Runtime cognition IR + reconstruction |
| Cross-run reasoning breaks | Ephemeral DOM | Stabilized hashes + parity-validated crypto |

WebWeaveX provides the **deterministic operational runtime layer** agents and teams share—not autonomous superintelligence.

---

## What WebWeaveX is NOT

WebWeaveX is **not**:

| Category | Clarification |
|----------|----------------|
| **Auth bypass tooling** | Does not defeat MFA, CAPTCHA, or login controls |
| **Malware or exploit infrastructure** | Not designed for unauthorized access |
| **Credential theft tooling** | Does not harvest secrets you do not already hold |
| **CAPTCHA bypass software** | No circumvention of bot defenses |
| **Browser exploitation tooling** | Not a vulnerability framework |
| **AGI or “autonomous hacking”** | No probabilistic agent that “figures out” sites |
| **Hacking infrastructure** | No unauthorized intrusion features |
| **An LLM wrapper** | Core path is deterministic; optional plugins fail safe |
| **A chatbot** | Infrastructure library, not conversational AI |

WebWeaveX only operates on **authorized authenticated runtimes** and data **you explicitly provide**.

---

## Why existing systems fail

| System | Strength | Limitation for operational runtime |
|--------|----------|-----------------------------------|
| **BeautifulSoup** | Fast static HTML parse | No live session, storage, or runtime graph |
| **Selenium** | Browser automation | No unified IR, Kaalka fabric, or replay equivalence layer |
| **Playwright** | Reliable browser control | Automation driver—not extraction + memory + reconstruction |
| **Puppeteer** | Chromium scripting | Same gap: no federated sync or deterministic checkpoints |
| **Stateless crawlers** | Scale on public pages | Poor on authenticated operational systems |
| **Probabilistic-only agents** | Flexible tasks | Weak replay, memory, and audit guarantees |

Common gaps WebWeaveX addresses:

- Lack of **runtime continuity** across processes
- Lack of **replay** and fingerprint equivalence
- Lack of **authenticated persistence** (encrypted, deterministic)
- Lack of **reconstruction** from structured IR
- Lack of **synchronization** between browser, semantic, workflow, and memory layers

---

## How WebWeaveX Differs

| Tool | Primary Focus |
|------|---------------|
| Playwright | Browser automation |
| Scrapy | Crawling |
| BeautifulSoup | HTML parsing |
| Firecrawl | Extraction |
| LangChain | LLM orchestration |
| CrewAI | Agent orchestration |
| WebWeaveX | Deterministic runtime cognition infrastructure |

WebWeaveX does not replace these systems. It provides deterministic runtime infrastructure that can sit beneath them.

---

## Runtime Cognition Infrastructure

WebWeaveX introduces a category beyond traditional scraping, browser automation, or agent orchestration.

> Infrastructure that captures, stabilizes, fingerprints, reconstructs, and continues operational runtime state through deterministic contracts.

| Category | Focus |
|----------|-------|
| Browser automation | Execute actions |
| Web scraping | Extract content |
| Agent orchestration | Coordinate reasoning |
| Runtime cognition infrastructure | Preserve operational runtime state |

WebWeaveX works alongside existing ecosystems rather than replacing them.

---

## Core capabilities

| Capability | Description |
|------------|-------------|
| **Browser runtime extraction** | Bounded Playwright capture, network/session envelopes |
| **SPA stabilization** | DOM and route stabilization for framework noise |
| **Electron extraction** | Routes, IPC, storage metadata, deterministic Electron hash |
| **Native runtime cognition** | Desktop, terminal, VM, remote (graceful OS fallbacks) |
| **Terminal runtime** | Shell-oriented cognition fixtures |
| **Distributed extraction** | Autonomous workers + Kaalka checkpoints |
| **Runtime causality** | Event chains and propagation in extraction fabrics |
| **Semantic cognition** | Entities, ontology, semantic graphs |
| **Workflow runtime** | Plans, objectives, workflow memory |
| **Synchronization runtime** | Multi-source runtime alignment |
| **Reconstruction engine** | Replay-safe rebuild from IR |
| **Federated memory** | Deterministic merge and stable hashes |
| **Execution sandbox** | Allowlisted actions only |
| **Runtime replay** | `validate_replay_equivalence()` |
| **Runtime graph** | Normalized universal runtime graph |
| **Deterministic fingerprints** | Global and pipeline hashes |
| **Authenticated runtime continuation** | Encrypted session reload |
| **Kaalka v5 crypto (cross-language)** | `webweavex-formula+kaalka@5.0.0` — verified vs `javascript` branch |
| **Connector runtime fabric** | Database, API, container, K8s, telemetry (bounded) |

---

## Authenticated runtime continuation

Modern applications authenticate with **cookies**, **localStorage**, **sessionStorage**, **tokens**, **runtime identity**, and **cross-navigation continuity**. Electron adds **IndexedDB metadata**, **IPC**, and **route state**. Multi-tab products add **synchronization state** across surfaces.

WebWeaveX supports:

- **Encrypted authenticated session persistence** (`save_encrypted_session`, session paths on `extract_web`)
- **Runtime continuation** across extractions when you supply the same Kaalka key and session file
- **Deterministic replay-safe reconstruction** of operational graphs from IR

Persistence uses **Kaalka v5 deterministic encryption** (`algorithm: webweavex-formula+kaalka@5.0.0`)—not plaintext JSON checkpoints on disk.

| Stored surface | Mechanism |
|----------------|-----------|
| Cookies / headers | Encrypted session store |
| Browser snapshot | Session + identity engines |
| Electron storage | Native/Electron cognition (bounded) |
| Workflow / sync state | Kaalka checkpoint engines |

**WebWeaveX does not:** bypass auth, defeat MFA, bypass security controls, or access systems without authorization.

**WebWeaveX only operates on authorized authenticated runtimes explicitly provided by the user.**

```python
from webweavex import extract_web

result = extract_web(
    "https://app.example.com/dashboard",
    authenticated=True,
    session_path="./session.kaalka",
    encryption_key="your-kaalka-master-key",
)
```

---

## Runtime Lifecycle

```text
Capture → Normalize → Fingerprint → Graph → Memory → Replay Validation → Reconstruction → Continuation
```

Every WebWeaveX runtime moves through this bounded lifecycle: captured state is normalized and fingerprinted, compiled into a runtime graph and memory fabric, validated for replay equivalence, then reconstructed and continued.

---

## Cross-Language Determinism

WebWeaveX ships as two independent products — Python (`pip install webweavex`) and JavaScript (`npm install webweavex`) — that conform to one shared `specification/`. They share byte-identical deterministic contracts:

| Contract | Verified |
|----------|----------|
| Kaalka hashing | byte-identical Python ⇄ JavaScript |
| Global runtime fingerprint | byte-identical Python ⇄ JavaScript |
| Runtime graph structure | structurally equal |
| Encrypted value persistence | byte-identical Python ⇄ JavaScript |

See `CROSS_LANGUAGE_PARITY_REPORT.md` for the measured per-capability status. Neither implementation invokes the other at runtime; parity is proven against the specification, not by cross-runtime calls.

---

## Architecture

```
                              ┌──────────────────┐
                              │      Input       │
                              │  UniversalInput  │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Canonical Pipeline│
                              │ run_canonical_    │
                              │   pipeline()      │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Runtime Cognition │
                              │ web·native·repo   │
                              └────────┬─────────┘
                                       │
           ┌───────────────────────────┼───────────────────────────┐
           ▼                           ▼                           ▼
    ┌─────────────┐            ┌─────────────┐            ┌─────────────┐
    │  Semantic   │            │  Causality  │            │  Workflow   │
    │   Layer     │            │   Layer     │            │  Runtime    │
    └──────┬──────┘            └──────┬──────┘            └──────┬──────┘
           │                          │                          │
           └──────────────────────────┼──────────────────────────┘
                                      ▼
                             ┌─────────────────┐
                             │ Synchronization │
                             │    Runtime      │
                             └────────┬────────┘
                                      ▼
                             ┌─────────────────┐
                             │ Federated Memory│
                             └────────┬────────┘
                                      ▼
                             ┌─────────────────┐
                             │ Execution Fabric│
                             └────────┬────────┘
                                      ▼
                             ┌─────────────────┐
                             │ Reconstruction  │
                             │    Engine       │
                             └────────┬────────┘
                                      ▼
                             ┌─────────────────┐
                             │ Universal Runtime│
                             │     Graph        │
                             └─────────────────┘
```

Source: [`core/kernel/runtime_pipeline.py`](core/kernel/runtime_pipeline.py)

---

## Canonical pipeline

Single production execution path—no shadow orchestrators.

```python
from webweavex import UniversalInput, run_canonical_pipeline

result = run_canonical_pipeline(
    UniversalInput(source="https://example.com", source_type="web"),
)

print(result["pipeline_hash"])
print(len(result["unified_runtime_graph"].get("nodes", [])))
```

| Property | Detail |
|----------|--------|
| Single execution path | `run_canonical_pipeline()` only |
| Deterministic normalization | `RuntimeGraphContract.normalize()` |
| Replay-safe runtime | Fingerprint at pipeline boundary |
| Canonical IR generation | Per-kind extraction → kernel phases |

---

## Quick start

```bash
pip install webweavex
pip install "webweavex[browser]"
pip install "webweavex[full]"
```

```bash
python -c "import webweavex; print(webweavex.__version__)"
# 3.0.1
```

---

## Core Capabilities

WebWeaveX exposes one deterministic engine across six cognition domains. Every
output is a bounded, hashable, replayable IR.

| Domain | Capabilities | Representative public APIs |
|--------|--------------|----------------------------|
| **Extraction** | Bounded web/SPA/Electron capture, structured content, runtime envelopes | `extract_web`, `run_canonical_pipeline`, `universal_extract` |
| **Documents** | Document IR; structure, citation, and discourse analysis | `extract_docs`, `compile_document`, `query_documents` |
| **Repositories** | Repository IR; dependency, build, and topology intelligence | `extract_repository`, `compile_repository`, `query_repository` |
| **Runtime** | Runtime graphs, memory fabric, replay equivalence, reconstruction | `build_runtime_graph`, `validate_replay_equivalence`, `run_reconstruction_runtime` |
| **Applications** | Application cognition, runtime objectives, session memory | `run_application_cognition`, `execute_runtime_objective` |
| **Cognition** | Causality, semantic, synchronization, evolution, workflows, execution | `run_semantic_runtime`, `run_causality_runtime`, `run_autonomous_workflow` |
| **Determinism** | Canonical normalization, stable serialization, fingerprints, Kaalka v5 | `compute_global_runtime_fingerprint`, `encrypt_value` |
| **Cross-language parity** | Byte-identical hashes across Python · JavaScript · Dart | `fingerprint`, `compute_kaalka_hash` |

---

## Common Workflows

```python
from webweavex import (
    UniversalInput, run_canonical_pipeline,
    extract_web, extract_docs, extract_repository,
    query_semantics, run_application_cognition,
)

# Extract structured content
content = extract_web("https://example.com")

# Analyze documents
doc_ir = extract_docs("./report.pdf")

# Analyze repositories
repo_ir = extract_repository("./my-project")

# Query semantic IR
semantics = query_semantics("entities", repo_ir)

# Runtime reasoning
pipeline = run_canonical_pipeline(
    UniversalInput(source="https://example.com", source_type="web"),
)
print(pipeline["pipeline_hash"])

# Application cognition
app = run_application_cognition(
    url="https://app.example.com",
    html="<html>...</html>",
)
```

---

## Supported Platforms

| Aspect | Detail |
|--------|--------|
| Runtime | CPython **3.10 – 3.13** |
| Operating systems | Linux · macOS · Windows (OS-independent core) |
| Install | `pip install webweavex` (extras: `[browser]`, `[full]`) |
| Optional | Playwright (browser), tree-sitter (parsers), OCR / ingestion extras |

---

## Versioning

WebWeaveX follows [Semantic Versioning](https://semver.org) — **MAJOR.MINOR.PATCH**.
The version is **synchronized across all three implementations**: PyPI, npm, and
pub.dev share the same `3.0.1`, so a given version number denotes the same
certified deterministic contract in every language. MAJOR marks a breaking change,
MINOR adds backward-compatible capability, PATCH is a fix. The internal engine
contract version (`v1_phase_14`) is independent of the package version and changes
only when the deterministic wire format changes.

---

## Real code examples

<details>
<summary><strong>Browser, auth, replay, semantic, reconstruction, distributed, native</strong></summary>

### Browser extraction

```python
from webweavex import extract_web, compute_global_runtime_fingerprint

out = extract_web("https://example.com")
print(out.get("bounded"), compute_global_runtime_fingerprint(out))
```

### Authenticated runtime persistence

```python
from webweavex import save_encrypted_session, extract_web

save_encrypted_session(
    "./session.kaalka",
    {"cookies": [], "headers": {}, "auth_tokens": []},
    "your-kaalka-master-key",
)

out = extract_web(
    "https://app.example.com",
    authenticated=True,
    session_path="./session.kaalka",
    encryption_key="your-kaalka-master-key",
)
```

Runnable: [`examples/authenticated_extraction.py`](examples/authenticated_extraction.py)

### Replay equivalence

```python
from webweavex import validate_replay_equivalence

assert validate_replay_equivalence(original, replayed)["equivalent"]
```

### Semantic runtime

```python
out = extract_web("https://example.com", semantic_runtime=True)
```

### Reconstruction

```python
from webweavex import run_reconstruction_runtime

rebuilt = run_reconstruction_runtime(
    sources={"extraction": prior},
    runtime_type="browser",
)
```

### Distributed extraction

```python
from webweavex import run_autonomous_extraction

out = run_autonomous_extraction(
    tasks=[{"task_id": "t1", "url": "https://example.com", "priority": 0}],
)
```

### Native extraction

```python
from webweavex import extract_native

out = extract_native(runtime="desktop", application="notepad")
```

</details>

---

## Determinism

| Mechanism | Role |
|-----------|------|
| `compute_global_runtime_fingerprint()` | Cross-run runtime digest |
| `validate_replay_equivalence()` | Graph + fingerprint + topology checks |
| `compute_stable_dom_hash()` | DOM meaning stable under attribute noise |
| SPA stabilizer | Framework route/state freeze |
| `stable_memory_hash()` | Ordered federated memory merge |
| Kaalka `encrypt_value` | UTF-8 → `derive_kaalka_time_key` → Kaalka v5 `_proc` → base64 |

**Cross-language parity (verified):** `validation/parity/javascript_vectors.json` vs Python output — normalization, serialization, SHA-256 hash, and ciphertext **match** the `javascript` branch. Spec: [`docs/architecture/CROSS_LANGUAGE_PARITY.md`](docs/architecture/CROSS_LANGUAGE_PARITY.md).

```bash
PYTHONPATH=. python validation/validate_cross_language_parity.py
```

**Honest limitations:** live SPA fetches may differ run-to-run; parity applies to the **canonical formula**, not wall-clock Kaalka CLI encryption without a fixed derived time key.

---

## Reconstruction engine

WebWeaveX reconstructs **operational structure** from runtime IR:

- Runtime topology and unified graphs
- Workflow and application memory views
- Browser/application state envelopes
- Semantic operational graphs

| Property | Meaning |
|----------|---------|
| Runtime reconstruction | IR → bounded runtime view |
| Operational graph rebuilding | Normalized nodes/edges |
| Replay-safe reconstruction | Tested equivalence paths |
| Deterministic recreation | Sorted, canonical structures |

This is **not** full machine cloning or sci-fi simulation—it is **auditable operational recreation** for engineering workflows.

---

## Real validation

<details>
<summary><strong>Validation commands and CI gates</strong></summary>

| Metric | Value |
|--------|--------|
| Tests | **815 passing** (`pytest -q`) |
| Scoped coverage | **≥ 90%** (production packages in `pyproject.toml`) |
| Wheel | `webweavex-3.0.1-py3-none-any.whl` |
| Replay | `validate_replay_equivalence` suite |
| Determinism | Kaalka cross-language + fingerprint tests |
| Playwright | Browser extraction paths (optional extra) |
| Native | Orchestrator + platform fallbacks |
| Distributed | Autonomous extraction tests |

```bash
pytest -q
python -m build
python validation/final_production_master.py
```

</details>

---

## Security model

| Control | Implementation |
|---------|----------------|
| Allowlisted execution | `core/execution/` sandbox |
| No arbitrary eval/exec | Forbidden in production paths |
| Sandboxed runtime | Bounded simulate/rollback |
| Deterministic persistence | Kaalka-only checkpoints |
| Encrypted memory/session | `encrypt_value`, session wrappers |
| Replay-safe recovery | Deterministic reload envelopes |

See [SECURITY.md](SECURITY.md). Report issues responsibly.

---

## Architecture guarantees

| Guarantee | How |
|-----------|-----|
| **Deterministic outputs** | Canonical ordering, stable hashes |
| **Replay-safe persistence** | Kaalka + equivalence validation |
| **Bounded execution** | Explicit `bounded: True` contracts |
| **Graceful degradation** | Playwright/native/connectors fail soft |
| **Canonical normalization** | Graph and DOM contracts |
| **Stable graph generation** | `build_runtime_graph` + normalize |
| **Cross-language consistency** | Kaalka reference vectors |

Contract document: [WEBWEAVEX_v2_ARCHITECTURE_LOCK_REPORT.md](WEBWEAVEX_v2_ARCHITECTURE_LOCK_REPORT.md)

---

## Repository structure

```
WebWeaveX/
├── core/           # Runtime infrastructure (kernel, browser, memory, sync, …)
├── webweavex/      # Public Python package
├── tests/          # 815 tests
├── docs/           # Architecture, API, security, Kaalka, replay, validation
├── examples/       # Runnable scripts
├── validation/     # Production and real-world validators
└── .github/        # CI, templates, code of conduct, funding
```

| Package | Role |
|---------|------|
| `core/kernel/` | Canonical pipeline, `RuntimeKernel` |
| `core/browser/` | Web extraction, DOM/SPA stabilization |
| `core/crypto/` | Kaalka engines |
| `core/memory/` | Federated memory fabric |
| `core/synchronization/` | Sync runtime |
| `core/reconstruction/` | Reconstruction orchestrator |
| `core/replay/` | Replay equivalence |
| `webweavex/` | Stable public API |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [.github/CODE_OF_CONDUCT.md](.github/CODE_OF_CONDUCT.md).

| Rule | Requirement |
|------|-------------|
| Determinism | No `random` / `uuid4` in runtime paths |
| Replay safety | Preserve graph normalization semantics |
| Canonical pipeline | No parallel mega-orchestrators |
| Persistence | Kaalka for new checkpoints |
| Tests | `pytest -q` must pass; coverage gate ≥ 90% scoped |

---

## Long-Term Vision

WebWeaveX aims to be a **deterministic runtime substrate** — a shared operational layer that runtime state can be captured into, reasoned over, and continued from. The goal is a common foundation for humans, AI agents, workflows, operational systems, and distributed cognition systems. It is infrastructure, not an application: the same deterministic contract serves every consumer.

---

## Future Direction

WebWeaveX is evolving toward a shared runtime substrate where operational state can move between humans, workflows, services, and AI agents without losing determinism.

Future areas include:

* broader language parity
* deeper runtime graph intelligence
* expanded connector ecosystems
* stronger replay guarantees
* larger runtime memory fabrics
* distributed operational cognition

> Runtime state should be as reproducible, portable, and verifiable as source code.

---

## Roadmap

See [ROADMAP.md](ROADMAP.md).

**v2.1 focus:**

- Deeper native bindings (UIA, AX, AT-SPI)
- Distributed runtime infrastructure hardening
- Stronger SPA normalization
- Real connector runtimes (live Postgres, Redis, K8s validation)
- Native OS integrations behind optional extras

---

## API Reference

The complete public API surface — every function, its parameters, and its
cross-language parity classification (Complete / Partial / Deferred) — is in
[API_REFERENCE.md](API_REFERENCE.md), generated from `PARITY_MANIFEST.json`
(portable-API parity gap: **0**).

---

## Cross-language parity & certification

Three implementations — **Python (canonical, PyPI)**, **JavaScript (npm)**,
**Dart (pub.dev)** — byte-identical on the certified surface. Every claim is
regenerated by execution; nothing passes on the strength of a report:

| Proof | Scale | Result |
|---|---|---|
| Core determinism | 10k vectors × 3 runs × 3 languages | 60,001/60,001 byte-identical |
| Extraction | 10k synthetic + 1,006 real pages + 14 torture | 3-way PASS |
| Semantic IR (layers A–O + parsers + repository + application) | 667 fixtures, ~300 engines | 3-way hash + deep equality |
| Million-vector battery | 1,000,000 vectors across 5 IR families | single aggregate digest, identical in all 3 |

The full model, reproduction commands, and current verdict:
[CERTIFICATION.md](CERTIFICATION.md) and `final_certification.json`.
Per-API status: [API_REFERENCE.md](API_REFERENCE.md) (generated from
`PARITY_MANIFEST.json`).

## AI-agent usage

WebWeaveX is built to be operated *by* AI agents as much as by humans: every
output is a bounded, deterministic, evidence-carrying IR that an agent can
hash, diff, replay, and reason over without screenshots or DOM diffing.
Agents contributing to the codebase should start at
[AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md) — architecture map, determinism rules,
the cross-language pitfalls catalogue, and the certification workflow.

## Limitations

- **Network/live-browser APIs are Partial by design** — the `extract*` /
  `crawl*` family and five bounded APIs have certified deterministic cores;
  their live side effects are out of certification scope.
- **Platform-bound APIs are Deferred** — live-page capture and OS-coupled
  native cognition (`extract_native`, `run_native_cognition`) branch on the
  host OS even in Python and cannot be made cross-platform-deterministic.
- **Valid-Python AST enrichment is Python-only** — the certified JS/Dart
  contract takes the parse-error fallback for `parse_ast` on valid Python
  (see ARCHITECTURE.md, "The AST contract").

## License

Apache 2.0 — see [LICENSE](LICENSE).

---

## Final positioning

**WebWeaveX is deterministic runtime cognition infrastructure for humans and AI agents**—operational runtime substrate for the authenticated web, not a crawler, not an LLM wrapper, not AGI hype.

If this work helps your team, consider supporting it:

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-piyushmishra00-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/piyushmishra00)

---

<p align="center">
  <sub>Documentation · <a href="docs/README.md">docs/</a> · <a href="examples/README.md">examples/</a> · <a href="WEBWEAVEX_v2_RELEASE_REPORT.md">release report</a></sub>
</p>
