/**
 * Converted from Python: core/plugins/semantic_plugin_runtime.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export class SemanticPluginRuntime {
  declare _plugins: any;
  constructor() {
    this._plugins = {};
  }
  register(name: any, metadata: any): any {
    py.setItem(this._plugins, name, metadata);
  }
  list_plugins(): any {
    return {"plugins": py.sorted(py.keys(this._plugins))};
  }
}
