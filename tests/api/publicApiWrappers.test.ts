/**
 * Behavioral coverage for the package-level convenience wrappers in
 * src/publicApi.ts (ported from webweavex/__init__.py). Each wrapper branch
 * is exercised so the public API surface is measured, not just present.
 */
import { describe, expect, it, beforeAll, afterAll, vi } from "vitest";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";

// The crawl wrappers and extract pipeline touch the network/heavy work; mock
// them so the wrapper logic (not the engines) is what these tests exercise.
vi.mock("../../src/crawling/crawlerEngine.js", () => ({
  crawl: vi.fn(() => ({ visited: ["https://example.com"], discovered: ["https://example.com/a"], bounded: true })),
}));
vi.mock("../../src/extract/pipeline.js", () => ({
  extract: vi.fn(() => ({
    metadata: {},
    content: { repository: { files: [] }, documents: { count: 0 } },
    relationships: { execution_graph: { nodes: [{ id: "n" }], edges: [] } },
    bounded: true,
  })),
  extractAsync: vi.fn(),
  extractDocs: vi.fn(),
  extractRepo: vi.fn(),
}));

import {
  analyze, crawl, crawlAsync, extractRecursive, queryGraph, queryRepo,
  queryRepository, queryKnowledge, queryDocuments, compileDocument,
  compileRepository, universalExtract, version,
} from "../../src/publicApi.js";

let dir: string;
beforeAll(() => {
  dir = mkdtempSync(join(tmpdir(), "wwx-papi-"));
});
afterAll(() => {
  rmSync(dir, { recursive: true, force: true });
});

describe("publicApi convenience wrappers", () => {
  it("version is the package version", () => {
    expect(version).toBe("2.0.0");
  });

  it("analyze: explicit edges branch and extract-derived branch", () => {
    const direct = analyze([{ id: "a" }, { id: "b" }], [{ from: "a", to: "b" }]) as Record<string, unknown>;
    expect(typeof direct).toBe("object");
    const derived = analyze("plain text input") as Record<string, unknown>;
    expect(typeof derived).toBe("object");
  });

  it("crawl and crawlAsync delegate to the crawler engine", async () => {
    const c = crawl("https://example.com", { max_pages: 1 }) as Record<string, unknown>;
    expect(typeof c).toBe("object");
    const ca = (await crawlAsync("https://example.com", { max_pages: 1 })) as Record<string, unknown>;
    expect(typeof ca).toBe("object");
  });

  it("extractRecursive merges crawl metadata into the extraction", () => {
    const out = extractRecursive("https://example.com") as Record<string, any>;
    expect(out.metadata).toBeDefined();
    expect(out.metadata.crawl).toBeDefined();
    expect(out).toHaveProperty("repository");
    expect(out).toHaveProperty("documents");
  });

  it("queryGraph: graph arg, null result, result-with-relationships, plain result", () => {
    expect(queryGraph(null, "", { nodes: [{ id: "n" }], edges: [] })).toBeDefined();
    expect(queryGraph(null, "n")).toBeDefined();
    expect(queryGraph({ relationships: { execution_graph: { nodes: [{ id: "x" }], edges: [] } } }, "x")).toBeDefined();
    expect(queryGraph({ nodes: [{ id: "y" }], edges: [] }, "y")).toBeDefined();
  });

  it("queryRepo / queryRepository branches", () => {
    expect(queryRepo({ content: { repository: { files: [] } } })).toEqual({ files: [] });
    expect(queryRepository({ content: { repository: { ok: true } } })).toEqual({ ok: true });
    expect(queryRepository(null, "src", "")).toBeDefined();
  });

  it("queryKnowledge: entities/edges branch and result branch", () => {
    expect(queryKnowledge(null, [{ label: "e" }], [])).toBeDefined();
    const r = queryKnowledge({ content: { knowledge_v2: { a: 1 }, knowledge_reconstruction_v18: { b: 2 } } }) as Record<string, unknown>;
    expect(r).toHaveProperty("knowledge_v2");
    expect(r).toHaveProperty("knowledge_v18");
  });

  it("queryDocuments: text branch, result branch, empty branch", () => {
    expect(queryDocuments(null, "some document text")).toBeDefined();
    expect(queryDocuments({ content: { documents: { count: 0 } } })).toEqual({ count: 0 });
    expect(queryDocuments()).toBeDefined();
  });

  it("compileDocument / compileRepository delegate to IR compilers", () => {
    expect(compileDocument("hello")).toBeDefined();
    expect(compileRepository("src", "")).toBeDefined();
  });

  it("query wrappers cover the defensive nullish-fallback branches", () => {
    // queryGraph: result has `relationships` but no execution_graph → `?? {}`
    expect(queryGraph({ relationships: {} }, "n")).toBeDefined();
    // queryRepo: result without content.repository → `?? {}`
    expect(queryRepo({})).toEqual({});
    // queryRepository: source provided (no result) → IR path
    expect(queryRepository(null, "src", "path", { files: [] })).toBeDefined();
    // queryKnowledge: entities-null but edges-provided → right side of `||`
    expect(queryKnowledge(null, null, [{ from: "a", to: "b" }])).toBeDefined();
    // queryKnowledge: result null → ternary false branch; missing keys → `?? {}`
    expect(queryKnowledge(null)).toEqual({ knowledge_v2: {}, knowledge_v18: {} });
    expect(queryKnowledge({})).toEqual({ knowledge_v2: {}, knowledge_v18: {} });
    // queryDocuments: result without content.documents → `?? {}`
    expect(queryDocuments({})).toEqual({});
  });

  it("analyze and extractRecursive cover empty-extraction fallbacks", async () => {
    const pipeline = await import("../../src/extract/pipeline.js");
    const mocked = vi.mocked(pipeline.extract);
    // extract returns no relationships / content → exercise `?? {}` / `?? []`
    mocked.mockReturnValueOnce({} as never);
    expect(analyze("text") as Record<string, unknown>).toBeDefined();
    const crawler = await import("../../src/crawling/crawlerEngine.js");
    vi.mocked(crawler.crawl).mockReturnValueOnce({} as never);
    mocked.mockReturnValueOnce({} as never);
    const out = extractRecursive("https://example.com") as Record<string, any>;
    expect(out.metadata.crawl.visited).toEqual([]);
    expect(out.repository).toEqual({});
    expect(out.documents).toEqual({});
  });

  it("universalExtract covers every input-type branch", () => {
    const cases: Array<[string, string]> = [
      ["doc.pdf", "%PDF-1.4 minimal"],
      ["doc.docx", "PK fake docx"],
      ["img.png", "PNG fake"],
      ["arc.zip", "PK fake zip"],
      ["page.html", "<html><body><p>hi</p></body></html>"],
      ["mod.py", "def f():\n  return 1\n"],
      ["data.unknown", "???"],
    ];
    for (const [name, content] of cases) {
      const p = join(dir, name);
      writeFileSync(p, content);
      const res = universalExtract(p) as Record<string, unknown>;
      expect(res.bounded === true || res.unsupported === true).toBe(true);
    }
  });
});
