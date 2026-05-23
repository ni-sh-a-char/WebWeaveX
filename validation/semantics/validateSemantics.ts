import { SemanticMemory, buildSemanticMemory } from "../../src/semantic/semanticMemory.js";
import { runSemanticRuntime } from "../../src/semantic/semanticRuntime.js";

const mem = new SemanticMemory();
mem.put("agent", { ok: true });
const built = buildSemanticMemory({ entities: { entities: [{ label: "login" }] } });
const runtime = runSemanticRuntime({}, { kind: "tick" });

const results = {
  memory_put: mem.get("agent") != null,
  build: built.bounded === true,
  runtime: runtime.bounded === true,
};

console.log("PASS", results);
if (!Object.values(results).every(Boolean)) process.exit(1);
