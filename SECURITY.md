# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability within WebWeaveX Kotlin SDK, please send an email to the maintainer. All security vulnerabilities will be promptly addressed.

## Security Model

| Control | Implementation |
|---------|----------------|
| No arbitrary eval | Deterministic execution paths only |
| Bounded extraction | Configurable limits on all extraction |
| Deterministic persistence | Kaalka-compatible checkpoints |
| Deterministic clock | No wall-clock-dependent behavior |

## Supported Versions

| Version | Supported |
|---------|-----------|
| 3.0.0 | Yes |

## Scope

This security policy applies to the Kotlin SDK (`io.webweavex:webweavex-kotlin:3.0.0`).

## Out of Scope

- Third-party dependencies (report upstream)
- Infrastructure deployment security
- Authentication bypass (WebWeaveX does not bypass authentication)
