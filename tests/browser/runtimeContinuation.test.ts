import { describe, expect, it, vi } from "vitest";
import { mkdtempSync, rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import {
  continueAuthenticatedRuntime,
  extractWithSession,
} from "../../src/browser/runtimeContinuation.js";
import { createRuntimeSession, persistRuntimeSession } from "../../src/browser/runtimeSession.js";

vi.mock("playwright", () => ({
  chromium: {
    launch: vi.fn(async () => ({
      newContext: vi.fn(async () => ({
        addCookies: vi.fn(async () => undefined),
        newPage: vi.fn(async () => ({
          addInitScript: vi.fn(async () => undefined),
          goto: vi.fn(async () => undefined),
        })),
      })),
      close: vi.fn(async () => undefined),
    })),
  },
}));

describe("runtime continuation", () => {
  it("extractWithSession applies playwright path", async () => {
    const session = createRuntimeSession({
      cookies: [{ name: "sid", value: "1", domain: "example.com", path: "/" }],
      headers: { "x-test": "1" },
      localStorage: { theme: "dark" },
    });
    const out = await extractWithSession("https://example.com", session, 1);
    expect(out.bounded).toBe(true);
    expect(out.unified_runtime_graph).toBeDefined();
    const cont = (out.runtime as Record<string, unknown>).session as Record<string, unknown>;
    expect(cont.continuation).toBe(true);
  });

  it("continueAuthenticatedRuntime restores session file", async () => {
    const dir = mkdtempSync(join(tmpdir(), "wwx-cont-"));
    const path = join(dir, "sess.kaalka");
    const session = createRuntimeSession({ cookies: [] });
    persistRuntimeSession(path, session, "key-cont");
    const out = await continueAuthenticatedRuntime("https://example.com", {
      sessionPath: path,
      encryptionKey: "key-cont",
      tick: 2,
    });
    expect(out.pipeline_hash).toBeTruthy();
    rmSync(dir, { recursive: true, force: true });
  });
});
