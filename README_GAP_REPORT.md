# README_GAP_REPORT.md

> Measured 2026-06-10 by comparing `README.md` (dart) against `origin/python:README.md`
> and `origin/javascript:README.md` (header extraction + line counts).

## Size comparison

| Branch | Lines | `##` sections |
|--------|------:|--------------:|
| **Dart (current)** | **231** | **19** |
| Python | 698 | ~33 |
| JavaScript | 841 | ~42 |

The Dart README is ~1/3 the size of Python's and ~1/4 of JavaScript's. It is coherent and
on-message but materially thinner, and omits several sections that both sibling branches —
and the mission's Phase 10 checklist — require.

## Sections the Dart README HAS

What is WebWeaveX? · Humans and AI agents · Why AI agents need deterministic runtime
infrastructure · What WebWeaveX is NOT · Why existing systems fail · Runtime cognition ·
Runtime memory · Replay equivalence · Runtime reconstruction · Authenticated runtime
continuation · Cross-language parity · Architecture · Quick start (humans) · AI agent usage ·
Determinism · Validation · Security · Roadmap · License.

## Missing sections (gap vs Phase 10 checklist + sibling READMEs)

| Required section | In Python? | In JS? | In Dart? | Priority |
|------------------|:----------:|:------:|:--------:|----------|
| Installation (pub.dev `dart pub add`) | ✓ | ✓ | ❌ | **High** — pub.dev landing essential |
| Features (capability bullets) | ✓ | ✓ | partial | High |
| API Reference (public symbol index) | ✓ | ✓ | ❌ | **High** |
| Examples (multiple worked examples) | ✓ | ✓ | partial (one quick start) | High |
| Performance / benchmarks | ✓ | ✓ | ❌ | Medium |
| Testing (how to run, counts) | ✓ | ✓ | ❌ | Medium |
| Coverage (badge + figure) | ✓ | ✓ | ❌ | Medium |
| CI/CD (gates, workflows) | ✓ | ✓ | ❌ | Medium |
| Pub.dev Release (package metadata, version) | n/a | n/a | ❌ | **High** (Dart-specific) |
| Contributing (section, not just link) | ✓ | ✓ | ❌ | Medium |
| OSS Governance | ✓ | ✓ | ❌ | Medium |
| Graph Intelligence | ✓ | ✓ | partial | Medium |
| Workflows | ✓ | ✓ | ❌ | Medium |
| Vision / Long-Term Vision | ✓ | ✓ | ❌ | Medium |
| Repository structure | ✓ | ✓ | ❌ | Low |

## Recommendation

Rewrite `README.md` to the full Phase 10 structure (Overview → Why → Features → Architecture →
Installation → Quick Start → per-subsystem sections → API Reference → Examples → Performance →
Testing → Coverage → CI/CD → Pub.dev Release → Contributing → OSS Governance → Security →
Roadmap → Vision), keeping the existing strong "runtime cognition" narrative and adding the
Dart-specific Installation / Pub.dev / Testing / Coverage / CI blocks with the **measured**
numbers from this validation run (779 tests, 97.23% coverage, all gates green, 77/126 parity).

This is a **fully achievable** gap — no platform constraints — and is the highest-leverage
single fix on the branch.
