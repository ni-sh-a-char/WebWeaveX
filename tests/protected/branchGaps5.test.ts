import { describe, expect, it } from "vitest";
import { inferFromEvidence } from "../../src/evidence/semanticInferenceCalculus.js";
import { runOntologyRuntime } from "../../src/semantic/ontologyRuntime.js";
import { buildSemanticLineage } from "../../src/semantic/semanticLineage.js";
import { reconcileSemanticStates } from "../../src/semantic/semanticReconciliation.js";
import { buildSemanticMemory, SemanticMemory } from "../../src/semantic/semanticMemory.js";
import { RuntimeStateMachine, transitionRuntimeState } from "../../src/runtime/runtimeStateMachine.js";
import { balanceExtractionWorkloads } from "../../src/distributed/distributedLoadBalancer.js";
import { routeAuthenticatedSessions } from "../../src/distributed/distributedSessionEngine.js";
import { buildParserCognitionEvidence, orchestrateParserFleet } from "../../src/parsers/parserOrchestration.js";
import { buildUnifiedRuntimeIR, compileRuntimeIR } from "../../src/ir/unifiedIr.js";

describe("nullable-argument arms across small modules", () => {
  it("inference calculus accepts null observed", () => {
    const out = inferFromEvidence(null as never, ["e1"], 1);
    expect(out.allowed).toBe(true);
    expect(out.inferred).toEqual({});
    const denied = inferFromEvidence({ k: 1 }, [null, "", "e1", "e1"], 2);
    expect(denied.allowed).toBe(false);
  });

  it("ontology, lineage, reconciliation and memory tolerate empty shapes", () => {
    expect(runOntologyRuntime([])).toBeDefined();
    expect(runOntologyRuntime([{ type: "T" }, {}])).toBeDefined();
    expect(buildSemanticLineage([])).toBeDefined();
    expect(buildSemanticLineage([{ id: "a" }, { from: "a", to: "b" }])).toBeDefined();
    expect(reconcileSemanticStates([])).toBeDefined();
    expect(buildSemanticMemory({})).toBeDefined();
    expect(buildSemanticMemory({ entities: {} })).toBeDefined();
    const mem = new SemanticMemory();
    expect(mem.get("missing")).toBeUndefined();
    mem.put("k", 1);
    expect(mem.get("k")).toBe(1);
  });

  it("state machine custom construction and transitions", () => {
    const sm = new RuntimeStateMachine();
    expect(sm.transition("running")).toBeDefined();
    expect(transitionRuntimeState("nonsense-state", "running")).toBeDefined();
    expect(transitionRuntimeState("running", "running")).toBeDefined();
  });

  it("distributed balancing and session routing edge shapes", () => {
    expect(balanceExtractionWorkloads([{ worker_id: "w" }], [])).toBeDefined();
    expect(balanceExtractionWorkloads([], [])).toBeDefined();
    expect(routeAuthenticatedSessions([])).toBeDefined();
    expect(routeAuthenticatedSessions([{ worker_id: "w", session: { cookies: [] } }, {}])).toBeDefined();
  });

  it("parser orchestration and unified ir variants", () => {
    expect(buildParserCognitionEvidence({} as never)).toBeDefined();
    expect(buildParserCognitionEvidence({ ast: { nodes: [1] }, symbols: { symbols: [1] } } as never)).toBeDefined();
    expect(orchestrateParserFleet([] as never)).toBeDefined();
    expect(orchestrateParserFleet(["def x():\n    pass"] as never)).toBeDefined();
    expect(buildUnifiedRuntimeIR({} as never)).toBeDefined();
    expect(compileRuntimeIR({})).toBeDefined();
    expect(compileRuntimeIR({ runtime: { nodes: [] } })).toBeDefined();
  });
});
