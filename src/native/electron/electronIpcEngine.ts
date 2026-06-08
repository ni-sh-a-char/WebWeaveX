/**
 * Converted from Python: core/native/electron/electron_ipc_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractElectronIpc(channels: any = null): any {
  var channel_list: any = py.sorted(py.or2(channels, () => ([{"channel": "ipc:renderer", "direction": "bidirectional"}, {"channel": "ipc:preload", "direction": "main_to_renderer"}])), {key: ((c: any) => py.toStr(py.get(c, "channel", ""))) as (item: any) => any});
  return {"channels": channel_list, "preload_metadata": py.sorted(py.iter(channel_list).filter((c: any) => py.contains(py.toStr(py.get(c, "channel", "")), "preload")).map((c: any) => c), {key: ((c: any) => py.toStr(py.get(c, "channel", ""))) as (item: any) => any}), "bounded": true};
}
