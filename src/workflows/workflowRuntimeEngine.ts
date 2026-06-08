/**
 * Converted from Python: core/workflows/workflow_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildWorkflowRuntimeContext(url: any = "", runtime: any = "browser", sources: any = null): any {
  sources = py.or2(sources, () => ({}));
  return {"url": url, "primary_runtime": runtime, "sources": py.sorted(py.keys(sources)), "bounded": true};
}
