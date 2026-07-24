# WebWeaveX — Frequently Asked Questions (FAQ)

### Q: What is WebWeaveX?
WebWeaveX is **universal runtime cognition infrastructure** for humans and AI agents. It models operational software systems as deterministic, graph-structured runtime objects.

### Q: How is WebWeaveX different from traditional web scrapers or browser drivers?
Browser drivers (Playwright, Selenium) execute low-level browser actions. WebWeaveX operates above browser drivers, normalizing raw DOM and network events into a stable, graph-based Intermediate Representation (IR) with state memory and replay proofs.

### Q: Does WebWeaveX bypass logins or CAPTCHAs?
**No.** WebWeaveX adheres to strict security bounds. It does **not** bypass authentication, crack passwords, or defeat CAPTCHAs. Session continuation is supported **strictly when user-authorized credentials or session cookies are provided by the operator**.

### Q: What is Kaalka v5?
Kaalka v5 is the cryptographic specification used by WebWeaveX to secure persisted session states and memory checkpoints. It uses AES-256-GCM authenticated cipher with PBKDF2-HMAC-SHA256 time-indexed key derivation.

### Q: Which SDK should I choose?
Choose the SDK that matches your target ecosystem:
- **Python:** Enterprise Python, AI notebooks, PyPI services.
- **JavaScript / TypeScript:** Node.js backend services, browser AI agents, npm.
- **Dart:** Flutter mobile apps, Dart microservices.
- **Java:** Spring Boot, enterprise JVM infrastructure.
- **Kotlin:** Native Android agents, Kotlin Multiplatform (KMP).

### Q: Is WebWeaveX free and open-source?
Yes, WebWeaveX is licensed under the permissive **Apache License 2.0**.
