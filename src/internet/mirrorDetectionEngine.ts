/**
 * Converted from Python: core/internet/mirror_detection_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectMirrors(urls: any): any {
  var paths: Record<string, any> = {};
  var url: any;
  for (url of py.iter(py.or2(urls, () => ([])))) {
    var parsed: any = py.urlparse(url);
    var key: any = py.or2(parsed.path, () => ("/"));
    py.listAppend(py.setdefault(paths, key, []), url);
  }
  var mirrors: any = py.items(paths).filter(([p, u]: any) => (py.len(u) > 1)).map(([p, u]: any) => ({"path": p, "urls": py.sorted(u)}));
  return {"mirrors": mirrors, "mirror_count": py.len(mirrors)};
}
