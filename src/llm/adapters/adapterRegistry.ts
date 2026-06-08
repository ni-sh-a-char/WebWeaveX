/**
 * Converted from Python: core/llm/adapters/adapter_registry.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function listAdapters(): any {
  return py.sorted(["groq", "ollama", "openai", "anthropic", "gemini", "mistral"]);
}
