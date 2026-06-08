import { beforeAll, afterAll, describe, expect, it } from "vitest";
import { spawn, type ChildProcess } from "node:child_process";
import { strategyFor } from "../../src/orchestration/extractionStrategyEngine.js";
import { buildMemoryLineage, verifyMemoryLineage } from "../../src/memory/memoryLineage.js";
import { runDistributedExtraction } from "../../src/distributed/distributedExtractionOrchestrator.js";
import { computeGlobalRuntimeFingerprint } from "../../src/determinism/globalRuntimeFingerprint.js";
import { runSemanticReasoning } from "../../src/semantic/semanticReasoningEngine.js";
import { enqueueExtraction, dequeueExtraction } from "../../src/distributed/extractionQueueEngine.js";
import { parsePythonAst } from "../../src/ast/pythonAstEngine.js";
import { parsePythonAst as repoAst } from "../../src/repository/ast/pythonAstEngine.js";
import { extractSemanticAst } from "../../src/repository/semantic/semanticAstEngine.js";
import { FakeBrowser } from "../../src/browser/syncPlaywright.js";

describe("strategy and lineage branches", () => {
  it("routes strategy by url shape", () => {
    expect(strategyFor("https://github.com/o/r").mode).toBe("repository");
    expect(strategyFor("https://docs.example.com").mode).toBe("documentation");
    expect(strategyFor("https://example.com").mode).toBe("web");
    expect(strategyFor("").mode).toBe("web");
  });

  it("builds and verifies lineage including breaks", () => {
    const built = buildMemoryLineage([
      { tick: 1, kind: "step" },
      { step: 2 },
      {},
    ]);
    expect(built.lineage).toHaveLength(3);
    expect(built.lineage[2]!.tick).toBe(2);
    expect(verifyMemoryLineage(built.lineage)).toBe(true);
    const broken = [...built.lineage];
    broken[1] = { ...broken[1]!, parent_id: "wrong" };
    expect(verifyMemoryLineage(broken)).toBe(false);
    expect(verifyMemoryLineage([])).toBe(true);
  });
});

describe("distributed orchestration branches", () => {
  it("uses provided workers and checkpoint queues", () => {
    const fromCheckpoint = runDistributedExtraction(
      [{ task_id: "t1", priority: 2 }],
      undefined,
      { queue: [{ task_id: "t0", priority: 1, order: 0 }], workers: [{ worker_id: "wq" }] },
      1,
      [{ nodes: [], edges: [] }],
    );
    expect(fromCheckpoint.bounded).toBe(true);
    const withWorkers = runDistributedExtraction(
      [{ task_id: "t2" }],
      [{ worker_id: "w1", status: "idle" }],
    );
    expect(withWorkers.bounded).toBe(true);
    const noWorkers = runDistributedExtraction([]);
    expect(noWorkers.bounded).toBe(true);
  });
});

describe("global fingerprint branches", () => {
  it("derives from extraction fields and explicit args", () => {
    const extraction = {
      runtime: { dom_stabilization: { stabilized_hash: "dh" } },
      browser_ir: { runtime_identity: "rid" },
      unified_runtime_graph: { nodes: [{ id: "n1" }], edges: [{ source: "a", target: "b", type: "t" }] },
      pipeline_hash: "ph",
    };
    const fp1 = computeGlobalRuntimeFingerprint(extraction);
    expect(fp1).toMatch(/^[0-9a-f]{64}$/);
    const fp2 = computeGlobalRuntimeFingerprint(
      extraction,
      { nodes: [], edges: [{ from: "x", to: "y" }] } as never,
      { stable_hash: "sh", memory: { runtime_history: [1, 2] } },
      { convergence: { converged: true } },
      { runtime: { runtime_id: "rrid" } },
      "seal",
    );
    expect(fp2).toMatch(/^[0-9a-f]{64}$/);
    expect(fp2).not.toBe(fp1);
    const spa = computeGlobalRuntimeFingerprint({
      runtime: { spa_stabilization: { stable_dom_hash: "sd" } },
      browser_ir: "not-a-dict",
    } as never);
    expect(spa).toMatch(/^[0-9a-f]{64}$/);
    const memInner = computeGlobalRuntimeFingerprint({}, null, { memory: { stable_hash: "in", runtime_history: [] } });
    expect(memInner).toMatch(/^[0-9a-f]{64}$/);
  });
});

describe("semantic reasoning branches", () => {
  it("handles empty and undefined claims", () => {
    const out = runSemanticReasoning([{ type: "A" }], undefined as never);
    expect(out.bounded).toBe(true);
    expect(out.reasoning_depth).toBe(1);
    const withClaims = runSemanticReasoning([], [{ k: 1 }, "text claim"]);
    expect(withClaims.reasoning_depth).toBe(2);
  });
});

describe("queue field-default branches", () => {
  it("covers each nullable field independently", () => {
    const a = enqueueExtraction([], { url: "u" });
    const b = enqueueExtraction(a.queue, { task_id: "x" });
    const c = enqueueExtraction(b.queue, { priority: 9 });
    expect(c.queue[0]!.priority).toBe(9);
    const noOrder = dequeueExtraction([{ task_id: "k", priority: 1 }, { task_id: "j" }]);
    expect(noOrder.task?.task_id).toBe("k");
  });
});

describe("analyzer residual branches", () => {
  it("covers defaults, annotations and import( guard", () => {
    const out = parsePythonAst(
      "def g(a: int = 1, b='x'):\n    return a\nval = import_helper()\n",
    ) as { functions: { args: string[] }[] };
    expect(out.functions[0]!.args).toEqual(["a", "b"]);
    const noImport = parsePythonAst("x = import_thing(1)\n") as { imports: unknown[] };
    expect(noImport.imports).toEqual([]);
  });

  it("repo ast import aliases and from-form", () => {
    const out = repoAst("import a.b as ab, c\nfrom d import e as f\n") as {
      imports: { module: string; kind: string }[];
    };
    expect(out.imports.map((i) => i.module)).toContain("a.b");
    expect(out.imports.map((i) => i.module)).toContain("c");
    expect(out.imports.find((i) => i.kind === "import_from")?.module).toBe("d");
  });

  it("semantic ast filters kwargs bases and blank classes", () => {
    const out = extractSemanticAst("class Meta(base=Thing):\n    pass\nclass Plain:\n    pass\n");
    expect(out.classes).toContain("Plain");
    expect(out.classes).toContain("Meta");
  });
});

describe("fake page selector branches (live)", () => {
  let server: ChildProcess | null = null;

  beforeAll(async () => {
    server = spawn("python", ["-B", "tools/convergence/probe_http_server.py"], { stdio: "ignore" });
    await new Promise((r) => setTimeout(r, 1200));
  });

  afterAll(() => {
    server?.kill();
  });

  it("matches ids, classes and replays cookies/headers", () => {
    const ctx = new FakeBrowser().new_context("UA/1.0", { width: 640, height: 480 }, "en-GB", "Europe/London");
    ctx.add_cookies([{ name: "probe", value: "1", url: "http://127.0.0.1:8787" }]);
    const page = ctx.new_page();
    page.set_extra_http_headers({ "x-test": "yes" });
    const responses: unknown[] = [];
    page.on("response", (r) => responses.push(r));
    page.goto("http://127.0.0.1:8787/probe");
    expect(page.query_selector("#main")?.inner_text()).toBe("Probe Fixture");
    expect(page.query_selector(".headline")).toBeTruthy();
    expect(page.evaluate("sessionStorage.getItem('x')")).toEqual({});
    expect(responses.length).toBeGreaterThan(0);
    expect(ctx.cookies().length).toBeGreaterThan(0);
  }, 120_000);
});
