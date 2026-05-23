import { readFileSync, writeFileSync, existsSync } from "node:fs";
import stringify from "fast-json-stable-stringify";
import { encryptValue, decryptValue } from "../crypto/kaalkaRuntime.js";

const store = new Map<string, Record<string, unknown>>();

export function saveLiveRuntimeMemory(
  key: string,
  memory: Record<string, unknown>,
  encryptionKey: string,
  path?: string,
): Record<string, unknown> {
  const enc = encryptValue(memory, encryptionKey).encrypted;
  store.set(key, memory);
  if (path) {
    writeFileSync(path, stringify({ encrypted: enc, version: "2.0.0" }), "utf-8");
  }
  return { saved: true, key, bounded: true };
}

export function loadLiveRuntimeMemory(
  key: string,
  encryptionKey: string,
  path?: string,
): Record<string, unknown> {
  if (path && existsSync(path)) {
    const raw = JSON.parse(readFileSync(path, "utf-8")) as { encrypted: string };
    const dec = decryptValue(raw.encrypted, encryptionKey);
    return JSON.parse(dec.decrypted) as Record<string, unknown>;
  }
  return store.get(key) ?? { bounded: true };
}

export function rememberLiveRuntime(key: string, fragment: Record<string, unknown>): void {
  const prev = store.get(key) ?? {};
  store.set(key, { ...prev, ...fragment, bounded: true });
}
