import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it, vi } from "vitest";
import { saveAuthenticatedRuntime } from "../../src/browser/authenticatedRuntime.js";

vi.mock("../../src/browser/captureRuntime.js", () => ({
  captureRuntime: vi.fn(async () => ({
    available: true,
    url: "https://example.com",
    dom_hash: "h",
    storage: { localStorage: {}, sessionStorage: {} },
    network: [],
    routes: [],
    bounded: true,
  })),
}));

describe("extractWeb auth", () => {
  it("loads session", async () => {
    const dir = mkdtempSync(join(tmpdir(), "wwx-"));
    const path = join(dir, "s.kaalka");
    saveAuthenticatedRuntime(path, { cookies: [], headers: {} }, "key");
    const { extractWeb } = await import("../../src/browser/extractWeb.js");
    const out = await extractWeb("https://example.com", {
      authenticated: true,
      sessionPath: path,
      encryptionKey: "key",
      semanticRuntime: true,
    });
    expect((out.runtime as Record<string, unknown>).session).toBeTruthy();
    expect(out.semantic).toBeTruthy();
  });
});
