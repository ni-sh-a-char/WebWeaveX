# Security Policy & Kaalka v5 Security Contract

## Supported Versions

| Version | Supported | Security Maintenance |
|:---|:---|:---|
| **v3.0.0** | ✅ Yes | Full Security Maintenance & Patching |
| < 3.0.0 | ❌ No | Deprecated |

---

## Security Guarantees & Invariants

1. **Zero Auth Bypass:** WebWeaveX does not attempt to bypass login screens, crack authentication passwords, or defeat CAPTCHAs. Session continuation is supported **strictly when user-authorized credentials or session cookies are provided by the system operator**.
2. **Kaalka v5 Encrypted State:** All operational checkpoints, session tokens, and memory fabric data stored at rest are encrypted using `Kaalka v5` (AES-256-GCM authenticated cipher with PBKDF2-HMAC-SHA256 time-indexed key derivation).
3. **Allowlisted Execution Sandbox:** Production execution paths enforce strict policy bounds. Functions like `eval()`, `exec()`, or arbitrary shell execution are strictly forbidden in production code.

---

## Reporting Vulnerabilities

If you discover a potential security vulnerability within WebWeaveX, please report it privately:

1. Email responsible disclosure reports to: `piyushmishra.dev@gmail.com` or submit a private security advisory on GitHub.
2. Include steps to reproduce, affected version(s), and system details.
3. We will acknowledge receipt within 24 hours and provide a patch timeframe within 72 hours.
