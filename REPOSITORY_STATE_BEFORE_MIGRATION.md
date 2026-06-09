# REPOSITORY_STATE_BEFORE_MIGRATION.md

Captured before canonicalizing `C:\Projects\WebWeaveX` onto the `dart` branch (Phase 0). All values measured, not assumed.

## Repository

- Canonical path: `C:\Projects\WebWeaveX`
- Remote `origin`: `https://github.com/ni-sh-a-char/WebWeaveX.git` (fetch + push)

## Current checkout (main repo)

- Active branch: **`python`** @ `c8c415267c90e91842b98eca0fa721c83f8951ac`
- `python` vs `origin/python`: **0 ahead / 0 behind** (in sync)
- Working tree: clean except untracked `tools/` (contains `dart_parity_audit.py` + 2 vector-gen scratch scripts + pre-existing JS convergence infra `convergence/`, `omega_final/`, `py2ts/`, `runtime_vectors/`)

## Worktrees

| Path | Branch | HEAD |
|------|--------|------|
| `C:/Projects/WebWeaveX` | `python` | `c8c4152` |
| `C:/Projects/wwx-dart` (to be removed) | `dart` | `fdeb675` |

- `wwx-dart` working tree: **clean**, HEAD `fdeb675` == `origin/dart`, **0 unpushed commits**. All Dart work is safely on the remote.

## Branch heads

| Branch | Local HEAD | Remote |
|--------|-----------|--------|
| `dart` | `fdeb675c75301428165c32a2fe1c1d7b6c705368` | `origin/dart` == same |
| `python` | `c8c415267c90e91842b98eca0fa721c83f8951ac` | `origin/python` == same |
| `main` | `9968141da10e6035926b540c9ab5a893c57cff2c` | `origin/main` |
| `javascript` | `0baeeacd698e0e1ee7cf2d1682ed6911c43facac` | `origin/javascript` |

Remote-only branches: `origin/SDK`, `origin/release/v1.0-universal-interface-layer`.

## Stashes (pre-existing, not created by this work — left untouched)

- `stash@{0}: On dart: dart-tier-bc`
- `stash@{1}: On javascript: js-tier-c-final`

## Migration safety conclusion

Safe to proceed: every Dart commit is on `origin/dart` (`fdeb675`), the worktree is clean with nothing unpushed, and `python` is in sync with its remote. Removing the `wwx-dart` worktree and checking out `dart` in the main repo loses no work.
