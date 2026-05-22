---
name: Feature request
about: Propose a capability that fits the canonical extraction pipeline
title: "[feature] "
labels: enhancement
assignees: ""
---

## Problem

What extraction or runtime gap are you solving?

## Proposed solution

How should it integrate with `run_canonical_pipeline()` or an existing phase package?

## Alternatives considered

## Determinism / replay impact

- [ ] Must remain replay-safe
- [ ] Must use Kaalka for any new persistence
- [ ] Must not introduce `random`, `uuid4`, or plaintext checkpoints
