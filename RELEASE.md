# Release Process (JavaScript / npm)

## Preconditions

```bash
npm run lint
npm run typecheck
npm run test
npm run coverage
npm run validate:ecosystem
npm run validate:parity
npm run build
npm pack --dry-run
```

## Versioning

Semantic versioning per [CHANGELOG.md](CHANGELOG.md).

## Publish

Publishing is maintainer-driven after all gates pass. See `FINAL_TRUE_EQUALITY_CERTIFICATION.md` — certification is issued only when forensic gates pass.
