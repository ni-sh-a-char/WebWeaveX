/**
 * Converted from Python: core/connectors/filesystem_connector_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractFilesystemRuntime(root: any = ".", snapshot: any = null): any {
  if ((snapshot !== null && snapshot !== undefined)) {
    return {"root": py.toStr(py.get(snapshot, "root", root)), "topology": py.sorted(py.get(snapshot, "files", []), {key: (py.toStr) as (item: any) => any}), "mutation_streams": [...py.iter(py.get(snapshot, "mutations", []))], "synchronization_state": py.pyDict(py.get(snapshot, "sync", {})), "permissions": py.pyDict(py.get(snapshot, "permissions", {})), "inode_relationships": [...py.iter(py.get(snapshot, "inodes", []))], "bounded": true};
  }
  var topology: any[] = [];
  try {
    var base: any = py.path(root);
    if (py.truthy(base.exists())) {
      var path: any;
      for (path of py.iter(py.slice(py.sorted(base.rglob("*")), null, 5000))) {
        if (py.truthy(path.is_file())) {
          py.listAppend(topology, py.toStr(path.relative_to(base)));
        }
      }
    }
  } catch (_e: any) {
    return {"root": root, "topology": [], "degraded": true, "bounded": true};
  }
  return {"root": root, "topology": topology, "mutation_streams": [], "synchronization_state": {}, "permissions": {}, "inode_relationships": [], "bounded": true};
}
