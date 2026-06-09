# WebWeaveX Governance

WebWeaveX is **deterministic runtime cognition infrastructure** for humans and AI agents,
implemented across three language branches that share one canonical contract.

## Canonical branch

- **Python** (`origin/python`) is the canonical runtime and specification source of truth.
- **JavaScript** (`origin/javascript`) and **Dart** (`origin/dart`) converge to Python via
  forensic audits and differential (hash-parity) validation.

## Decision process

1. Changes that affect cross-language contracts require **parity vector updates** in every
   affected branch and a passing `validate_parity` run.
2. Releases require passing the full gate sequence on the target branch
   (format, analyze, test, coverage ≥ 90%, parity, publish dry-run).
3. Security issues follow [SECURITY.md](SECURITY.md) and take precedence over feature work.
4. Platform-deferred APIs (capabilities not available in-process for a given runtime) must be
   documented as **Deferred** with an explicit reason — never silently dropped or faked.

## Classification honesty

Every public API is classified Complete / Partial / Deferred / Missing against the Python
contract. "Complete" requires a proven hash-parity vector or save/load roundtrip. Optimistic or
unverified classifications are not permitted (see [`API_PARITY_VALIDATION_REPORT.md`](API_PARITY_VALIDATION_REPORT.md)).

## Roles

See [MAINTAINERS.md](MAINTAINERS.md). Review ownership is defined in [CODEOWNERS](CODEOWNERS).
