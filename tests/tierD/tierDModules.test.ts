import { describe, expect, it } from "vitest";
import { detectContradictions } from "../../src/semantic/contradictionEngine.js";
import { runSemanticReasoning } from "../../src/semantic/semanticReasoningEngine.js";
import { runSemanticVm } from "../../src/vm/semanticVmEngine.js";
import { executeCognitionVm } from "../../src/vm/cognitionExecutionVm.js";
import { runWorldModelRuntime } from "../../src/worldModel/worldModelRuntime.js";
import { buildDistributedTopologyWorldState } from "../../src/worldModel/distributedTopologyWorldState.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";
import { registerParser, listParsers } from "../../src/parsers/parserRegistry.js";
import { recoverParserState } from "../../src/parsers/parserRecovery.js";
import { transitionRuntimeState } from "../../src/runtime/runtimeStateMachine.js";
import {
  reasonTopology,
  analyzeGraphContradictions,
  reconcileGraphs,
  compressGraph,
  exportGraph,
} from "../../src/graph/graphIntelligence.js";
import { federateSemanticMemory } from "../../src/distributed/distributedCognitionSync.js";
import { patchSemanticState } from "../../src/semantic/semanticPatch.js";
import { runOntologyRuntime } from "../../src/semantic/ontologyRuntime.js";

describe("Tier D convergence modules", () => {
  it("ontology and contradiction", () => {
    const onto = runOntologyRuntime([{ type: "User" }, { type: "Session" }]);
    expect(onto.classes).toContain("User");
    const contra = detectContradictions([
      "role is admin",
      "role is not admin",
    ]) as Record<string, unknown>;
    expect(Array.isArray(contra.contradiction_pairs)).toBe(true);
    expect((contra.lineage as Record<string, unknown>).stage).toBe("contradiction_evidence");
    expect(runSemanticReasoning([{ type: "A" }], []).bounded).toBe(true);
  });

  it("semantic VM fleet", () => {
    const vm = runSemanticVm([{ opcode: "LINK", operand: { from: "x", to: "y" } }]);
    expect(vm.bounded).toBe(true);
    expect(executeCognitionVm({}, [{ step: 1 }]).steps).toBe(1);
  });

  it("world model runtime", () => {
    const wm = runWorldModelRuntime({ entities: [{ id: 1 }] });
    expect(wm.bounded).toBe(true);
    const shards = [buildRuntimeGraph({ a: 1 }), buildRuntimeGraph({ b: 2 })];
    expect(buildDistributedTopologyWorldState(shards).shard_count).toBe(2);
  });

  it("graph intelligence helpers", () => {
    const g = buildRuntimeGraph({ a: 1 });
    expect(reasonTopology(g).bounded).toBe(true);
    expect(analyzeGraphContradictions(g).bounded).toBe(true);
    expect(reconcileGraphs([g, g]).nodes.length).toBeGreaterThan(0);
    expect(compressGraph(g)).toBeDefined();
    expect(exportGraph(g)).toBeTruthy();
    expect(federateSemanticMemory([{ shard: 1 }]).federated).toBe(true);
    expect(patchSemanticState({ a: 1 }, { b: 2 }).bounded).toBe(true);
    expect(runOntologyRuntime([]).entity_count).toBe(0);
  });

  it("parser registry and state machine", () => {
    registerParser("ts", { lang: "typescript" });
    expect(listParsers().length).toBeGreaterThan(0);
    expect(recoverParserState("ts", { offset: 0 }).recovered).toBe(true);
    expect(transitionRuntimeState("initialized", "running").valid).toBe(true);
  });
});
