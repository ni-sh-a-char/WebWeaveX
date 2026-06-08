/**
 * Converted from Python: core/distributed_memory/semantic_memory_fabric.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export class SemanticMemoryFabric {
  declare regions: any;
  constructor() {
    this.regions = {};
  }
  put(region: any, key: any, value: any): any {
    py.setdefault(this.regions, region, {});
    py.setItem(py.at(this.regions, region), key, value);
  }
  get(region: any, key: any): any {
    return py.get(py.get(this.regions, region, {}), key);
  }
}
