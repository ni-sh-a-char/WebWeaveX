# Final Determinism Report (Dart)

- NFKC via Node.js (`String.normalize('NFKC')`) when Node is on PATH
- CRLF → LF, volatile key stripping, stable JSON key ordering
- SHA-256 over `stableSerialize` payload
- Kaalka v5 byte `_proc` + base64 ciphertext
