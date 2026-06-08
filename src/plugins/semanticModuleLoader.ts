/**
 * Converted from Python: core/plugins/semantic_module_loader.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function loadSemanticModule(manifest: any): any {
  return {"module": py.get(manifest, "name"), "loaded": true};
}
