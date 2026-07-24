# WebWeaveX — Human Engineering Onboarding Guide

WebWeaveX provides human engineers, security auditors, QA automation teams, and system architects with a reliable operational substrate.

---

## 1. Onboarding Paths

```
  ┌─────────────────────────────────────────────────────────────┐
  │ 🔰 Beginner Path                                            │
  │ Learn UniversalInput, run_canonical_pipeline, and basic IR  │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ ⚡ Intermediate Path                                         │
  │ Authenticated continuation, Kaalka session management       │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │ 🔬 Advanced / Enterprise Path                               │
  │ Graph diffing, cross-run replay proofs, security auditing   │
  └─────────────────────────────────────────────────────────────┘
```

---

## 2. Step-by-Step Developer Tutorials

### Tutorial A: Basic Web Application Extraction

```python
from webweavex import UniversalInput, run_canonical_pipeline

# 1. Define target site
input_spec = UniversalInput(source="https://news.ycombinator.com", source_type="web")

# 2. Run pipeline
output = run_canonical_pipeline(input_spec)

# 3. Inspect deterministic metrics
print("=== Extraction Summary ===")
print(f"Graph Node Count : {len(output.graph.nodes)}")
print(f"Pipeline Hash   : {output.pipeline_hash}")
print(f"DOM Hash        : {output.fingerprint.dom_hash}")
```

---

### Tutorial B: State Diffing Across Deployments

Human QA engineers use WebWeaveX to verify that a web application deployment introduced no unintended state regressions:

```python
from webweavex import UniversalInput, run_canonical_pipeline

def audit_deployment_diff(staging_url: str, production_url: str):
    staging_res = run_canonical_pipeline(UniversalInput(source=staging_url, source_type="web"))
    prod_res = run_canonical_pipeline(UniversalInput(source=production_url, source_type="web"))
    
    if staging_res.pipeline_hash == prod_res.pipeline_hash:
        print("✅ Staging and Production topologies are mathematically EQUIVALENT!")
    else:
        print("⚠️ Structural divergence detected between Staging and Production!")
        print(f"Staging Hash: {staging_res.pipeline_hash}")
        print(f"Prod Hash   : {prod_res.pipeline_hash}")
```

---

## 3. Migration Guide: From Scrapers to WebWeaveX

| Feature | Legacy Scraper (BeautifulSoup / Puppeteer) | WebWeaveX Substrate |
|:---|:---|:---|
| **Element Selection** | Fragile CSS selectors (`.btn-primary-v2`) | Deterministic node IDs based on canonical topology |
| **Auth Handling** | Re-login script on every run | Kaalka v5 encrypted session continuation |
| **Output Type** | Loose HTML strings | Strict typed JSON graph + SHA-256 state hash |
| **Error Handling** | Unhandled DOM mutation crashes | Graceful degradation with explicit policy bounds |

---

## 4. Troubleshooting & FAQ for Humans

### Q: What if an application uses auto-generated CSS classes (e.g. Styled-Components / Emotion)?
WebWeaveX's **DOM Stabilization engine** automatically strips volatile dynamic CSS classes and auto-generated attributes before computing node identities, ensuring stable hashes across builds.

### Q: How do I store session tokens securely?
Always write session objects into WebWeaveX using Kaalka v5 encryption wrapper. Never dump session dicts to raw plaintext files or unencrypted caches.
