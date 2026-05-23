import { describe, expect, it } from "vitest";
import { deriveKaalkaTimeKey } from "../../src/crypto/kaalkaRuntime.js";
import { kaalkaV5DecryptBytes, kaalkaV5EncryptBytes } from "../../src/crypto/kaalkaV5Client.js";

describe("kaalka v5 npm client", () => {
  it("round-trips UTF-8 bytes with derived time key", () => {
    const timeKey = deriveKaalkaTimeKey("k");
    expect(timeKey).toMatch(/^\d{1,2}:\d{1,2}:\d{1,2}$/);
    const payload = Buffer.from("café 🚀", "utf8");
    const enc = kaalkaV5EncryptBytes(payload, timeKey);
    expect(kaalkaV5DecryptBytes(enc, timeKey).equals(payload)).toBe(true);
  });
});
