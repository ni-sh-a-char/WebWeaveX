# FINAL DETERMINISM REPORT

## Formula

```text
normalizeRuntimeValue → stableSerialize → UTF-8 → deriveKaalkaTimeKey → kaalka@5._proc → base64
```

## Guarantees

- Replay-safe serialization (volatile keys stripped)
- DOM stabilization fingerprints (not raw HTML equality)
- `validateReplayEquivalence` graph + fingerprint + DOM hash

See [docs/architecture/CROSS_LANGUAGE_PARITY.md](docs/architecture/CROSS_LANGUAGE_PARITY.md).