import { describe, expect, it } from "vitest";
import { runRuntimeCognitionTick } from "../../src/cognition/runtimeCognitionEngine.js";
import { buildParserCognitionEvidence } from "../../src/parsers/parserOrchestration.js";
import { runSemanticOrchestration } from "../../src/semantic/semanticOrchestration.js";
import { diffRuntimeGraphs, buildGraphCognitionIndex } from "../../src/graph/graphIntelligence.js";
import { synchronizeDistributedCognition } from "../../src/distributed/distributedCognitionSync.js";
import { compileExecutionReality } from "../../src/execution/executionReality.js";
import { buildSemanticLineage } from "../../src/semantic/semanticLineage.js";
import { recoverRuntime } from "../../src/runtime/runtimeRecoveryEngine.js";
import { replaySemanticEvents } from "../../src/runtime/semanticReplayVm.js";
import { buildSemanticGraphLineage } from "../../src/semantic/semanticGraphCognition.js";
import type { RuntimeGraph } from "../../src/contracts/graphContracts.js";

describe("Tier C/D convergence", () => {
  it("runtime cognition tick", () => {
    const out = runRuntimeCognitionTick({ u: 1 }, [{ s: 1 }], [{ id: "1", type: "t" }]);
    expect(out.bounded).toBe(true);
    expect(out.recovery).toBeDefined();
  });

  it("parser cognition", () => {
    const empty = buildParserCognitionEvidence();
    expect((empty.parser_evidence as string[]).length).toBe(0);
    const full = buildParserCognitionEvidence({ parser_evidence: { x: true }, symbols: {} });
    expect((full.parser_evidence as string[]).length).toBeGreaterThan(0);
  });

  it("semantic orchestration and lineage", () => {
    expect(runSemanticOrchestration([{ a: 1 }, { b: 2 }]).bounded).toBe(true);
    expect(buildSemanticLineage([{ kind: "a", tick: 0 }]).lineage).toHaveLength(1);
  });

  it("graph intelligence", () => {
    const g1 = runRuntimeCognitionTick({ a: 1 }).graph as RuntimeGraph;
    const g2 = runRuntimeCognitionTick({ b: 2 }).graph as RuntimeGraph;
    expect(diffRuntimeGraphs(g1, g2).bounded).toBe(true);
    expect(buildGraphCognitionIndex(g1).index_id).toBeTruthy();
    expect(buildSemanticGraphLineage([g1, g2]).graph_count).toBe(2);
  });

  it("distributed cognition and execution reality", () => {
    expect(synchronizeDistributedCognition([], []).synchronized).toBe(true);
    expect(
      compileExecutionReality({
        runtime: { available: true, dom_stabilization: { stabilized_hash: "h" } },
        unified_runtime_graph: { nodes: [{}], edges: [] },
      }).available,
    ).toBe(true);
  });

  it("recovery and semantic replay vm", () => {
    expect(recoverRuntime("initialized", []).recovered_state).toBe("initialized");
    expect(replaySemanticEvents([]).event_count).toBe(0);
  });
});
