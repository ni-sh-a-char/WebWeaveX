# JAVA_SESSION_6_ANALYSIS

**Phase 1 — canonical source identification for `build_interaction_graph`. Result: CLEAN
(0 forbidden). Cleared for implementation.**

Python canon `origin/python` @ `9625f4a` (2.1.0). Relative-import-aware transitive trace
([`tools/trace_imports_s5_relative.py`](../tools/trace_imports_s5_relative.py)).

API: `build_interaction_graph` → `core.interaction.interaction_graph_engine.build_interaction_graph(interactions)`.

---

## Transitive closure (5 modules / 326 lines / 0 forbidden)

| Module | Lines | Third-party imports | First-party imports | Classification | Dependency type |
| --- | ---: | --- | --- | --- | --- |
| `core/interaction/interaction_graph_engine.py` | 81 | `typing` | `core.crypto.kaalka_hash_engine` | **Pure deterministic** | none (the only NEW module) |
| `core/crypto/kaalka_hash_engine.py` | 14 | `typing` | `core.crypto.kaalka_runtime_engine` | **Pure deterministic** | already ported (Java `Kaalka`) |
| `core/crypto/kaalka_runtime_engine.py` | 92 | `base64`, `hashlib`, `typing` | `core.crypto.kaalka_v5_proc`, `core.determinism.normalization` | **Pure deterministic** (stdlib crypto) | already ported (Java `Kaalka`/`KaalkaV5Proc`) |
| `core/crypto/kaalka_v5_proc.py` | 40 | — | — | **Pure deterministic** | already ported (Java `KaalkaV5Proc`) |
| `core/determinism/normalization.py` | 99 | `json`, `re`, `unicodedata` | — | **Pure deterministic** (NFKC) | already ported (Java `Normalization`/`StableSerialize`) |

**Net new code to port:** exactly **one** module — `interaction_graph_engine.py` (81 lines).
The other four are the Session-1 determinism + crypto foundation, already byte-exact in Java.

## Forbidden-dependency checklist

| # | Forbidden class | Present? |
| --- | --- | :---: |
| 1 | BeautifulSoup | no |
| 2 | lxml | no |
| 3 | OCR | no |
| 4 | PDF binary | no |
| 5 | DOCX binary | no |
| 6 | Browser runtime | no |
| 7 | Network runtime | no |
| 8 | Platform | no |

Third-party imports across the whole closure: `typing`, `base64`, `hashlib`, `json`, `re`,
`unicodedata` — **all stdlib, all already reproduced byte-exact in the Java foundation.**
**No STOP condition. Cleared.**

## Behavioural summary (the function to port)

`build_interaction_graph(interactions: List[Dict]) -> Dict`:

1. Seed `nodes` with `{"id":"state_root","type":"state","name":"root"}`; `previous_id="state_root"`.
2. For each `interaction[:MAX_GRAPH_NODES=10000]` at `index`:
   - `node_id = str(interaction.get("id", f"interaction_{index}"))`
   - `action = str(interaction.get("action",""))`, `selector = str(interaction.get("selector",""))`
   - `node_type = "form" if action=="fill" else "page"`; then `"modal"` if `"modal" in
     selector.lower()`; then `"tab"` if `"tab" in selector.lower()` (independent checks — `tab`
     wins over `modal` when both present).
   - append node `{id, type, action, selector}`.
   - `relation = action or "transition"`; override: `click→"click"`, `fill|select→"submission"`,
     `wait→"navigation"`.
   - append edge `{from: previous_id, to: node_id, relation}`; `previous_id = node_id`.
3. Return `{"ir":"interaction_graph", "nodes": nodes[:10000], "edges": edges[:50000],
   "graph_hash": compute_kaalka_hash_payload({"nodes":…, "edges":…}), "bounded": True}`.

`compute_kaalka_hash_payload == compute_deterministic_hash == sha256(stable_serialize(value))`
(`core/crypto/kaalka_hash_engine.py:11`, `core/crypto/kaalka_runtime_engine.py:40-45`) — i.e.
**exactly** Java `Kaalka.computeKaalkaHash`. No new hashing primitive required.

**Sibling NOT ported** (per mission scope): `interaction_graph_to_runtime_ir` in the same
module is a separate function and out of scope.

## Parity-critical semantics (to reproduce byte-exact)

- `str(interaction.get(k, default))` — Python `str()` coercion (None→"None", int→decimal, ""
  stays ""); default applies only when the key is **absent**.
- `selector.lower()` — Python `str.lower()` (use `toLowerCase(Locale.ROOT)`).
- `action or "transition"` — empty string is falsy → `"transition"`.
- Two independent `node_type` overrides (modal then tab), not elif.
- `nodes[:10000]` slice is applied **after** appending the root + interactions (so 10000
  interactions yield 10001 nodes truncated to 10000), and the same sliced lists feed both the
  output and the `graph_hash`.
- `graph_hash` is over `{"nodes": sliced, "edges": sliced}` — `stable_serialize` sorts keys, so
  map insertion order is irrelevant; list element order and values must match exactly.
