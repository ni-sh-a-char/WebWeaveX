/**
 * Converted from Python: core/security/pdf_bomb_guard.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function safePdfPages(pages: any, limit: any = 2000): any {
  return py.le(pages, limit);
}
