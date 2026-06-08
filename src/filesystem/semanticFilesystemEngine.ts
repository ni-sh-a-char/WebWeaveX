/**
 * Converted from Python: core/filesystem/semantic_filesystem_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export class SemanticFilesystem {
  declare files: any;
  constructor() {
    this.files = {};
  }
  write(path: any, content: any): any {
    py.setItem(this.files, path, content);
  }
  read(path: any): any {
    return py.get(this.files, path, "");
  }
  list_paths(): any {
    return py.sorted(py.keys(this.files));
  }
}
