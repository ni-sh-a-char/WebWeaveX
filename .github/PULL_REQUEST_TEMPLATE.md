## Summary

<!-- What does this PR change and why? -->

## Type

- [ ] Bug fix
- [ ] Documentation
- [ ] Test coverage
- [ ] Performance
- [ ] Feature (pipeline-aligned)

## Checklist

- [ ] Tests added or updated (`pytest -q` passes locally)
- [ ] Scoped production coverage remains **≥ 90%** (`python -m pytest`)
- [ ] Determinism preserved (no `random` / `uuid4` in runtime paths)
- [ ] Replay-safe (no breaking changes to graph normalization or fingerprints)
- [ ] Kaalka-compatible persistence (no plaintext/pickle checkpoints)
- [ ] No new shadow orchestrators — changes go through `run_canonical_pipeline()` or documented specialized engines
- [ ] `import webweavex` works; `webweavex.__version__ == "3.0.0"`
- [ ] `python -m build` succeeds

## Notes for reviewers

<!-- Optional: migration, limitations, benchmark numbers -->

