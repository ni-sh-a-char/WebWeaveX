/**
 * Converted from Python: core/performance/budget_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function enforceBudgets(pages: any, bytes_used: any, max_pages: any = 100, max_bytes: any = 50000000): any {
  return {"pages_ok": py.le(pages, max_pages), "bytes_ok": py.le(bytes_used, max_bytes)};
}
