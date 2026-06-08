/**
 * Converted from Python: core/plugins/semantic_package_manager.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export class SemanticPackageManager {
  declare _packages: any;
  constructor() {
    this._packages = [];
  }
  install(package_: any): any {
    if (!py.contains(this._packages, package_)) {
      py.listAppend(this._packages, package_);
    }
  }
  list_packages(): any {
    return py.sorted(this._packages);
  }
}
