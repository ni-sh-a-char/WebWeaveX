/**
 * Converted from Python: core/integrations/provider_router.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { supportsCapability, supportsProviderCapability } from "./capabilityRegistry.js";
import { ProviderRegistry } from "./providerRegistry.js";

export function routeAugmentation(capability: any, provider: any = null): any {
  if (py.truthy(provider)) {
    if (!py.truthy(supportsProviderCapability(provider, capability))) {
      return null;
    }
    return py.get(ProviderRegistry, provider);
  }
  if (py.truthy(supportsCapability(capability))) {
    var providers: any = ProviderRegistry.list_providers();
    return (py.truthy(providers) ? py.get(ProviderRegistry, py.at(providers, 0)) : null);
  }
  return null;
}
export { ProviderRegistry, supportsCapability, supportsProviderCapability };
