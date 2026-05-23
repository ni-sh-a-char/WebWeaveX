import { mkdtempSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import {
  loadAuthenticatedRuntime,
  rotateAuthenticatedSession,
  saveAuthenticatedRuntime,
} from "../../src/browser/authenticatedRuntime.js";

describe("authenticated runtime", () => {
  it("save load rotate", () => {
    const dir = mkdtempSync(join(tmpdir(), "wwx-"));
    const path = join(dir, "session.kaalka");
    saveAuthenticatedRuntime(path, { cookies: [], headers: {} }, "key");
    const raw = readFileSync(path, "utf-8");
    expect(raw).toContain("kaalka");
    const loaded = loadAuthenticatedRuntime(path, "key");
    expect(loaded.headers).toEqual({});
    const rotated = rotateAuthenticatedSession(loaded);
    expect(rotated.headers?.["x-kaalka-rotated"]).toBe("1");
  });
});
