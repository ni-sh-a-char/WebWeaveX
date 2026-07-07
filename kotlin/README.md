# WebWeaveX — Kotlin

First-class Kotlin/JVM implementation of WebWeaveX, byte-identical to the Python
reference (and to the JavaScript, Java, and Dart branches).

Public behavior is verified by the same cross-language harness used for the other
languages: Python generates golden vectors, each language canonical-serializes its
output (NFC + float normalization + sorted keys) and SHA-256-compares. Target: 5-way
MATCH (Python == JavaScript == Java == Dart == Kotlin).

Status: **K0 scaffold** — build module + determinism core + verification harness.
Full public-API + enrichment-stage port proceeds per `KotlinRoadmap.json`.

Kotlin/JVM interoperates with the verified Java branch: where byte-parity risk is
highest, Kotlin delegates directly to the certified `io.webweavex.*` Java classes,
then idiomatizes. This guarantees parity with near-zero reimplementation drift.
