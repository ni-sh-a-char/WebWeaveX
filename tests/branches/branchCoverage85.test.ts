import { describe, expect, it } from "vitest";
import * as wwx from "../../src/index.js";
import { buildRuntimeGraph as _buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";
import { buildParserCognitionEvidence } from "../../src/parsers/parserOrchestration.js";
import { RuntimeStateMachine } from "../../src/runtime/runtimeStateMachine.js";
import { inferFromEvidence } from "../../src/evidence/semanticInferenceCalculus.js";
import { mergeSemanticStates } from "../../src/semantic/semanticMerge.js";
import { healSelector } from "../../src/adaptive/selectorHealing.js";
import { extractDatabaseRuntime } from "../../src/connectors/databaseConnector.js";
import { extractContainerRuntime } from "../../src/connectors/containerConnector.js";
import { validateReplayEquivalence } from "../../src/replay/replayEquivalence.js";
import { compileExecutionReality } from "../../src/execution/executionReality.js";

describe("branch coverage targets", () => {
  it("evidence and semantic branches", () => {
    expect(inferFromEvidence({}, [], 2).allowed).toBe(false);
    expect(inferFromEvidence({ x: 1 }, ["e"], 1).allowed).toBe(true);
    expect((mergeSemanticStates({ a: 1 }, { a: 2 }).state as Record<string, unknown>).a).toMatchObject({
      conflict: true,
    });
    expect(mergeSemanticStates({ a: 1 }, { b: 2 }).deterministic).toBe(true);
  });

  it("parser and recovery branches", () => {
    expect(buildParserCognitionEvidence(null as unknown as Record<string, unknown>).bounded).toBe(true);
    const sm = new RuntimeStateMachine();
    sm.transition("failed");
    expect(wwx.recoverRuntime("failed").recovered_state).toBe("failed");
    expect(wwx.recoverRuntime("failed").transitions).toBe(3);
  });

  it("connector degraded branches", () => {
    expect(extractDatabaseRuntime("unknown").degraded).toBe(true);
    expect(extractContainerRuntime("lxc").degraded).toBe(true);
  });

  it("adaptive healing branches", () => {
    expect(healSelector("#x", []).healed).toBe("#x");
    const healed = healSelector("#login", [
      { tag: "button", text: "login", attrs: { "data-testid": "login-btn" } },
    ]);
    expect((healed.strategies as unknown[]).length).toBeGreaterThan(0);
  });

  it("replay dom branches", () => {
    const g = _buildRuntimeGraph({ n: 1 });
    const env = { unified_runtime_graph: g, dom_html: "<div/>" };
    const env2 = { unified_runtime_graph: g, dom_html: "<div/>" };
    expect(validateReplayEquivalence(env, env2).equivalent).toBe(true);
  });

  it("execution reality branches", () => {
    expect(compileExecutionReality({ runtime: { available: false } }).available).toBe(false);
    expect(compileExecutionReality({ runtime: { available: true } }).causal_chain).toBeDefined();
  });

  it("workflow replay branch", () => {
    const wf = wwx.runAutonomousWorkflow("replay_session");
    expect((wf.plan as Record<string, unknown>).steps).toHaveLength(3);
    expect((wf.objective as Record<string, unknown>).objective).toBe("replay_session");
    expect(wf.bounded).toBe(true);
  });
});
