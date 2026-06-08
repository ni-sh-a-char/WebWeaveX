/**
 * Converted from Python: core/security/html_sanitizer.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function sanitizeHtml(text: any): any {
  return py.reSub("<script.*?>.*?</script>", "", py.or2(text, () => ("")), 0, "is");
}
