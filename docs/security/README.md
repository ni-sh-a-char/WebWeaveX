# Security

## Execution

- Production execution paths use an **allowlist sandbox** in `core/execution/`
- **No** `eval`, **no** `exec`, **no** `shell=True` in bounded runtime actions

## Persistence

- Runtime checkpoints use **Kaalka** wrappers only
- Do not add plaintext `json.dump` checkpoints for operational state

## URLs and fetch

- Legacy fetch paths enforce timeouts and bounded retries
- Prefer canonical pipeline ingress for new integrations

## Reporting vulnerabilities

See [SECURITY.md](../../SECURITY.md) at the repository root.
