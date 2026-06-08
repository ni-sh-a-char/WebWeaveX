import { describe, expect, it } from "vitest";
import { enqueueExtraction, dequeueExtraction } from "../../src/distributed/extractionQueueEngine.js";
import { computeGlobalRuntimeFingerprint } from "../../src/determinism/globalRuntimeFingerprint.js";
import { parsePythonAst } from "../../src/ast/pythonAstEngine.js";
import { parsePythonAst as repoAst } from "../../src/repository/ast/pythonAstEngine.js";
import { buildDistributedRuntimeGraph } from "../../src/distributed/distributedRuntimeGraphEngine.js";
import { loadStreamRuntime, saveStreamRuntime } from "../../src/streaming/streamPersistence.js";
import { makeStreamEvent } from "../../src/streaming/streamCapture.js";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";

describe("queue comparator tie branches", () => {
  it("falls through priority → order → task_id in enqueue sorting", () => {
    const preexisting = [
      { task_id: "zz", priority: 1, order: 0 },
      { task_id: "aa", priority: 1, order: 0 },
      { task_id: "mm" }, // no priority, no order
    ];
    const out = enqueueExtraction(preexisting, { task_id: "new", priority: 1 });
    const ids = out.queue.map((t) => t.task_id);
    expect(ids.indexOf("aa")).toBeLessThan(ids.indexOf("zz"));
    expect(out.queue.some((t) => t.task_id === "mm")).toBe(true);
    const deq = dequeueExtraction([
      { task_id: "b", priority: 2, order: 1 },
      { task_id: "a", priority: 2, order: 0 },
      { priority: 2, order: 0, task_id: "a2" },
    ]);
    expect(deq.task?.task_id).toBe("a");
  });
});

describe("fingerprint nullable graph fields", () => {
  it("normalizes nodes/edges missing ids and endpoints", () => {
    const fp = computeGlobalRuntimeFingerprint({
      unified_runtime_graph: {
        nodes: [{}, { id: "n" }],
        edges: [{}, { from: "f", to: "t" }, { source: "s", target: "g", type: "k" }],
      },
    } as never);
    expect(fp).toMatch(/^[0-9a-f]{64}$/);
    const noGraph = computeGlobalRuntimeFingerprint({}, undefined as never);
    expect(noGraph).toMatch(/^[0-9a-f]{64}$/);
  });
});

describe("analyzer edge branches", () => {
  it("handles inline comments, arrow returns and unterminated groups", () => {
    const out = parsePythonAst(
      "x = call(1)  # trailing comment\ndef typed() -> int:\n    return 1\n",
    ) as { functions: { name: string }[]; assignments: { targets: string[] }[] };
    expect(out.functions.map((f) => f.name)).toContain("typed");
    expect(out.assignments.flatMap((a) => a.targets)).toContain("x");
    // unterminated bracket flushes the trailing buffer
    const tail = parsePythonAst("y = func(\n    1,\n") as { assignments: { targets: string[] }[] };
    expect(tail.assignments.flatMap((a) => a.targets)).toContain("y");
    // tabs in indentation
    const tabbed = parsePythonAst("def t():\n\tz = 1\n") as { functions: unknown[] };
    expect(tabbed.functions).toHaveLength(1);
  });

  it("repo ast covers no-path error and call-at-start", () => {
    const errOut = repoAst("<bad>") as { parse_error: string };
    expect(errOut.parse_error).toContain("<python>");
    const calls = repoAst("run(1)\n") as { calls: { target: string }[] };
    expect(calls.calls.map((c) => c.target)).toContain("run");
  });
});

describe("distributed graph + stream persistence branches", () => {
  it("covers worker/node fallbacks", () => {
    const g = buildDistributedRuntimeGraph(
      [{ status: "busy" }, { worker_id: "w", identity: { fingerprint_hash: "h" } }],
      {} as never,
    );
    expect((g.nodes as unknown[]).length).toBeGreaterThan(0);
    const g2 = buildDistributedRuntimeGraph([], { nodes: [{ id: "n" }], edges: [{ from: "n", to: "n2" }] });
    expect(g2.edges).toBeDefined();
  });

  it("covers stream load fallbacks", () => {
    const dir = mkdtempSync(join(tmpdir(), "wwx-st-"));
    const missing = loadStreamRuntime(join(dir, "nope.json"), "k");
    expect(missing.events).toEqual([]);
    const okPath = join(dir, "ok.json");
    saveStreamRuntime(okPath, { events: [makeStreamEvent(1, "s", "in", "{}", "c")] }, "k2");
    expect(loadStreamRuntime(okPath, "k2").events.length).toBe(1);
    writeFileSync(join(dir, "noenc.json"), JSON.stringify({ other: 1 }));
    expect(loadStreamRuntime(join(dir, "noenc.json"), "k").events).toEqual([]);
    rmSync(dir, { recursive: true, force: true });
  });
});
