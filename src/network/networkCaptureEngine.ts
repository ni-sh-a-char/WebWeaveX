/**
 * Converted from Python: core/network/network_capture_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_REQUESTS: any = 5000;
export function attachNetworkCapture(page: any): any {
  var requests: any[] = [];
  function onRequest(req: any): any {
    if ((py.len(requests) >= MAX_REQUESTS)) {
      return;
    }
    py.listAppend(requests, {"url": py.slice(py.toStr(req.url), null, 5000), "method": py.toStr(req.method), "resource_type": py.toStr(req.resource_type)});
  }
  page.on("request", onRequest);
  return {"requests": requests, "bounded": true};
}
