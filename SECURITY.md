# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 3.0.0   | Yes       |

## Reporting

Report vulnerabilities via GitHub Issues (private disclosure preferred for sensitive reports).

## Guarantees

- Production execution forbids `eval`, `exec`, and arbitrary subprocess invocation
- Persisted runtime state uses Kaalka encryption (`core.crypto.kaalka_runtime_engine`)
- Execution sandbox enforces allowlisted actions and policy bounds

## Known limitations

- In-memory cache (`core/cache_engine.py`) uses integrity hashing only — not for secrets
- Some database segment stores write plaintext JSON — migrate to Kaalka before storing sensitive data
