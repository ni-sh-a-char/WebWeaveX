/**
 * Kaalka v5 proc — production parity with core/crypto/kaalka_v5_proc.py
 */
export const KAALKA_FALLBACK_TIME_KEY = "12:0:0";

const ROUNDTRIP_PROBE = Buffer.from("\x00\x7f\xff🚀probe", "utf8");

import { kaalkaV5DecryptBytes, kaalkaV5EncryptBytes } from "./kaalkaV5Client.js";
import { toInt } from "../runtime/pyCompat.js";

export function parseTimeKey(timeKey: string): [number, number, number] {
  const parts = String(timeKey).split(":");
  let h = 0;
  let m = 0;
  let s = 0;
  if (parts.length === 3) {
    h = toInt(parts[0]);
    m = toInt(parts[1]);
    s = toInt(parts[2]);
  } else if (parts.length === 2) {
    m = toInt(parts[0]);
    s = toInt(parts[1]);
  } else if (parts.length === 1 && parts[0]) {
    s = toInt(parts[0]);
  }
  return [((h % 12) + 12) % 12, m, s];
}

export function kaalkaV5Proc(data: Uint8Array, encrypt: boolean, timeKey: string): Uint8Array {
  const buf = Buffer.from(data);
  return encrypt
    ? kaalkaV5EncryptBytes(buf, timeKey)
    : kaalkaV5DecryptBytes(buf, timeKey);
}

export function kaalkaTimeKeyRoundTrips(timeKey: string): boolean {
  try {
    const enc = kaalkaV5EncryptBytes(ROUNDTRIP_PROBE, timeKey);
    const dec = kaalkaV5DecryptBytes(enc, timeKey);
    return dec.equals(ROUNDTRIP_PROBE);
  } catch {
    return false;
  }
}
