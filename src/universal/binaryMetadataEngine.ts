/**
 * Converted from Python: core/universal/binary_metadata_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractBinaryMetadata(payload: any): any {
  var data: any = ((typeof payload === "string") ? py.encode(payload, "utf-8") : py.or2(payload, () => (new py.PyBytes(""))));
  return {"size": py.len(data), "sha256": py.hashNew("sha256", data).hexdigest(), "magic_hex": py.slice(data, null, 8).hex(), "is_binary": py.any(py.iter(py.slice(data, null, 1024)).map((b: any) => py.eq(b, 0)))};
}
