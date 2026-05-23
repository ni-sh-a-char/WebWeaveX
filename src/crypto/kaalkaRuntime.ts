/** Thin adapter — canonical Kaalka lives in the `kaalka` npm package (packages/kaalka). */
export {
  encryptValue,
  decryptValue,
  computeDeterministicHash,
  normalizeRuntimeValue,
  computeDeterministicHashPayload,
} from "kaalka";

/** @deprecated Use computeDeterministicHash */
export { computeDeterministicHash as computeKaalkaHash } from "kaalka";

/** @deprecated Use computeDeterministicHashPayload */
export { computeDeterministicHashPayload as computeKaalkaHashPayload } from "kaalka";
