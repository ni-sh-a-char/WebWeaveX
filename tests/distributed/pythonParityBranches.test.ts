import { describe, expect, it } from "vitest";
import { synchronizeAdaptiveRuntime } from "../../src/distributed/distributedAdaptiveRuntimeEngine.js";
import { routeBrowserIdentity } from "../../src/distributed/distributedIdentityEngine.js";
import { monitorExtractionCluster } from "../../src/distributed/distributedMonitoringEngine.js";
import { federateStreamRuntimes } from "../../src/distributed/distributedStreamEngine.js";
import { federateExtractionRuntimes } from "../../src/distributed/runtimeFederationEngine.js";
import { buildRuntimeMemoryParity } from "../../validation/support/pythonParityMemory.js";
import { reconstructRuntimeParity } from "../../validation/support/pythonParityReconstruction.js";
import { buildSemanticOntology } from "../../src/semantic/ontologyRuntime.js";
import { executeWorkflowPlan } from "../../src/workflows/workflowOrchestrator.js";

describe("python parity branches", () => {
  it("distributed adaptive and monitoring", () => {
    const sync = synchronizeAdaptiveRuntime([
      {
        memory: {
          healed_selectors: { s: "ok" },
          pagination_patterns: ["p1"],
          modal_solutions: [{ id: "m" }],
        },
        schema: { fields: ["a", "b"] },
      },
    ]);
    expect(sync.healed_selectors).toBeDefined();
    expect((sync.pagination_patterns as string[]).length).toBe(1);
    expect((routeBrowserIdentity([{ worker_id: "w", identity: { profile_id: "p", fingerprint_hash: "fp" } }]).routes as unknown[]).length).toBe(1);
    expect(monitorExtractionCluster([{ status: "idle" }, { status: "running" }], [{}, {}]).queue_depth).toBe(2);
    expect(federateStreamRuntimes([{ worker_id: "w", events: [{ timestamp: 1, id: "e" }] }]).stream_count).toBe(1);
    expect(federateExtractionRuntimes([]).topology).toBeDefined();
  });

  it("memory reconstruction ontology workflow", () => {
    const mem = buildRuntimeMemoryParity({
      runtime_history: [{ step: "s", tick: 1, kind: "workflow" }],
      lineage: [{ id: "L1" }],
      semantic_relations: [{ from: "a", to: "b" }],
    });
    expect(mem.stable_hash).toBeTruthy();
    const rec = reconstructRuntimeParity({ runtime_graph: { nodes: [{ id: "n" }], edges: [] } });
    expect(rec.runtime_id).toBeTruthy();
    const ont = buildSemanticOntology([{ type: "X" }], "ops");
    expect(ont.primary_domain).toBe("ops");
    const wf = executeWorkflowPlan({ objective: "o", steps: [{ id: "1", action: "a" }] });
    expect(wf.completed_count).toBe(1);
  });
});
