import { describe, expect, it } from "vitest";
import { deriveKaalkaTimeKey } from "../../src/crypto/kaalkaRuntime.js";

describe("deriveKaalkaTimeKey", () => {
  it("is pure and stable", () => {
    const a = deriveKaalkaTimeKey("session-key-🚀");
    const b = deriveKaalkaTimeKey("session-key-🚀");
    expect(a).toBe(b);
    expect(a).toMatch(/^\d{1,2}:\d{1,2}:\d{1,2}$/);
  });
});
