# Contributing to WebWeaveX

Thank you for contributing to **WebWeaveX**, the universal runtime cognition infrastructure for humans and AI agents.

---

## 1. Quick Setup

```bash
git clone https://github.com/ni-sh-a-char/WebWeaveX.git
cd WebWeaveX
pip install -e ".[dev,browser]"
playwright install chromium   # Optional for browser runtime tests
```

---

## 2. Pre-PR Checklist

Before opening a pull request:

```bash
# 1. Run unit test suite
pytest -q

# 2. Verify import & version
python -c "import webweavex; assert webweavex.__version__ == '2.0.0'"

# 3. Test package build
python -m build
```

- Scoped production coverage must remain **≥ 90%**.
- All cross-language parity tests must pass.

---

## 3. Core Architectural Invariants

1. **Canonical Pipeline Only:** All runtime cognition behaviors must route through `run_canonical_pipeline()` or an explicit phase orchestrator. No parallel shadow orchestrators.
2. **Determinism:** No `random`, `uuid4`, or wall-clock timestamps in persisted or hashed data structures.
3. **Kaalka v5 Persistence:** Operational checkpoints must use Kaalka v5 AES-256-GCM encryption (`algorithm: kaalka`). Plaintext or pickle persistence is forbidden.
4. **Replay Equivalence:** Identical inputs must yield identical SHA-256 graph hashes across Python, JavaScript, Dart, Java, and Kotlin.
5. **No Side Effects on Import:** `import webweavex` must not launch background network connections or browser instances.

---

## 4. Submitting Pull Requests

Please fill out the PR template in `.github/PULL_REQUEST_TEMPLATE.md` with complete details.
