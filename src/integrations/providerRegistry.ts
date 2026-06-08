/**
 * Converted from Python: core/integrations/provider_registry.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export class ProviderRegistry {
  static _providers = {};
  static register(name: any, adapter: any): any {
    py.setItem(ProviderRegistry._providers, name, adapter);
  }
  static get(name: any): any {
    return py.get(ProviderRegistry._providers, name);
  }
  static list_providers(): any {
    return py.sorted(py.keys(ProviderRegistry._providers));
  }
}
(ProviderRegistry.prototype as Record<string, any>)["_providers"] = (ProviderRegistry as Record<string, any>)["_providers"];
