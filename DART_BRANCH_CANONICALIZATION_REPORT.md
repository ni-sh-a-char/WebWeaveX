# DART_BRANCH_CANONICALIZATION_REPORT.md

Phase 1 result: `C:\Projects\WebWeaveX` is now the single canonical repository, checked out on the `dart` branch. The `wwx-dart` worktree has been removed. All evidence below is measured.

## Actions performed

1. Verified the `wwx-dart` worktree was clean and fully pushed: HEAD `fdeb675` == `origin/dart`, **0 unpushed commits** (see `REPOSITORY_STATE_BEFORE_MIGRATION.md`).
2. `git worktree remove C:/Projects/wwx-dart` — removed; `git worktree list` now shows only `C:/Projects/WebWeaveX`.
3. `git checkout dart` in the main repo — switched cleanly from `python`.
4. `git pull origin dart` — already up to date at `fdeb675`.
5. Cleaned stale untracked contamination from the working tree (a prior ~1,500-file alternate Dart transpilation overlay, a stray `_pycov/` Python venv, `.coverage`, `docs/specs/`, and JS-branch `tools/` infra) via `git clean -fd -e .claude`, after staging the two artifacts to keep. **No tracked file was touched** (git clean only removes untracked files).

## Proof of canonical state

| Check | Result |
|-------|--------|
| Active branch | `dart` |
| HEAD | `fdeb675c75301428165c32a2fe1c1d7b6c705368` (== `origin/dart`) |
| Worktrees | only `C:/Projects/WebWeaveX` (forbidden `wwx-dart` removed) |
| Tracked Dart lib files | **146** (`git ls-files lib | grep .dart`) — matches branch, contamination gone |
| `find lib -name '*.dart'` on disk | **146** (no untracked overlay remaining) |
| `dart pub get` | OK |
| `dart analyze` | **No issues found!** |
| `dart test` | **779 passing** |
| Parity vectors present | `validation/parity/*_api_vectors.json` (12 family files) |

## Forbidden paths — none in use

`C:\Projects\wwx-dart` removed; no detached worktrees, shadow repos, or external dev folders remain. All further development happens directly in `C:\Projects\WebWeaveX` on `dart`.

## Other branches (untouched)

`python` `c8c4152`, `javascript` `0baeeac`, `main` `9968141` — none modified by this migration.
