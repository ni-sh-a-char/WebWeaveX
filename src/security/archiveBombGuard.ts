/**
 * Converted from Python: core/security/archive_bomb_guard.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function safeArchiveSize(size: any, limit: any = 50000000): any {
  return py.le(size, limit);
}
