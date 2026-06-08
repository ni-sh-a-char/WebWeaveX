/**
 * Converted from Python: core/native/electron/electron_hash_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { computeKaalkaHash } from "../../crypto/kaalkaHashEngine.js";

export function stableElectronRuntimeHash(payload: any): any {
  var canonical: any = {"cdp": py.sorted(py.get(py.or2(py.get(payload, "cdp"), () => ({})), "endpoints", []), {key: ((e: any) => py.toStr(py.get(e, "method", ""))) as (item: any) => any}), "routes": py.sorted(py.get(py.or2(py.get(payload, "routes"), () => ({})), "routes", []), {key: ((r: any) => py.toStr(py.get(r, "path", ""))) as (item: any) => any}), "ipc": py.sorted(py.get(py.or2(py.get(payload, "ipc"), () => ({})), "channels", []), {key: ((c: any) => py.toStr(py.get(c, "channel", ""))) as (item: any) => any}), "storage": {"indexed_db": py.sorted(py.get(py.or2(py.get(payload, "storage"), () => ({})), "indexed_db", []), {key: ((x: any) => py.toStr(x)) as (item: any) => any}), "local_storage": py.sorted(py.items(py.or2(py.get(py.or2(py.get(payload, "storage"), () => ({})), "local_storage"), () => ({}))))}};
  return computeKaalkaHash(py.jsonDumps(canonical, {sortKeys: true, separators: [",", ":"] as [string, string]}));
}
export { computeKaalkaHash };
