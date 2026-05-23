# Dart Gap Audit (vs Python canonical)

**Reference:** `python` branch · **Audited:** `dart` @ `origin/dart`  
**Date:** 2026-05-23

---

## Summary

| Tier | Dart | Notes |
|------|:----:|-------|
| **Canonical crypto/graph parity** | ✅ | 11/11 vs `javascript_vectors.json` |
| **Canonical modules present** | ✅ | All `lib/src/*` packages exist |
| **Canonical replay** | ✅ | Matches JS spec checks |
| **NFKC normalization** | ⚠️ | Node.js subprocess when on PATH |
| **Browser depth** | ⚠️ | HTTP bounded; no Playwright in package |
| **Python production extensions** | ❌ | Not ported (expected) |
| **Validation tree** | ⚠️ | Parity only on remote; ecosystem validators in progress |
| **README depth** | ⚠️ | Shorter than Python |

---

## Capability matrix

| Capability | Python | Dart | Status |
|------------|--------|------|--------|
| Deterministic normalization | Full | Full (NFKC via Node) | ⚠️ |
| Kaalka v5 parity | Full | Full | ✅ |
| `buildRuntimeGraph` | Full | Full | ✅ |
| `validateReplayEquivalence` | Core+ | Full spec | ✅ |
| `buildRuntimeMemory` | Graph + extended | Graph fabric | ✅ contract |
| `queryRuntimeMemory` | Extended | Keyed query | ⚠️ |
| `reconstructRuntime` | Extended IR | Graph extraction | ✅ contract |
| `extractWeb` | Playwright | HTTP bounded | ⚠️ honest limit |
| Authenticated session | Full | Kaalka file | ✅ |
| `validation/parity/` | Full | Full | ✅ |
| `validation/replay/` | Partial | Local WIP | ⚠️ → ship |
| `validate_production.dart` | master script | Missing | ❌ → add |
| README equality | Full | Partial | ⚠️ → expand |
| pub publish dry-run | N/A | Clean with ignore rules | ⚠️ |

---

## Required actions (dart branch)

1. Ship `validation/replay/`, `validate_ecosystem.dart`, `validate_production.dart`
2. Add graph helpers: `validateRuntimeGraph`, `computeRuntimeFingerprint` aliases
3. Expand README to Python section parity
4. Document browser: HTTP-native; Playwright via host environment
5. Fix `lib/webweavex.dart` export duplication
6. Run `dart test` + parity + ecosystem gates

---

## Honest limits (do not fake)

- Dart browser extraction uses **HTTP** unless host integrates Playwright separately.
- NFKC requires **Node.js** on PATH for byte-identical unicode vectors (CRLF/volatile rules are pure Dart).
