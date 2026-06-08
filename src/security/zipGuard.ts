/**
 * Converted from Python: core/security/zip_guard.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function safeZipRatio(uncompressed: any, compressed: any, max_ratio: any = py.F(100.0)): any {
  return py.and2((compressed > 0), () => (py.le(py.div(uncompressed, compressed), max_ratio)));
}
