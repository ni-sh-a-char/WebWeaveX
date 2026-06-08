import { describe, expect, it } from "vitest";
import { enqueueExtraction, dequeueExtraction } from "../../src/distributed/extractionQueueEngine.js";
import { computeGlobalRuntimeFingerprint } from "../../src/determinism/globalRuntimeFingerprint.js";
import { dumpsDeterministic } from "../../src/serialize/deterministicSerializer.js";
import { reconstructBrowserState } from "../../src/reconstruction/reconstructBrowser.js";
import { mergeStreamRuntimePayloads, loadStreamRuntime, saveStreamRuntime } from "../../src/streaming/streamPersistence.js";
import { buildDistributedRuntimeGraph } from "../../src/distributed/distributedRuntimeGraphEngine.js";
import { ParserRegistry } from "../../src/parsers/parserRegistry.js";
import { FakeContext, FakeBrowser } from "../../src/browser/syncPlaywright.js";
import { encryptValue, decryptValue } from "../../src/crypto/kaalkaRuntime.js";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";

describe("nfc-colliding serializer keys", () => {
  it("hits the equal-key comparator arm via unicode normalization", () => {
    const composed = "é"; // é
    const decomposed = "é"; // e + combining acute
    const out = dumpsDeterministic({ [composed]: 1, [decomposed]: 2 });
    expect(out).toContain("é");
  });
});

describe("queue same-priority different-order pairs", () => {
  it("hits the order comparator arm in dequeue", () => {
    const deq = dequeueExtraction([
      { task_id: "later", priority: 4, order: 9 },
      { task_id: "sooner", priority: 4, order: 1 },
    ]);
    expect(deq.task?.task_id).toBe("sooner");
    const enq = enqueueExtraction(
      [
        { task_id: "o2", priority: 7, order: 2 },
        { task_id: "o1", priority: 7, order: 1 },
      ],
      { task_id: "low", priority: 0 },
    );
    expect(enq.queue[0]!.task_id).toBe("o1");
  });
});

describe("queue adjacent tie pairs", () => {
  it("hits the task_id comparator in both sorts", () => {
    const tiePair = [
      { task_id: "z", priority: 3, order: 5 },
      { task_id: "a", priority: 3, order: 5 },
    ];
    const enq = enqueueExtraction(tiePair, { task_id: "filler", priority: 0 });
    const ids = enq.queue.map((t) => t.task_id);
    expect(ids.indexOf("a")).toBeLessThan(ids.indexOf("z"));
    const deq = dequeueExtraction(tiePair);
    expect(deq.task?.task_id).toBe("a");
  });
});

describe("fingerprint argument arms", () => {
  it("covers empty-graph and non-dict ir arms", () => {
    expect(computeGlobalRuntimeFingerprint({})).toMatch(/^[0-9a-f]{64}$/);
    expect(
      computeGlobalRuntimeFingerprint({ runtime: [], browser_ir: 42 } as never),
    ).toMatch(/^[0-9a-f]{64}$/);
    expect(
      computeGlobalRuntimeFingerprint({ browser_ir: { other: 1 } } as never),
    ).toMatch(/^[0-9a-f]{64}$/);
  });
});

describe("serializer comparator arms", () => {
  it("sorts descending keys, equal items and mixed arrays", () => {
    expect(dumpsDeterministic({ z: 1, a: 2 })).toBe('{"a":2,"z":1}');
    expect(dumpsDeterministic({ a: 2, z: 1 })).toBe('{"a":2,"z":1}');
    expect(dumpsDeterministic([{ b: 1 }, { a: 1 }, { a: 1 }])).toBe('[{"a":1},{"a":1},{"b":1}]');
    expect(dumpsDeterministic([2, 1, 1])).toBe("[1,1,2]");
  });
});

describe("reconstruct browser arms", () => {
  it("covers route paths, session fallbacks and storage", () => {
    const withRoutes = reconstructBrowserState({
      browser_ir: {
        routes: { history: [{ path: "/x" }, {}] },
        storage: { ls: 1 },
      },
      runtime: { session: "rt-session" },
    } as never);
    expect(withRoutes.tabs.map((t) => t.path)).toContain("/x");
    expect(withRoutes.tabs.map((t) => t.path)).toContain("/");
    expect(withRoutes.session.session_id).toBe("rt-session");
    expect(withRoutes.storage).toEqual({ ls: 1 });

    const withSession = reconstructBrowserState(
      { browser_ir: {} } as never,
      { session_id: "explicit" } as never,
    );
    expect(withSession.session.session_id).toBe("explicit");
    expect(withSession.tabs[0]!.path).toBe("/");
  });
});

describe("stream persistence arms", () => {
  it("covers events-missing decrypt and timestampless sort", () => {
    const dir = mkdtempSync(join(tmpdir(), "wwx-sp-"));
    const p = join(dir, "noevents.json");
    const enc = encryptValue(JSON.stringify({ other: true }), "k").encrypted as string;
    writeFileSync(p, JSON.stringify({ encrypted: enc }));
    expect(loadStreamRuntime(p, "k").events).toEqual([]);
    const merged = mergeStreamRuntimePayloads([
      { events: [{ id: "n", source: "s", direction: "in", payload: "{}", connection_id: "c" }] },
      { events: [{ timestamp: 5, id: "t", source: "s", direction: "in", payload: "{}", connection_id: "c" }] },
    ]);
    expect(Number(merged.events[0]!.timestamp ?? 0)).toBeLessThanOrEqual(Number(merged.events[1]!.timestamp ?? 0));
    rmSync(dir, { recursive: true, force: true });
    expect(typeof decryptValue(enc, "k").decrypted).toBe("string");
    // round-trip via save for the success arm
    const dir2 = mkdtempSync(join(tmpdir(), "wwx-sp2-"));
    const ok = join(dir2, "ok.json");
    saveStreamRuntime(ok, { events: [] }, "k3");
    expect(loadStreamRuntime(ok, "k3").events).toEqual([]);
    rmSync(dir2, { recursive: true, force: true });
  });
});

describe("distributed graph node arms", () => {
  it("covers topology nodes without ids/types and worker status default", () => {
    const g = buildDistributedRuntimeGraph(
      [{ worker_id: "w1" }, { worker_id: "w2", status: "busy" }],
      { nodes: [{}, { id: "n", type: "custom" }], edges: [] } as never,
    );
    const nodes = g.nodes as { id: string; type: string }[];
    expect(nodes.some((n) => n.type === "runtime")).toBe(true);
    expect(nodes.some((n) => n.type === "custom")).toBe(true);
    expect((g.edges as unknown[]).length).toBeGreaterThan(0);
  });
});

describe("parser registry arms", () => {
  it("covers language-as-source-id and parse_error evidence", () => {
    const noPath = ParserRegistry.parse("plain words only");
    expect(noPath.source_id).toBe("text");
    const errPy = ParserRegistry.parse("<not python>", "broken.py");
    expect(errPy.language).toBe("python");
    const evidence = errPy.evidence as Record<string, unknown>;
    expect(evidence.parse_error).toBe(true);
  });
});

describe("fake context nullish arms", () => {
  it("covers explicit null context options and undefined cookie lists", () => {
    const ctx = new FakeContext(null, null, null, null);
    expect(ctx.opts.user_agent).toBe("");
    expect(ctx.opts.locale).toBe("en-US");
    ctx.add_cookies(undefined as never);
    expect(ctx.cookies()).toEqual([]);
    expect(new FakeBrowser().new_context(undefined, undefined, undefined, undefined)).toBeInstanceOf(FakeContext);
  });
});
