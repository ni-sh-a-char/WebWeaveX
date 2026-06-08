import { describe, expect, it } from "vitest";
import { extractRepository } from "../../src/repository/extractRepository.js";
import { validateInference } from "../../src/evidence/inferenceValidation.js";
import { makeStreamEvent, normalizeStreamEvents } from "../../src/streaming/streamCapture.js";
import { runAdaptiveExtraction } from "../../src/adaptive/adaptiveOrchestrator.js";
import { runAutonomousWorkflow } from "../../src/workflows/workflowOrchestrator.js";
import { mergeSemanticStates } from "../../src/semantic/semanticMerge.js";
import { createSemanticSnapshot } from "../../src/semantic/semanticSnapshot.js";
import { extractDocumentStructure } from "../../src/documents/documentExtraction.js";
import { compileWorldModel } from "../../src/worldModel/worldModelCompile.js";

describe("Tier B convergence modules", () => {
  it("repository extraction", () => {
    const out = extractRepository(".");
    expect((out.repository_ir as Record<string, unknown>).available).toBe(true);
  });

  it("evidence inference", () => {
    expect(validateInference({ a: 1 }, ["e"]).valid).toBe(true);
  });

  it("streaming events", () => {
    const ev = makeStreamEvent(0, "s", "in", "{}", "c");
    expect(normalizeStreamEvents([ev]).length).toBe(1);
  });

  it("adaptive healing", () => {
    expect(runAdaptiveExtraction("btn", "<button>btn</button>").bounded).toBe(true);
  });

  it("workflow orchestration", () => {
    expect((runAutonomousWorkflow("replay_session").plan as Record<string, unknown>).steps).toBeDefined();
  });

  it("semantic merge and snapshot", () => {
    const merged = mergeSemanticStates({ a: 1 }, { b: 2 });
    expect(createSemanticSnapshot(merged.state as Record<string, unknown>).snapshot_id).toBeTruthy();
  });

  it("documents and world model", () => {
    expect(extractDocumentStructure("# H").headings).toBeDefined();
    expect(compileWorldModel({ entities: [{ id: 1 }] }).bounded).toBe(true);
  });
});
