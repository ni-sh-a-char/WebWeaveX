/**
 * Parity with core/crypto/kaalka_hash_engine.py
 */
import {
  computeDeterministicHash,
  computeDeterministicHashPayload,
  computeKaalkaHash,
  computeKaalkaHashPayload,
} from "./kaalkaRuntime.js";

export {
  computeDeterministicHash,
  computeDeterministicHashPayload,
  computeKaalkaHash,
  computeKaalkaHashPayload,
};

export const compute_kaalka_hash = computeDeterministicHash;
export const compute_kaalka_hash_payload = computeDeterministicHashPayload;
