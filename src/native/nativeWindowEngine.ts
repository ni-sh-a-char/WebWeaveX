/**
 * Converted from Python: core/native/native_window_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractNativeWindows(snapshot: any = null): any {
  if ((snapshot !== null && snapshot !== undefined)) {
    return _normalizeWindows(snapshot);
  }
  try {
    return _enumeratePlatformWindows();
  } catch (_e: any) {
    return {"windows": [], "focused_window": "", "platform": py.sysShim.platform, "degraded": true, "bounded": true};
  }
}
export function _normalizeWindows(snapshot: any): any {
  var windows: any = py.slice([...py.iter(py.get(snapshot, "windows", []))], null, 5000);
  var focused: any = py.toStr(py.get(snapshot, "focused_window", ""));
  if ((!py.truthy(focused) && py.truthy(windows))) {
    var window: any;
    for (window of py.iter(windows)) {
      if (py.truthy(py.get(window, "focused"))) {
        focused = py.toStr(py.get(window, "title", py.get(window, "id", "")));
        break;
      }
    }
  }
  return {"windows": py.sorted(windows, {key: ((item: any) => [(-py.toInt(py.get(item, "z_order", 0))), py.toStr(py.get(item, "title", ""))]) as (item: any) => any}), "focused_window": focused, "platform": py.toStr(py.get(snapshot, "platform", py.sysShim.platform)), "bounded": true};
}
export function _enumeratePlatformWindows(): any {
  var platform: any = py.sysShim.platform;
  if (py.eq(platform, "win32")) {
    return _enumerateWindowsUia();
  }
  if (py.eq(platform, "darwin")) {
    return _enumerateWindowsAx();
  }
  return _enumerateWindowsAtspi();
}
export function _enumerateWindowsUia(): any {
  var comtypes: any = null;
  return _emptyWindows("win32", "uia_unavailable");
  return _emptyWindows("win32", "uia_requires_runtime_binding");
}
export function _enumerateWindowsAx(): any {
  return _emptyWindows("darwin", "ax_requires_runtime_binding");
}
export function _enumerateWindowsAtspi(): any {
  return _emptyWindows("linux", "atspi_requires_runtime_binding");
}
export function _emptyWindows(platform: any, reason: any): any {
  return {"windows": [], "focused_window": "", "platform": platform, "degraded": true, "reason": reason, "bounded": true};
}
