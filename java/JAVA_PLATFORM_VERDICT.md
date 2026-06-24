# JAVA_PLATFORM_VERDICT

**Phase-5 audit (Session 28). Verdict: OS-runtime dependent — blocked.** Python canon `9625f4a`.
APIs: `extract_native`, `run_native_cognition` (native/desktop runtime); plus `extract_repository`
(filesystem, documented here as the adjacent OS-coupled case).

## A. Concrete runtime — `sys.platform` reaches observable output
`extract_native`/`run_native_cognition → extract_native_windows(snapshot)`:
```python
# core/native/native_window_engine.py
if snapshot is not None: return _normalize_windows(snapshot)   # else live OS enumeration
def _normalize_windows(snapshot):
    return {"windows": sorted(...), "focused_window": focused,
            "platform": str(snapshot.get("platform", sys.platform)),   # <-- sys.platform leaks
            "bounded": True}
def _enumerate_platform_windows():
    platform = sys.platform
    if platform == "win32":  return _enumerate_windows_uia()      # live UIAutomation
    if platform == "darwin": ...                                   # live Quartz
    if platform == "linux":  ...                                   # live X11
```
`run_native_cognition` likewise branches on `sys.platform` (win32/darwin/linux) for its runtime fixture.

## B. Observable output dependency
Even on the deterministic *snapshot* path, the result's `platform` field falls back to `sys.platform`
when the snapshot omits `"platform"` — so the observable output embeds the host OS string
(`"win32"`/`"darwin"`/`"linux"`). On the no-snapshot path the entire window set comes from live OS
enumeration (UIAutomation/Quartz/X11), which is non-deterministic and OS-specific.

## C. Why Java cannot reproduce it (cross-platform byte-exact)
`sys.platform` is the running interpreter's OS identifier. A Java port on Windows would have to emit
`"win32"` while the same code on macOS emits `"darwin"` — the *same input* produces *different output*
per OS, so no single deterministic function exists across the supported matrix. Reproducing the live
enumeration paths additionally requires per-OS native accessibility APIs (UIAutomation/Quartz/X11),
which are platform binaries, not portable Java. Byte-exact cross-platform parity cannot be guaranteed.

## D. Why frontier reduction fails
The `sys.platform` value is not discarded — it is a top-level field (`platform`) and feeds the
fingerprint. The only way to remove it is for canon to require an explicit `platform` in every
snapshot (a canon change). No observable surface excludes it today.

## Adjacent case — `extract_repository` (filesystem)
`extract_repository(path) → ingest_repository(path)` reads an actual on-disk repository (file contents
+ directory walk). Output depends on real filesystem state, and `os.walk` ordering is OS/filesystem
dependent, so byte-exact cross-environment parity is not guaranteed. Blocked (filesystem-runtime
required) — distinct substrate from native/platform but same "real OS resource" class.

## Verdict
`extract_native`, `run_native_cognition` = **OS-runtime dependent (blocked)** via `sys.platform` +
live accessibility enumeration. `extract_repository` = **filesystem-runtime required (blocked)**.
Unblock lever: canon change requiring an explicit `platform` in snapshots and a filesystem-fixture
contract with deterministic ordering.
