# WebWeaveX Language Implementations

WebWeaveX is a **multi-language deterministic runtime extraction ecosystem**. Each language has its own branch and package—no mixed implementations on a single branch.

| Language | Branch | Package | Status |
|----------|--------|---------|--------|
| Python | [`python`](https://github.com/ni-sh-a-char/WebWeaveX/tree/python) | [`webweavex` on PyPI](https://pypi.org/project/webweavex/) | **Stable** (v2.0.0) |
| JavaScript / TypeScript | [`javascript`](https://github.com/ni-sh-a-char/WebWeaveX/tree/javascript) | [`webweavex` on npm](https://www.npmjs.com/package/webweavex) | **In development** |
| Rust | `rust` | planned | Planned |
| Go | `go` | planned | Planned |
| Java | `java` | planned | Planned |

## Choosing an implementation

| Use case | Branch |
|----------|--------|
| Production Python services, PyPI install | `python` |
| Node.js, browser automation, npm / ESM / CJS | `javascript` |
| Architecture, security policy, roadmap | `main` (this portal) |

## Cross-language guarantees

All implementations share:

- **Kaalka** deterministic encryption and hashing (parity-validated vectors)
- **Canonical pipeline** single execution path
- **Replay-safe** runtime graphs and fingerprints
- **Authorized-only** authenticated runtime continuation (no auth bypass)

See `docs/` on each branch for language-specific guides.
