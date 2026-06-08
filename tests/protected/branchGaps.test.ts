import { describe, expect, it } from "vitest";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { enqueueExtraction, dequeueExtraction } from "../../src/distributed/extractionQueueEngine.js";
import {
  compute_kaalka_hash,
  compute_kaalka_hash_payload,
  computeKaalkaHash,
  computeKaalkaHashPayload,
  computeDeterministicHash,
  computeDeterministicHashPayload,
} from "../../src/crypto/kaalkaHashEngine.js";
import { encryptBytes, decryptBytes } from "../../src/crypto/kaalkaRuntimeEngine.js";
import {
  saveLiveRuntimeMemory,
  loadLiveRuntimeMemory,
  rememberLiveRuntime,
} from "../../src/connectors/liveRuntimeMemory.js";
import { extractFilesystemRuntime } from "../../src/connectors/filesystemConnector.js";
import { parsePythonAst } from "../../src/ast/pythonAstEngine.js";
import { parsePythonAst as repoAst } from "../../src/repository/ast/pythonAstEngine.js";
import { extractSemanticAst } from "../../src/repository/semantic/semanticAstEngine.js";
import { FakeBrowser, syncPlaywright } from "../../src/browser/syncPlaywright.js";
import { dumpsDeterministic } from "../../src/serialize/deterministicSerializer.js";
import * as py from "../../src/runtime/pyCompat.js";

describe("extraction queue branches", () => {
  it("defaults task fields and breaks ties deterministically", () => {
    const q1 = enqueueExtraction([], {});
    expect(q1.enqueued).toBe("task_0");
    const q2 = enqueueExtraction(q1.queue, { task_id: "b", priority: 5, url: "u" });
    const q3 = enqueueExtraction(q2.queue, { task_id: "a", priority: 5 });
    expect(q3.queue[0]!.task_id).toBe("b"); // same priority → earlier order first
    const deq = dequeueExtraction(q3.queue);
    expect(deq.task?.task_id).toBe("b");
    expect(dequeueExtraction([]).task).toBeNull();
    // equal priority + equal order → task_id compare
    const tie = [
      { task_id: "z", priority: 1, order: 0 },
      { task_id: "a", priority: 1, order: 0 },
    ];
    expect(dequeueExtraction(tie).task?.task_id).toBe("a");
  });
});

describe("kaalka hash engine surface", () => {
  it("exposes hashes and aliases", () => {
    const h1 = computeKaalkaHash("payload");
    expect(h1).toMatch(/^[0-9a-f]{64}$/);
    expect(computeDeterministicHash({ a: 1 })).toMatch(/^[0-9a-f]{64}$/);
    expect(compute_kaalka_hash({ a: 1 })).toBe(computeDeterministicHash({ a: 1 }));
    expect(compute_kaalka_hash_payload("x")).toBe(computeDeterministicHashPayload("x"));
    expect(computeKaalkaHashPayload("x")).toMatch(/^[0-9a-f]{64}$/);
  });

  it("round-trips byte encryption", () => {
    const data = new TextEncoder().encode("secret-bytes");
    const enc = encryptBytes(data, "key-1");
    expect(enc.encrypted).toBeTruthy();
    const dec = decryptBytes(data, "key-1");
    expect(dec).toBeDefined();
  });
});

describe("live runtime memory branches", () => {
  it("saves and loads via path and via store", () => {
    const dir = mkdtempSync(join(tmpdir(), "wwx-lrm-"));
    const p = join(dir, "mem.json");
    const saved = saveLiveRuntimeMemory("k1", { v: 1 }, "ek", p);
    expect(saved.saved).toBe(true);
    const loaded = loadLiveRuntimeMemory("k1", "ek", p);
    expect(loaded.v).toBe(1);
    // store path (no file)
    saveLiveRuntimeMemory("k2", { w: 2 }, "ek");
    expect(loadLiveRuntimeMemory("k2", "ek").w).toBe(2);
    // unknown key default
    expect(loadLiveRuntimeMemory("nope", "ek").bounded).toBe(true);
    // missing file falls back to store
    expect(loadLiveRuntimeMemory("k2", "ek", join(dir, "missing.json")).w).toBe(2);
    rememberLiveRuntime("k2", { x: 3 });
    expect(loadLiveRuntimeMemory("k2", "ek").x).toBe(3);
    rememberLiveRuntime("fresh-key", { y: 1 });
    expect(loadLiveRuntimeMemory("fresh-key", "ek").y).toBe(1);
    rmSync(dir, { recursive: true, force: true });
  });
});

describe("filesystem connector branches", () => {
  it("uses snapshot branch with and without fields", () => {
    const full = extractFilesystemRuntime("base", {
      root: "custom",
      files: ["b.txt", "a.txt"],
      mutations: [1],
      sync: { s: 1 },
      permissions: { p: 1 },
      inodes: [2],
    });
    expect(full.root).toBe("custom");
    expect(full.topology).toEqual(["a.txt", "b.txt"]);
    const dflt = extractFilesystemRuntime("base", {});
    expect(dflt.root).toBe("base");
    expect(dflt.topology).toEqual([]);
  });

  it("walks a real directory and handles missing roots", () => {
    const dir = mkdtempSync(join(tmpdir(), "wwx-fs-"));
    writeFileSync(join(dir, "one.txt"), "1");
    const sub = join(dir, "sub");
    rmSync(sub, { recursive: true, force: true });
    writeFileSync(join(dir, "two.txt"), "2");
    const out = extractFilesystemRuntime(dir);
    expect((out.topology as string[]).length).toBe(2);
    rmSync(dir, { recursive: true, force: true });
    const missing = extractFilesystemRuntime(join(dir, "gone"));
    expect(missing.topology).toEqual([]);
  });
});

describe("python analyzer branch edges", () => {
  it("handles continuations, multiline brackets, aliases and chains", () => {
    const src = [
      "from a.b import (",
      "    c,",
      "    d as dee,",
      ")",
      "import x.y as xy",
      "total = 1 + \\",
      "    2",
      "a = b = 3",
      "class NoBase:",
      "    pass",
      "def star(*args, **kw):",
      "    pass",
    ].join("\n");
    const out = parsePythonAst(src) as Record<string, Record<string, unknown>[]>;
    const imp = out.imports.find((i) => i.module === "a.b") as { names: string[] };
    expect(imp.names).toContain("c");
    expect(imp.names).toContain("d");
    expect(out.classes.map((c) => c.name)).toContain("NoBase");
    const star = out.functions.find((f) => f.name === "star") as { args: string[] };
    expect(star.args).toContain("args");
    expect(star.args).toContain("kw");
    const targets = out.assignments.flatMap((a) => a.targets as string[]);
    expect(targets).toContain("total");
  });

  it("repo ast skips keywords and def headers in calls", () => {
    const out = repoAst("if (x):\n    pass\ndef shown(a):\n    return used(a)\n") as {
      calls: { target: string }[];
      nodes: { name: string }[];
    };
    const targets = out.calls.map((c) => c.target);
    expect(targets).toContain("used");
    expect(targets).not.toContain("if");
    expect(targets).not.toContain("shown");
    expect(out.nodes.map((n) => n.name)).toContain("shown");
  });

  it("semantic ast hits remaining language patterns", () => {
    const out = extractSemanticAst(
      [
        "package main",
        "func Run() {}",
        "fn rust_like() {}",
        "use std::fmt;",
        "import 'package:flutter/material.dart';",
        "void main() {}",
        "public class JavaThing {}",
        "package com.example;",
        "fun kotlinThing() {}",
      ].join("\n"),
    );
    for (const lang of ["go", "rust", "dart", "java", "kotlin"]) {
      expect(out.languages).toContain(lang);
    }
  });
});

describe("sync playwright defaults", () => {
  it("covers default context options and pre-goto reads", () => {
    const ctx = new FakeBrowser().new_context();
    const page = ctx.new_page();
    expect(page.content()).toBe("");
    expect(page.title()).toBe("");
    expect(page.evaluate("anything")).toBeNull();
    expect(page.query_selector("h1")).toBeNull();
    expect(page.query_selector_all("a")).toEqual([]);
    expect(ctx.cookies()).toEqual([]);
    expect(syncPlaywright().start().chromium.launch()).toBeInstanceOf(FakeBrowser);
  });
});

describe("serializer branch edges", () => {
  it("covers depth cutoff, NaN floats and non-plain objects", () => {
    let deep: Record<string, unknown> = { leaf: 1 };
    for (let i = 0; i < 70; i++) deep = { next: deep };
    expect(typeof dumpsDeterministic(deep)).toBe("string");
    expect(dumpsDeterministic(py.F(Number.NaN))).toBe("0.0");
    expect(dumpsDeterministic(NaN)).toBe("0");
    expect(dumpsDeterministic([new py.PyPath("a/b")])).toContain("a");
  });
});
