/**
 * Converted from Python: core/integrations/capability_registry.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let CAPABILITIES: any = new Set(["semantic_summarization", "semantic_embedding", "semantic_reasoning_augment"]);
export class CapabilityRegistry {
  static _providers = {};
  static _global = new Set();
  static register(provider_or_capability: any, capabilities: any = null): any {
    if ((capabilities !== null && capabilities !== undefined)) {
      py.setItem(CapabilityRegistry._providers, provider_or_capability, py.toSet(py.sorted(py.iter(capabilities).filter((c: any) => py.contains(CAPABILITIES, c)).map((c: any) => c))));
    } else if (py.contains(CAPABILITIES, provider_or_capability)) {
      py.setAdd(CapabilityRegistry._global, provider_or_capability);
    }
  }
  static supports(capability: any): any {
    return py.contains(CapabilityRegistry._global, capability);
  }
  static supports_provider(provider: any, capability: any): any {
    return py.contains(py.get(CapabilityRegistry._providers, provider, new Set()), capability);
  }
}
(CapabilityRegistry.prototype as Record<string, any>)["_providers"] = (CapabilityRegistry as Record<string, any>)["_providers"];
(CapabilityRegistry.prototype as Record<string, any>)["_global"] = (CapabilityRegistry as Record<string, any>)["_global"];
export let REGISTRY: any = new CapabilityRegistry();
export function supportsCapability(capability: any): any {
  return CapabilityRegistry.supports(capability);
}
export function supportsProviderCapability(provider: any, capability: any): any {
  return CapabilityRegistry.supports_provider(provider, capability);
}
