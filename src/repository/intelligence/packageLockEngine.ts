/**
 * Converted from Python: core/repository/intelligence/package_lock_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function detectLocks(text: any): any {
  var src: any = String(py.or2(text, () => (""))).toLowerCase();
  var locks: any[] = [];
  var k: any;
  for (k of py.iter(["package-lock.json", "pnpm-lock.yaml", "yarn.lock", "poetry.lock", "cargo.lock", "pubspec.lock"])) {
    if (py.contains(src, k)) {
      py.listAppend(locks, k);
    }
  }
  return py.sorted(py.toSet(locks));
}
