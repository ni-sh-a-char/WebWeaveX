# Roadmap — JavaScript branch (`webweavex` npm)

## v2.0.x (current)

- [x] Native TypeScript runtime on `javascript` branch
- [x] `kaalka@5.0.0` registry integration + parity spec
- [x] npm publish-ready packaging (ESM/CJS, `sideEffects: false`)
- [ ] npm publish `webweavex@2.0.0` (when release approved)
- [ ] Python branch ciphertext alignment with [`CROSS_LANGUAGE_PARITY.md`](docs/architecture/CROSS_LANGUAGE_PARITY.md)

## v2.1

- Optional `playwright` peer dependency split
- Connector plugins (REST, streaming) as documented modules
- Coverage expansion for browser edge paths
- Cross-language CI matrix (JS vectors ↔ Python vectors)

## Future language branches

- **Rust** — performance-critical extraction workers
- **Go** — deployment-side runtime agents
- **Portal (`main`)** — language-neutral docs only (no mixed runtimes)

## Non-goals

- Auth bypass, CAPTCHA defeat, or credential cracking features
- Local forks of Kaalka published as npm packages from this repo
