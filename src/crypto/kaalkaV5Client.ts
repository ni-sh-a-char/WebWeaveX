/**
 * Thin sync bridge to npm `kaalka@5.0.0` (CommonJS Kaalka class).
 * Uses byte `_proc` (lossless UTF-8) — not `_encryptMessage` (BMP-only strings).
 */
import { createRequire } from "node:module";

type KaalkaInstance = {
  _setTime(timeKey?: string): void;
  _proc(data: Buffer, encrypt: boolean): Buffer;
};

type KaalkaCtor = new () => KaalkaInstance;

const require = createRequire(import.meta.url);
const Kaalka = require("kaalka") as KaalkaCtor;

export function kaalkaV5EncryptBytes(payloadUtf8: Buffer, timeKey: string): Buffer {
  const instance = new Kaalka();
  instance._setTime(timeKey);
  return instance._proc(payloadUtf8, true);
}

export function kaalkaV5DecryptBytes(ciphertext: Buffer, timeKey: string): Buffer {
  const instance = new Kaalka();
  instance._setTime(timeKey);
  return instance._proc(ciphertext, false);
}
