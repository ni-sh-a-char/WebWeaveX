/**
 * Converted from Python: core/integrations/augmentation_runtime.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { supportsCapability, supportsProviderCapability } from "./capabilityRegistry.js";

export function augmentMetadata(bundle: any, capability: any, provider_result: any = null, provider: any = null): any {
  var meta: any = py.pyDict(py.or2(py.get(bundle, "metadata", {}), () => ({})));
  var llm: any = py.pyDict(py.or2(py.get(meta, "llm", {}), () => ({})));
  var enabled: any = (py.truthy(provider) ? supportsProviderCapability(provider, capability) : supportsCapability(capability));
  if ((py.truthy(enabled) && py.truthy(provider_result))) {
    py.setItem(llm, capability, provider_result);
  }
  py.setItem(meta, "llm", llm);
  return {...(bundle), "metadata": meta};
}
export { supportsCapability, supportsProviderCapability };
