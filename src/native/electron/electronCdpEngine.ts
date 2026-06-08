/**
 * Converted from Python: core/native/electron/electron_cdp_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractElectronCdp(target_url: any = "", devtools_port: any = 9222): any {
  var endpoints: any = py.sorted([{"method": "Runtime.evaluate", "domain": "Runtime"}, {"method": "DOM.getDocument", "domain": "DOM"}, {"method": "Network.enable", "domain": "Network"}, {"method": "Page.navigate", "domain": "Page"}], {key: ((e: any) => py.at(e, "method")) as (item: any) => any});
  return {"available": py.truthy(py.or2(target_url, () => (devtools_port))), "devtools_port": devtools_port, "target_url": target_url, "protocol": "cdp", "endpoints": endpoints, "preload_scripts": [], "bounded": true};
}
