# JAVA_BRANCH_POLICY

**Branch identity and contribution rules for the `java` branch.**

This branch is one of four ecosystem-native expressions of a single deterministic
contract:

```
Python  =  Java  =  JavaScript  =  Dart
```

The two invariants below are held simultaneously and are non-negotiable:

1. **Behavioural parity** — Java output is byte-identical to canonical Python for every
   API marked complete.
2. **Structural identity** — the `java` branch looks and builds like a native Maven /
   JVM project; no foreign-ecosystem build, source, or release artifacts at the root.

---

## 1. Maven-first

- The build is **Maven**. The authoritative build descriptor is
  [`java/pom.xml`](java/pom.xml); the published artifact is
  `io.webweavex:webweavex:2.1.0` on **Maven Central**.
- Target runtime is **Java 17+** (CI matrix: JDK 17 and 21).
- The deterministic core depends on the **JDK alone** (`java.text.Normalizer`,
  `MessageDigest`, `Base64`). Third-party libraries must never be able to perturb
  canonical bytes. Jackson is permitted as a **test-only** dependency (golden-vector
  loading).
- **No Dart, JavaScript, or Python build/source/release artifacts** may be added at the
  repo root: no `pubspec.yaml` / `.pubignore` / `analysis_options.yaml`, no `package.json`
  / `.npmignore`, no `pyproject.toml` / `setup.py` / wheels, no Dart/JS/Python CI.
  Historical examples are preserved under [`docs/archive/`](docs/archive/).
- The root [`README.md`](README.md) must read as a Java project. It may **name** the
  sibling ecosystems (Python/JS/Dart) in the parity table, but must not contain
  foreign **install commands or version badges** (`dart pub add`, `npm install`,
  `pip install`, pub.dev/Dart badges). This is machine-enforced — see §5.

## 2. Python is canonical

- The **Python branch is the single source of behavioural truth.** When Java and the
  Dart/JS wrappers disagree, **Java conforms to Python**, never to a Dart- or
  JS-specific symbol or behaviour.
- APIs are ported **directly from the Python `core/`** canon (e.g.
  `core.determinism.*`, `core.ir.*`, `core.crypto.*`), not transcribed from the Dart or
  JavaScript ports. Some Dart/JS public symbols intentionally diverge from Python; those
  divergences are not reproduced.
- [`PARITY_MANIFEST.json`](PARITY_MANIFEST.json) (the shared 128-API surface) is the
  single source of truth for *which* APIs exist; it is not edited to suit Java.

## 3. Parity vectors are mandatory

> **No feature lands in Java without Python parity vectors.**

Every new public API must, in the same change set:

1. Be **implemented from the Python canon** — no behaviour invented in Java.
2. Ship **Python-generated golden vectors** under
   `java/src/test/resources/parity/` (produced by a `tools/gen_java_parity_vectors*.py`
   generator that imports the canonical Python `core`).
3. Add a **parity test** (`io.webweavex.parity.CrossLanguageParity*Test`) asserting Java
   output is byte-identical to the recorded Python output.
4. Update [`java/JAVA_PARITY_MATRIX.md`](java/JAVA_PARITY_MATRIX.md) (regenerated, not
   hand-edited) to mark the API **Implemented (parity-proven)**.
5. Update the governance validator mapping in
   [`tools/validate_java_manifest.py`](tools/validate_java_manifest.py).

## 4. Proof, not assertion

> **No API is marked complete without parity proof.**

- "Complete" / "Implemented (parity-proven)" means a green parity test exists that
  compares Java against recorded **Python** output. A passing unit test alone is not
  proof of parity.
- Parity is transitive: because Python ≡ JavaScript ≡ Dart is already certified, proving
  **Java ≡ Python** proves **Java ≡ JS ≡ Dart** for that API.
- Coverage, build-green, and test-green are necessary but **not sufficient** to claim an
  API complete (see the completion gate in the session mission).

## 5. No stubs. No placeholders. No TODO implementations.

- A class or method may not be committed in a non-functional state to "reserve" an API.
- Forbidden in shipped `src/main`: `TODO`, `FIXME`, `throw new UnsupportedOperationException`
  used as a placeholder, empty method bodies standing in for real logic, or returning
  fabricated/hard-coded values to satisfy a test.
- A planned API stays **absent** from the matrix's "Implemented" set (and from the
  validator mapping) until it is genuinely implemented and parity-proven. The matrix
  marks it `⬜ Planned`.

## 6. Machine-enforced invariants

These rules are enforced in CI by
[`tools/validate_java_manifest.py`](tools/validate_java_manifest.py) and the workflows
[`java-build.yml`](.github/workflows/java-build.yml),
[`java-parity.yml`](.github/workflows/java-parity.yml), and
[`parity-regression.yml`](.github/workflows/parity-regression.yml). The build/PR **fails** on:

| # | Failure condition |
| --- | --- |
| 1 | A proven API absent from `PARITY_MANIFEST.json` |
| 2 | A mapped Java class file that does not exist (matrix entry → missing source) |
| 3 | A proven API with no golden-vector section (untested) |
| 4 | A proven API not documented in `JAVA_PARITY_MATRIX.md` |
| 5 | Matrix proven-count ≠ validator mapping size (drift) |
| 6 | README references a foreign ecosystem's install command or badge (pub/Dart/npm/pip) |
| 7 | An implemented Java package undocumented in the matrix |
| 8 | A proven API whose golden-vector file is loaded by no parity test |
| 10 | Source ↔ matrix drift: a mapped class with no proven row, or a proven row not mapped to source |

Plus the regression gate: instruction coverage must stay **≥ 94 %** and the
parity-proven API count must **never decrease** (floor 17).

## 7. Release discipline

- Version is **synchronized** across all four implementations (`2.1.0` = the same
  certified deterministic contract everywhere). Bump in lockstep.
- `mvn -Prelease verify` GPG-signs artifacts for Maven Central; releases follow
  [RELEASE.md](RELEASE.md).
- Each session produces a certification artifact under `java/` (e.g.
  `SESSION_N_CERTIFICATION.{md,json}`) and the branch-level
  [`JAVA_BRANCH_CERTIFICATION.md`](JAVA_BRANCH_CERTIFICATION.md), with evidence
  regenerated by execution.

---

_Provenance: this policy accompanies the Maven-first cleanup recorded in
[`JAVA_BRANCH_AUDIT.md`](JAVA_BRANCH_AUDIT.md) and
[`JAVA_CLEANUP_REPORT.md`](JAVA_CLEANUP_REPORT.md)._
