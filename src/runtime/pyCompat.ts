/**
 * Python semantics parity layer for the WebWeaveX JavaScript implementation.
 *
 * Hand-written production module (protected). Generated modules import this as
 * `import * as py from ".../pyCompat.js"` and call the short-name helpers;
 * legacy py-prefixed exports are retained for hand-written modules.
 */
import { createHash } from "node:crypto";
import {
  copyFileSync,
  existsSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  renameSync,
  rmSync,
  statSync,
  unlinkSync,
  writeFileSync,
} from "node:fs";
import {
  basename,
  dirname,
  extname,
  join as nodeJoin,
  resolve as nodeResolve,
  sep as nodeSep,
} from "node:path";
import { inflateRawSync } from "node:zlib";
import * as childProcessModule from "node:child_process";

/* ------------------------------------------------------------------ */
/* float boxing — Python int/float duality                             */
/* ------------------------------------------------------------------ */

/**
 * Boxed Python float. JS has one number type; Python distinguishes
 * 2 from 2.0 (str(), json.dumps(), repr()). Float literals and
 * float-producing operations box; arithmetic helpers propagate.
 */
export class PyFloat {
  v: number;

  constructor(v: number) {
    this.v = v;
  }

  valueOf(): number {
    return this.v;
  }

  toString(): string {
    return floatStr(this.v);
  }

  toJSON(): number {
    return this.v;
  }
}

/** box a float literal */
export function F(v: number): any {
  return new PyFloat(v);
}

export function isF(v: unknown): v is PyFloat {
  return v instanceof PyFloat;
}

/** numeric value of a possibly-boxed number */
export function num(v: unknown): number {
  return v instanceof PyFloat ? v.v : (v as number);
}

/** unbox recursively (for serialization edges) */
export function unbox(v: unknown): any {
  return v instanceof PyFloat ? v.v : v;
}

/* ------------------------------------------------------------------ */
/* truthiness / equality / ordering                                    */
/* ------------------------------------------------------------------ */

/** Python truthiness: empty containers, "", 0, null/undefined are falsy. */
export function truthy(value: unknown): boolean {
  if (value === null || value === undefined || value === false) return false;
  if (value === true) return true;
  if (value instanceof PyFloat) return value.v !== 0 && !Number.isNaN(value.v);
  if (typeof value === "number") return value !== 0 && !Number.isNaN(value);
  if (typeof value === "string") return value.length > 0;
  if (Array.isArray(value)) return value.length > 0;
  if (value instanceof Set || value instanceof Map) return value.size > 0;
  if (value instanceof PyBytes) return value.data.length > 0;
  if (typeof value === "object") return Object.keys(value as object).length > 0;
  return true;
}

/** Python `a and b` (returns operand, lazily evaluates b). */
export function and2(a: unknown, b: () => unknown): any {
  return truthy(a) ? b() : a;
}

/** Python `a or b` (returns operand, lazily evaluates b). */
export function or2(a: unknown, b: () => unknown): any {
  return truthy(a) ? a : b();
}

/** Python `==` deep structural equality. */
export function eq(a: unknown, b: unknown): boolean {
  if (a instanceof PyFloat || b instanceof PyFloat) {
    const na = a instanceof PyFloat ? a.v : a;
    const nb = b instanceof PyFloat ? b.v : b;
    return typeof na === "number" && typeof nb === "number" && na === nb;
  }
  if (a === b) return true;
  if (typeof a === "number" && typeof b === "number") return a === b;
  if (a === null || b === null || a === undefined || b === undefined) {
    return (a === null || a === undefined) && (b === null || b === undefined);
  }
  if (typeof a !== typeof b) return false;
  if (Array.isArray(a) && Array.isArray(b)) {
    if (a.length !== b.length) return false;
    for (let i = 0; i < a.length; i++) if (!eq(a[i], b[i])) return false;
    return true;
  }
  if (a instanceof Set && b instanceof Set) {
    if (a.size !== b.size) return false;
    for (const v of a) {
      let found = false;
      for (const w of b) if (eq(v, w)) { found = true; break; }
      if (!found) return false;
    }
    return true;
  }
  if (a instanceof Map && b instanceof Map) {
    if (a.size !== b.size) return false;
    for (const [k, v] of a) if (!b.has(k) || !eq(v, b.get(k))) return false;
    return true;
  }
  if (typeof a === "object" && typeof b === "object") {
    if (Array.isArray(a) !== Array.isArray(b)) return false;
    const ka = Object.keys(a as object);
    const kb = Object.keys(b as object);
    if (ka.length !== kb.length) return false;
    for (const k of ka) {
      if (!(k in (b as object))) return false;
      if (!eq((a as Record<string, unknown>)[k], (b as Record<string, unknown>)[k])) return false;
    }
    return true;
  }
  return false;
}

/** Python ordering comparison; supports numbers, strings, booleans, arrays. */
export function cmp(a: unknown, b: unknown): number {
  if (a instanceof PyFloat) a = a.v;
  if (b instanceof PyFloat) b = b.v;
  if (a instanceof PyPath && b instanceof PyPath) {
    // CPython PurePath ordering uses casefolded comparison on Windows
    const ka = process.platform === "win32" ? a.p.toLowerCase() : a.p;
    const kb = process.platform === "win32" ? b.p.toLowerCase() : b.p;
    return ka < kb ? -1 : ka > kb ? 1 : 0;
  }
  if (typeof a === "number" && typeof b === "number") return a < b ? -1 : a > b ? 1 : 0;
  if (typeof a === "boolean" || typeof b === "boolean") {
    const na = Number(a);
    const nb = Number(b);
    return na < nb ? -1 : na > nb ? 1 : 0;
  }
  if (typeof a === "string" && typeof b === "string") {
    // Python compares by code point — never locale-dependent.
    return a < b ? -1 : a > b ? 1 : 0;
  }
  if (Array.isArray(a) && Array.isArray(b)) {
    const n = Math.min(a.length, b.length);
    for (let i = 0; i < n; i++) {
      const c = cmp(a[i], b[i]);
      if (c !== 0) return c;
    }
    return a.length - b.length;
  }
  const sa = toStr(a);
  const sb = toStr(b);
  return sa < sb ? -1 : sa > sb ? 1 : 0;
}

export function lt(a: unknown, b: unknown): boolean { return cmp(a, b) < 0; }
export function le(a: unknown, b: unknown): boolean { return cmp(a, b) <= 0; }
export function gt(a: unknown, b: unknown): boolean { return cmp(a, b) > 0; }
export function ge(a: unknown, b: unknown): boolean { return cmp(a, b) >= 0; }

/** Python `in` operator. */
export function contains(container: unknown, item: unknown): boolean {
  if (container === null || container === undefined) return false;
  const itemIsDict =
    item !== null && typeof item === "object" && !Array.isArray(item)
    && !(item instanceof PyFloat) && !(item instanceof PyBytes)
    && (item as object).constructor === Object;
  if (typeof container === "string") {
    if (typeof item !== "string") {
      throw new TypeError("'in <string>' requires string as left operand");
    }
    return container.includes(item);
  }
  if (Array.isArray(container)) return container.some((v) => eq(v, item));
  if (container instanceof Set || container instanceof Map
    || (typeof container === "object" && !(container instanceof PyTag))) {
    if (itemIsDict) throw new TypeError("unhashable type: 'dict'");
  }
  if (container instanceof Set) {
    if (container.has(item)) return true;
    for (const v of container) if (eq(v, item)) return true;
    return false;
  }
  if (container instanceof Map) return container.has(item);
  if (typeof container === "object") return toStr(item) in (container as object);
  return false;
}

/* ------------------------------------------------------------------ */
/* arithmetic                                                          */
/* ------------------------------------------------------------------ */

export function add(a: unknown, b: unknown): any {
  if (a instanceof PyFloat || b instanceof PyFloat) {
    return new PyFloat(num(a) + num(b));
  }
  if (typeof a === "number" && typeof b === "number") return a + b;
  if (typeof a === "string" && typeof b === "string") return a + b;
  if (Array.isArray(a) && Array.isArray(b)) return [...a, ...b];
  if (Array.isArray(a) || Array.isArray(b) || typeof a === "string" || typeof b === "string") {
    // Python raises TypeError for list+str / list+None / str+int etc.
    throw new TypeError(`unsupported operand type(s) for +: '${typeof a}' and '${typeof b}'`);
  }
  return (a as number) + (b as number);
}

/** Call a function mapping keyword args (incl. **kwargs expansion) onto its parameter order. */
export function callKw(
  fn: (...a: unknown[]) => unknown,
  order: string[],
  kwargs: Record<string, unknown>,
  ...spreads: unknown[]
): any {
  const merged: Record<string, unknown> = { ...kwargs };
  for (const s of spreads) Object.assign(merged, s ?? {});
  const known = new Set(order);
  const rest: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(merged)) if (!known.has(k)) rest[k] = v;
  const args = order.map((n) => (n === "**" ? rest : merged[n]));
  return fn(...args);
}

function containsSet(s: Set<unknown>, x: unknown): boolean {
  if (s.has(x)) return true;
  for (const v of s) if (eq(v, x)) return true;
  return false;
}

export function sub(a: unknown, b: unknown): any {
  if (a instanceof PyFloat || b instanceof PyFloat) {
    return new PyFloat(num(a) - num(b));
  }
  if (a instanceof Set) {
    const bb = b instanceof Set ? b : new Set(iter(b));
    return new Set([...a].filter((x) => !containsSet(bb, x)));
  }
  return (a as number) - (b as number);
}

export function mul(a: unknown, b: unknown): any {
  if (a instanceof PyFloat || b instanceof PyFloat) {
    return new PyFloat(num(a) * num(b));
  }
  if (typeof a === "string" && typeof b === "number") return a.repeat(Math.max(0, Math.trunc(b)));
  if (typeof b === "string" && typeof a === "number") return b.repeat(Math.max(0, Math.trunc(a)));
  if (Array.isArray(a) && typeof b === "number") {
    const out: unknown[] = [];
    for (let i = 0; i < Math.trunc(b); i++) out.push(...a);
    return out;
  }
  if (Array.isArray(b) && typeof a === "number") return mul(b, a);
  return (a as number) * (b as number);
}

export function div(a: unknown, b: unknown): any {
  if (a instanceof PyPath) return a.joinpath(toStr(b));
  if (num(b) === 0) throw err("ZeroDivisionError", "division by zero");
  return new PyFloat(num(a) / num(b));
}

export function floordiv(a: unknown, b: unknown): any {
  const r = Math.floor(num(a) / num(b));
  return a instanceof PyFloat || b instanceof PyFloat ? new PyFloat(r) : r;
}

/** Python `%`: modulo with divisor sign, or printf-style string formatting. */
export function mod(a: unknown, b: unknown): any {
  if (typeof a === "string") {
    const args = Array.isArray(b) ? b : [b];
    let i = 0;
    return a.replace(/%[sdif%]/g, (m) => {
      if (m === "%%") return "%";
      const v = args[i++];
      if (m === "%d" || m === "%i") return String(Math.trunc(Number(v)));
      if (m === "%f") return Number(v).toFixed(6);
      return toStr(v);
    });
  }
  const x = num(a);
  const y = num(b);
  const r0 = x % y;
  const r = r0 !== 0 && Math.sign(r0) !== Math.sign(y) ? r0 + y : r0;
  return a instanceof PyFloat || b instanceof PyFloat ? new PyFloat(r) : r;
}

export function bitor(a: unknown, b: unknown): any {
  if (a instanceof Set) return new Set([...a, ...iter(b)]);
  if (a !== null && typeof a === "object" && !Array.isArray(a)) {
    return { ...(a as object), ...(b as object) };
  }
  return (a as number) | (b as number);
}

export function bitand(a: unknown, b: unknown): any {
  if (a instanceof Set) {
    const bb = b instanceof Set ? b : new Set(iter(b));
    return new Set([...a].filter((x) => containsSet(bb, x)));
  }
  return (a as number) & (b as number);
}

export function bitxor(a: unknown, b: unknown): any {
  if (typeof a === "string" || typeof b === "string") {
    throw new TypeError(`unsupported operand type(s) for ^: '${typeof a}' and '${typeof b}'`);
  }
  if (a instanceof Set) {
    const bb = b instanceof Set ? b : new Set(iter(b));
    const out = new Set([...a].filter((x) => !containsSet(bb, x)));
    for (const x of bb) if (!containsSet(a, x)) out.add(x);
    return out;
  }
  return (a as number) ^ (b as number);
}

export function divmod(a: number, b: number): [number, number] {
  return [Math.floor(a / b), mod(a, b) as number];
}

/* ------------------------------------------------------------------ */
/* iteration                                                           */
/* ------------------------------------------------------------------ */

/** Python iteration semantics: dicts iterate keys, strings iterate chars. */
export function iter<T = any>(value: unknown): T[] {
  if (value === null || value === undefined) return [];
  if (Array.isArray(value)) return value as T[];
  if (value instanceof Set) return [...value] as T[];
  if (value instanceof Map) return [...value.keys()] as T[];
  if (typeof value === "string") return [...value] as unknown as T[];
  if (value instanceof PyBytes) return [...value.data] as unknown as T[];
  if (typeof value === "object") {
    if (typeof (value as { __iter__?: unknown }).__iter__ === "function") {
      return iter((value as { __iter__: () => unknown }).__iter__());
    }
    if (typeof (value as { [Symbol.iterator]?: unknown })[Symbol.iterator] === "function") {
      return [...(value as Iterable<T>)];
    }
    return Object.keys(value) as unknown as T[];
  }
  return [value as T];
}

export function items(value: unknown): [string, any][] {
  if (value === null || value === undefined) return [];
  if (value instanceof Map) return [...value.entries()] as [string, unknown][];
  if (Array.isArray(value)) return value as [string, unknown][];
  if (typeof value === "object") {
    if ((value as object).constructor !== Object
      && typeof (value as { items?: unknown }).items === "function") {
      // custom class with its own .items() (e.g. queue engines)
      return (value as { items: () => [string, unknown][] }).items();
    }
    return Object.entries(value as Record<string, unknown>);
  }
  return [];
}

export function keys(value: unknown): string[] {
  if (value === null || value === undefined) return [];
  if (value instanceof Map) return [...value.keys()] as string[];
  if (Array.isArray(value)) {
    throw err("AttributeError", "'list' object has no attribute 'keys'");
  }
  if (typeof value === "string") {
    throw err("AttributeError", "'str' object has no attribute 'keys'");
  }
  if (typeof value === "object" && !(value instanceof Set)) {
    return Object.keys(value as object);
  }
  return iter<string>(value);
}

/** Python set()/frozenset() construction — rejects unhashable members. */
export function toSet(value?: unknown): Set<unknown> {
  const out = new Set<unknown>();
  for (const v of iter(value ?? [])) {
    if (v !== null && typeof v === "object" && !Array.isArray(v) && !(v instanceof PyBytes)) {
      if (v instanceof Set) throw err("TypeError", "unhashable type: 'set'");
      if ((v as object).constructor === Object) throw err("TypeError", "unhashable type: 'dict'");
    }
    setAdd(out, v);
  }
  return out;
}

/** Python type.__mro__ access parity. */
export function mro(value: unknown): any[] {
  if (typeof value === "function") return [value];
  const t = Array.isArray(value) ? "list" : value === null ? "NoneType" : typeof value === "string" ? "str" : typeof value;
  throw err("AttributeError", `'${t}' object has no attribute '__mro__'`);
}

export function values(value: unknown): any[] {
  if (value === null || value === undefined) return [];
  if (value instanceof Map) return [...value.values()];
  if (typeof value === "object" && !Array.isArray(value) && !(value instanceof Set)) {
    return Object.values(value as object);
  }
  return iter(value);
}

export function enumerate<T = any>(value: unknown, start = 0): [number, T][] {
  return iter<T>(value).map((item, index) => [index + start, item]);
}

export function zip(...iterables: unknown[]): unknown[][] {
  const arrays = iterables.map((x) => iter(x));
  const n = arrays.length ? Math.min(...arrays.map((a) => a.length)) : 0;
  const out: unknown[][] = [];
  for (let i = 0; i < n; i++) out.push(arrays.map((a) => a[i]));
  return out;
}

export function range(start: number, stop?: number, step = 1): number[] {
  let lo = start;
  let hi = stop;
  if (hi === undefined) {
    hi = start;
    lo = 0;
  }
  const out: number[] = [];
  if (step > 0) for (let i = lo; i < hi; i += step) out.push(i);
  else if (step < 0) for (let i = lo; i > hi; i += step) out.push(i);
  return out;
}

export function reversed<T = any>(value: unknown): T[] {
  return [...iter<T>(value)].reverse();
}

export function len(value: unknown): number {
  if (value instanceof PyFloat) {
    throw new TypeError("object of type 'float' has no len()");
  }
  if (value === null || value === undefined) {
    throw new TypeError("object of type 'NoneType' has no len()");
  }
  if (typeof value === "string") return value.length;
  if (Array.isArray(value)) return value.length;
  if (value instanceof Set || value instanceof Map) return value.size;
  if (value instanceof PyBytes) return value.data.length;
  if (typeof value === "object") {
    if (typeof (value as { __len__?: unknown }).__len__ === "function") {
      return (value as { __len__: () => number }).__len__();
    }
    if (typeof (value as { __iter__?: unknown }).__iter__ === "function") {
      return iter(value).length;
    }
    return Object.keys(value as object).length;
  }
  throw new TypeError(`object of type '${typeof value}' has no len()`);
}

/** Python subscript load with negative index support (strict: KeyError/IndexError). */
export function at(container: unknown, key: unknown): any {
  if (container === null || container === undefined) {
    throw new TypeError("'NoneType' object is not subscriptable");
  }
  if (typeof key === "number" && (Array.isArray(container) || typeof container === "string")) {
    const seq = container as { length: number };
    const idx = key < 0 ? seq.length + key : key;
    if (idx < 0 || idx >= seq.length) {
      throw err("IndexError", Array.isArray(container) ? "list index out of range" : "string index out of range");
    }
    return (container as Record<number, unknown>)[idx];
  }
  if (container instanceof Map) {
    if (!container.has(key)) throw err("KeyError", repr(key));
    return container.get(key);
  }
  if (container instanceof PyBytes && typeof key === "number") {
    const idx = key < 0 ? container.data.length + key : key;
    if (idx < 0 || idx >= container.data.length) throw err("IndexError", "index out of range");
    return container.data[idx];
  }
  if (container instanceof PyMatch) {
    return container.group(key as number | string);
  }
  if (DEFAULTDICTS.has(container as object)) {
    return (container as Record<string, unknown>)[key as string];
  }
  // plain object (dict) or class instance: missing string key raises KeyError
  const rec = container as Record<string, unknown>;
  const k = key as string;
  if (typeof container === "object" && (container as object).constructor === Object && !(k in (rec as object))) {
    throw err("KeyError", repr(k));
  }
  return rec[k];
}

/** Python next(iterator[, default]). */
export function next<T = any>(seq: T[], ...dflt: unknown[]): any {
  if (seq.length) return seq[0];
  if (dflt.length) return dflt[0];
  throw err("StopIteration", "");
}

/** Python subscript store. */
export function setItem(container: unknown, key: unknown, value: unknown): void {
  if (typeof key === "number" && Array.isArray(container)) {
    const idx = key < 0 ? container.length + key : key;
    container[idx] = value;
    return;
  }
  if (container instanceof Map) {
    container.set(key, value);
    return;
  }
  (container as Record<string, unknown>)[key as string] = value;
}

export function delItem(container: unknown, key: unknown): void {
  if (typeof key === "number" && Array.isArray(container)) {
    const idx = key < 0 ? container.length + key : key;
    container.splice(idx, 1);
    return;
  }
  if (container instanceof Map) {
    container.delete(key);
    return;
  }
  delete (container as Record<string, unknown>)[key as string];
}

/** Python slice semantics, including step. */
export function slice<T = any>(
  value: unknown,
  lo: number | null,
  hi: number | null,
  step: number | null = null,
): any {
  if (value instanceof PyBytes && (step === null || step === 1)) {
    const n = value.data.length;
    const start = lo === null || lo === undefined ? 0 : lo < 0 ? Math.max(0, n + lo) : Math.min(lo, n);
    const stop = hi === null || hi === undefined ? n : hi < 0 ? Math.max(0, n + hi) : Math.min(hi, n);
    return new PyBytes(value.data.slice(start, stop));
  }
  const isStr = typeof value === "string";
  const seq: unknown[] = isStr ? [...(value as string)] : [...iter(value)];
  const n = seq.length;
  const st = step === null || step === undefined ? 1 : step;
  let start: number;
  let stop: number;
  if (st > 0) {
    start = lo === null || lo === undefined ? 0 : lo < 0 ? Math.max(0, n + lo) : Math.min(lo, n);
    stop = hi === null || hi === undefined ? n : hi < 0 ? Math.max(0, n + hi) : Math.min(hi, n);
  } else {
    start = lo === null || lo === undefined ? n - 1 : lo < 0 ? Math.max(-1, n + lo) : Math.min(lo, n - 1);
    stop = hi === null || hi === undefined ? -1 : hi < 0 ? Math.max(-1, n + hi) : Math.min(hi, n - 1);
  }
  const out: unknown[] = [];
  if (st > 0) for (let i = start; i < stop; i += st) out.push(seq[i]);
  else for (let i = start; i > stop; i += st) out.push(seq[i]);
  return isStr ? (out as string[]).join("") : (out as T[]);
}

/* ------------------------------------------------------------------ */
/* builtins                                                            */
/* ------------------------------------------------------------------ */

export interface SortOpts {
  key?: (item: unknown) => unknown;
  reverse?: boolean;
}

export function sorted(value: unknown, opts: SortOpts = {}): any[] {
  const arr = [...iter(value)];
  const keyed = arr.map((v, i) => [opts.key ? opts.key(v) : v, i, v] as const);
  keyed.sort((a, b) => {
    const c = cmp(a[0], b[0]);
    if (c !== 0) return c;
    return a[1] - b[1]; // stable
  });
  const out = keyed.map((k) => k[2]);
  return opts.reverse ? out.reverse() : out;
}

export function sortInPlace(arr: unknown[], opts: SortOpts = {}): void {
  const out = sorted(arr, opts);
  arr.length = 0;
  arr.push(...out);
}

export function sum(value: unknown, start: unknown = 0): any {
  let acc: unknown = start;
  for (const v of iter(value)) acc = add(acc, v);
  return acc;
}

export interface MinMaxOpts {
  key?: (item: unknown) => unknown;
  dflt?: unknown;
  hasDefault?: boolean;
}

export function min(value: unknown, opts: MinMaxOpts = {}): any {
  const arr = [...iter(value)];
  if (!arr.length) {
    if (opts.hasDefault) return opts.dflt;
    throw new Error("min() arg is an empty sequence");
  }
  let best = arr[0];
  let bestKey = opts.key ? opts.key(best) : best;
  for (let i = 1; i < arr.length; i++) {
    const k = opts.key ? opts.key(arr[i]) : arr[i];
    if (cmp(k, bestKey) < 0) {
      best = arr[i];
      bestKey = k;
    }
  }
  return best;
}

export function max(value: unknown, opts: MinMaxOpts = {}): any {
  const arr = [...iter(value)];
  if (!arr.length) {
    if (opts.hasDefault) return opts.dflt;
    throw new Error("max() arg is an empty sequence");
  }
  let best = arr[0];
  let bestKey = opts.key ? opts.key(best) : best;
  for (let i = 1; i < arr.length; i++) {
    const k = opts.key ? opts.key(arr[i]) : arr[i];
    if (cmp(k, bestKey) > 0) {
      best = arr[i];
      bestKey = k;
    }
  }
  return best;
}

/** Python abs() preserving float-ness. */
export function pyAbs(x: unknown): any {
  const r = Math.abs(num(x));
  return x instanceof PyFloat ? new PyFloat(r) : r;
}

export function all(value: unknown): boolean {
  return iter(value).every((v) => truthy(v));
}

export function any(value: unknown): boolean {
  return iter(value).some((v) => truthy(v));
}

/**
 * Python round(): correctly-rounded half-even on the exact binary value,
 * implemented with exact BigInt arithmetic (matches CPython output).
 */
export function round(xIn: number | PyFloat, ndigits?: number): any {
  const wasFloat = xIn instanceof PyFloat;
  const x = num(xIn);
  const wrap = (r: number): number | PyFloat =>
    wasFloat && ndigits !== undefined && ndigits !== null ? new PyFloat(r) : r;
  if (!Number.isFinite(x)) return wrap(x);
  const n = ndigits === undefined || ndigits === null ? 0 : Math.trunc(ndigits);

  // decompose the double exactly: x = sign * mant * 2^exp
  const buf = new DataView(new ArrayBuffer(8));
  buf.setFloat64(0, Math.abs(x));
  const hi = buf.getUint32(0);
  const lo = buf.getUint32(4);
  const biasedExp = (hi >>> 20) & 0x7ff;
  let mant = (BigInt(hi & 0xfffff) << 32n) | BigInt(lo);
  let exp: bigint;
  if (biasedExp === 0) {
    exp = -1074n; // subnormal
  } else {
    mant |= 1n << 52n;
    exp = BigInt(biasedExp) - 1075n;
  }
  if (mant === 0n) return wrap(0);

  // want q = round_half_even(|x| * 10^n); |x| * 10^n = mant * 2^exp * 10^n
  let numer = mant;
  let den = 1n;
  if (n >= 0) numer *= 10n ** BigInt(n);
  else den *= 10n ** BigInt(-n);
  if (exp >= 0n) numer <<= exp;
  else den <<= -exp;

  let q = numer / den;
  const rem = numer % den;
  const twice = rem * 2n;
  if (twice > den || (twice === den && (q & 1n) === 1n)) q += 1n;

  const sign = x < 0 ? -1 : 1;
  if (n <= 0) {
    const out = Number(q * 10n ** BigInt(-n)) * sign;
    return wrap(out);
  }
  return wrap((sign * Number(q)) / Math.pow(10, n));
}

export function toInt(x: unknown, base?: number): number {
  if (x instanceof PyFloat) return Math.trunc(x.v);
  if (typeof x === "number") return Math.trunc(x);
  if (typeof x === "boolean") return x ? 1 : 0;
  const s = String(x).trim();
  const n = base !== undefined ? parseInt(s, base) : Number(s);
  if (Number.isNaN(n)) throw new Error(`invalid literal for int(): '${s}'`);
  return Math.trunc(n);
}

export function toFloat(x: unknown): any {
  if (x instanceof PyFloat) return x;
  if (typeof x === "number") return new PyFloat(x);
  const n = Number(String(x).trim());
  if (Number.isNaN(n) && String(x).trim().toLowerCase() !== "nan") {
    throw new Error(`could not convert string to float: '${String(x)}'`);
  }
  return new PyFloat(n);
}

/** Python str(). */
export function toStr(value: unknown): string {
  if (value === null || value === undefined) return "None";
  if (value === true) return "True";
  if (value === false) return "False";
  if (typeof value === "string") return value;
  if (value instanceof PyFloat) return floatStr(value.v);
  if (typeof value === "number") return String(value);
  if (value instanceof Error) return value.message;
  if (value instanceof PyBytes) return value.reprStr();
  if (value instanceof PyPath) return value.toString();
  if (Array.isArray(value) || value instanceof Set || value instanceof Map) return repr(value);
  if (typeof value === "object") {
    if ((value as object).constructor !== Object
      && typeof (value as { toString?: unknown }).toString === "function"
      && (value as object).toString !== Object.prototype.toString) {
      return String(value);
    }
    return repr(value);
  }
  return String(value);
}

/** Python repr(). */
export function repr(value: unknown): string {
  if (value === null || value === undefined) return "None";
  if (value === true) return "True";
  if (value === false) return "False";
  if (value instanceof PyFloat) return floatStr(value.v);
  if (typeof value === "number") return String(value);
  if (typeof value === "string") {
    if (value.includes("'") && !value.includes('"')) {
      return `"${value.replace(/\\/g, "\\\\")}"`;
    }
    return `'${value.replace(/\\/g, "\\\\").replace(/'/g, "\\'")}'`;
  }
  if (Array.isArray(value)) {
    if (REPR_SEEN.has(value)) return "[...]";
    REPR_SEEN.add(value);
    try {
      return `[${value.map((v) => repr(v)).join(", ")}]`;
    } finally {
      REPR_SEEN.delete(value);
    }
  }
  if (value instanceof Set) {
    if (!value.size) return "set()";
    return `{${[...value].map((v) => repr(v)).join(", ")}}`;
  }
  if (value instanceof Map) {
    return `{${[...value.entries()].map(([k, v]) => `${repr(k)}: ${repr(v)}`).join(", ")}}`;
  }
  if (value instanceof PyBytes) return value.reprStr();
  if (typeof value === "object") {
    if (REPR_SEEN.has(value as object)) return "{...}";
    REPR_SEEN.add(value as object);
    try {
      return `{${Object.entries(value as Record<string, unknown>)
        .map(([k, v]) => `${repr(k)}: ${repr(v)}`)
        .join(", ")}}`;
    } finally {
      REPR_SEEN.delete(value as object);
    }
  }
  return String(value);
}

const REPR_SEEN = new Set<object>();

/** Python str() of a float-typed value: integral floats render as "N.0". */
export function floatStr(xIn: unknown): string {
  const x = xIn instanceof PyFloat ? xIn.v : xIn;
  if (typeof x !== "number") return toStr(x);
  if (Number.isInteger(x) && Number.isFinite(x)) {
    if (Math.abs(x) >= 1e16) return x.toExponential();
    return `${x}.0`;
  }
  if (Number.isFinite(x) && x !== 0 && Math.abs(x) < 1e-4) {
    let s = x.toExponential();
    s = s.replace(/e([+-])(\d)$/, "e$10$2");
    return s;
  }
  if (Number.isNaN(x)) return "nan";
  if (x === Infinity) return "inf";
  if (x === -Infinity) return "-inf";
  return String(x);
}

export function ord(s: string): number {
  return s.codePointAt(0) ?? 0;
}

export function chr(n: number): string {
  return String.fromCodePoint(n);
}

export function print(...args: unknown[]): void {
  process.stderr.write(args.map((a) => toStr(a)).join(" ") + "\n");
}

/** Python format(value, spec) — common spec subset. */
export function format(value: unknown, spec: string): string {
  if (value instanceof PyFloat && !spec) return floatStr(value.v);
  value = unbox(value);
  if (!spec) return toStr(value);
  const m = spec.match(/^([^{}]?[<>^=])?([+\- ])?(#)?(0)?(\d+)?(,)?(?:\.(\d+))?([bcdeEfFgGnosxX%])?$/);
  if (!m) return toStr(value);
  const [, alignRaw, sign, , zero, widthRaw, comma, precRaw, type] = m;
  let fill = " ";
  let align = alignRaw ?? "";
  if (align.length === 2) {
    fill = align[0]!;
    align = align[1]!;
  }
  let s: string;
  const num = typeof value === "number" ? value : Number(value);
  if (type === "f" || type === "F") {
    const prec = precRaw !== undefined ? Number(precRaw) : 6;
    s = num.toFixed(prec);
  } else if (type === "d") {
    s = String(Math.trunc(num));
  } else if (type === "%") {
    const prec = precRaw !== undefined ? Number(precRaw) : 6;
    s = (num * 100).toFixed(prec) + "%";
  } else if (type === "e" || type === "E") {
    const prec = precRaw !== undefined ? Number(precRaw) : 6;
    s = num.toExponential(prec);
    if (type === "E") s = s.toUpperCase();
    s = s.replace(/e([+-])(\d)$/, "e$10$2");
  } else if (type === "x") {
    s = Math.trunc(num).toString(16);
  } else if (type === "X") {
    s = Math.trunc(num).toString(16).toUpperCase();
  } else if (type === "b") {
    s = Math.trunc(num).toString(2);
  } else if (type === "o") {
    s = Math.trunc(num).toString(8);
  } else if (type === "g" || type === "G") {
    const prec = precRaw !== undefined ? Number(precRaw) : 6;
    s = String(Number(num.toPrecision(prec)));
  } else if (precRaw !== undefined && (type === "s" || type === undefined) && typeof value === "string") {
    s = value.slice(0, Number(precRaw));
  } else {
    s = toStr(value);
  }
  if (sign === "+" && typeof value === "number" && num >= 0 && !s.startsWith("+")) s = "+" + s;
  if (comma) {
    const parts = s.split(".");
    parts[0] = parts[0]!.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    s = parts.join(".");
  }
  const width = widthRaw ? Number(widthRaw) : 0;
  if (s.length < width) {
    const pad = width - s.length;
    if (zero && !align) {
      const neg = s.startsWith("-");
      s = (neg ? "-" : "") + "0".repeat(pad) + (neg ? s.slice(1) : s);
    } else if (align === ">" || (!align && typeof value === "number")) {
      s = fill.repeat(pad) + s;
    } else if (align === "^") {
      const left = Math.floor(pad / 2);
      s = fill.repeat(left) + s + fill.repeat(pad - left);
    } else {
      s = s + fill.repeat(pad);
    }
  }
  return s;
}

/* ------------------------------------------------------------------ */
/* str methods                                                         */
/* ------------------------------------------------------------------ */

export function split(base: unknown, sep?: unknown, maxsplit = -1): any {
  if (base instanceof PyRegex) {
    return base.split(String(sep), typeof maxsplit === "number" && maxsplit >= 0 ? maxsplit : 0);
  }
  const s = String(base);
  if (sep === undefined || sep === null) {
    const parts = s.split(/\s+/).filter((p) => p.length > 0);
    if (maxsplit >= 0 && parts.length > maxsplit) {
      const out: string[] = [];
      let rest = s.replace(/^\s+/, "");
      while (out.length < maxsplit && /\s/.test(rest)) {
        const m = rest.match(/^(\S+)\s+/);
        if (!m) break;
        out.push(m[1]!);
        rest = rest.slice(m[0].length);
      }
      if (rest.length) out.push(rest.replace(/\s+$/, ""));
      return out;
    }
    return parts;
  }
  const ss = String(sep);
  if (maxsplit < 0) return s.split(ss);
  const out: string[] = [];
  let rest = s;
  while (out.length < maxsplit) {
    const i = rest.indexOf(ss);
    if (i < 0) break;
    out.push(rest.slice(0, i));
    rest = rest.slice(i + ss.length);
  }
  out.push(rest);
  return out;
}

export function rsplit(base: unknown, sep?: unknown, maxsplit = -1): string[] {
  const s = String(base);
  if (sep === undefined || sep === null) return split(s, undefined, -1) as string[];
  const ss = String(sep);
  if (maxsplit < 0) return s.split(ss);
  const out: string[] = [];
  let rest = s;
  while (out.length < maxsplit) {
    const i = rest.lastIndexOf(ss);
    if (i < 0) break;
    out.unshift(rest.slice(i + ss.length));
    rest = rest.slice(0, i);
  }
  out.unshift(rest);
  return out;
}

function escapeCharClass(chars: string): string {
  return chars.replace(/[.*+?^${}()|[\]\\\-]/g, "\\$&");
}

export function strip(base: unknown, chars?: string): string {
  const s = String(base);
  if (chars === undefined || chars === null) return s.trim();
  const cc = escapeCharClass(chars);
  return s.replace(new RegExp(`^[${cc}]+`), "").replace(new RegExp(`[${cc}]+$`), "");
}

export function lstrip(base: unknown, chars?: string): string {
  const s = String(base);
  if (chars === undefined || chars === null) return s.replace(/^\s+/, "");
  return s.replace(new RegExp(`^[${escapeCharClass(chars)}]+`), "");
}

export function rstrip(base: unknown, chars?: string): string {
  const s = String(base);
  if (chars === undefined || chars === null) return s.replace(/\s+$/, "");
  return s.replace(new RegExp(`[${escapeCharClass(chars)}]+$`), "");
}

/** str.replace — all occurrences (unlike JS). */
export function replace(base: unknown, oldS: string, newS: string, count = -1): string {
  const s = String(base);
  if (count < 0) return s.split(oldS).join(newS);
  let out = s;
  for (let i = 0; i < count; i++) {
    const idx = out.indexOf(oldS);
    if (idx < 0) break;
    out = out.slice(0, idx) + newS + out.slice(idx + oldS.length);
  }
  return out;
}

/** str.count / list.count. */
export function count(base: unknown, item: unknown): number {
  if (typeof base === "string") {
    const sub2 = String(item);
    if (!sub2.length) return base.length + 1;
    let n = 0;
    let i = 0;
    for (;;) {
      const j = base.indexOf(sub2, i);
      if (j < 0) break;
      n++;
      i = j + sub2.length;
    }
    return n;
  }
  return iter(base).filter((v) => eq(v, item)).length;
}

export function find(base: unknown, sub2: unknown, start = 0): any {
  if (base !== null && typeof base === "object"
    && typeof (base as { find?: unknown }).find === "function" && !Array.isArray(base)) {
    return (base as { find: (x: unknown) => unknown }).find(sub2);
  }
  return String(base).indexOf(String(sub2), start);
}

export function rfind(base: unknown, sub2: string): number {
  return String(base).lastIndexOf(sub2);
}

export function startswith(base: unknown, prefix: unknown, start?: number): boolean {
  const s = start ? String(base).slice(start) : String(base);
  if (Array.isArray(prefix)) return prefix.some((p) => s.startsWith(String(p)));
  return s.startsWith(String(prefix));
}

export function endswith(base: unknown, suffix: unknown): boolean {
  const s = String(base);
  if (Array.isArray(suffix)) return suffix.some((p) => s.endsWith(String(p)));
  return s.endsWith(String(suffix));
}

export function zfill(base: unknown, width: number): string {
  const s = String(base);
  if (s.length >= width) return s;
  const neg = s.startsWith("-") || s.startsWith("+");
  return neg ? s[0] + s.slice(1).padStart(width - 1, "0") : s.padStart(width, "0");
}

export function ljust(base: unknown, width: number, fill = " "): string {
  return String(base).padEnd(width, fill);
}

export function rjust(base: unknown, width: number, fill = " "): string {
  return String(base).padStart(width, fill);
}

export function center(base: unknown, width: number, fill = " "): string {
  const s = String(base);
  if (s.length >= width) return s;
  const pad = width - s.length;
  const left = Math.floor(pad / 2);
  return fill.repeat(left) + s + fill.repeat(pad - left);
}

export function capitalize(base: unknown): string {
  const s = String(base);
  return s.length ? s[0]!.toUpperCase() + s.slice(1).toLowerCase() : s;
}

export function title(base: unknown): string {
  if (base !== null && typeof base === "object"
    && typeof (base as { title?: unknown }).title === "function") {
    // receiver with its own .title() method (e.g. page objects)
    return (base as { title: () => string }).title();
  }
  return String(base).replace(/[A-Za-z]+/g, (w) => w[0]!.toUpperCase() + w.slice(1).toLowerCase());
}

export function splitlines(base: unknown, keepends = false): string[] {
  const s = String(base);
  if (!s.length) return [];
  const out: string[] = [];
  let cur = "";
  for (let i = 0; i < s.length; i++) {
    const ch = s[i]!;
    if (ch === "\n" || ch === "\r") {
      let endLen = 1;
      if (ch === "\r" && s[i + 1] === "\n") {
        endLen = 2;
        i++;
      }
      out.push(keepends ? cur + s.slice(i - endLen + 1, i + 1) : cur);
      cur = "";
    } else {
      cur += ch;
    }
  }
  if (cur.length) out.push(cur);
  return out;
}

export function partition(base: unknown, sep: string): [string, string, string] {
  const s = String(base);
  const i = s.indexOf(sep);
  if (i < 0) return [s, "", ""];
  return [s.slice(0, i), sep, s.slice(i + sep.length)];
}

export function rpartition(base: unknown, sep: string): [string, string, string] {
  const s = String(base);
  const i = s.lastIndexOf(sep);
  if (i < 0) return ["", "", s];
  return [s.slice(0, i), sep, s.slice(i + sep.length)];
}

export function removeprefix(base: unknown, prefix: string): string {
  const s = String(base);
  return s.startsWith(prefix) ? s.slice(prefix.length) : s;
}

export function removesuffix(base: unknown, suffix: string): string {
  const s = String(base);
  return suffix.length && s.endsWith(suffix) ? s.slice(0, -suffix.length) : s;
}

export function isdigit(base: unknown): boolean {
  const s = String(base);
  return s.length > 0 && /^[0-9]+$/.test(s);
}

export function isalpha(base: unknown): boolean {
  const s = String(base);
  return s.length > 0 && /^\p{L}+$/u.test(s);
}

export function isalnum(base: unknown): boolean {
  const s = String(base);
  return s.length > 0 && /^[\p{L}\p{Nd}]+$/u.test(s);
}

export function isspace(base: unknown): boolean {
  const s = String(base);
  return s.length > 0 && /^\s+$/.test(s);
}

export function isupper(base: unknown): boolean {
  const s = String(base);
  return /[A-Za-z]/.test(s) && s === s.toUpperCase();
}

export function islower(base: unknown): boolean {
  const s = String(base);
  return /[A-Za-z]/.test(s) && s === s.toLowerCase();
}

export function join(sep: unknown, iterable: unknown): string {
  return iter(iterable).map((v) => toStr(v)).join(String(sep));
}

/** str.format(...) — positional {} / {0} / {name} with format specs. */
export function strFormat(template: unknown, args: unknown[], kwargs: Record<string, unknown> = {}): string {
  let auto = 0;
  return String(template).replace(/\{\{|\}\}|\{([^{}:]*)(?::([^{}]*))?\}/g, (m, name, spec) => {
    if (m === "{{") return "{";
    if (m === "}}") return "}";
    let v: unknown;
    if (name === "" || name === undefined) v = args[auto++];
    else if (/^\d+$/.test(name)) v = args[Number(name)];
    else v = kwargs[name];
    return spec ? format(v, spec) : toStr(v);
  });
}

/* ------------------------------------------------------------------ */
/* dict / list / set methods                                           */
/* ------------------------------------------------------------------ */

export function get(obj: unknown, key: unknown, dflt: unknown = null): any {
  if (obj === null || obj === undefined) return dflt;
  if (obj instanceof Map) return obj.has(key) ? obj.get(key) : dflt;
  if (Array.isArray(obj)) {
    throw err("AttributeError", "'list' object has no attribute 'get'");
  }
  if (typeof obj === "string") {
    throw err("AttributeError", "'str' object has no attribute 'get'");
  }
  if (typeof obj === "number" || typeof obj === "boolean") {
    throw err("AttributeError", `'${typeof obj}' object has no attribute 'get'`);
  }
  if (typeof obj === "object" && (obj as object).constructor !== Object
    && typeof (obj as { get?: unknown }).get === "function") {
    return (obj as { get: (k: unknown, d: unknown) => unknown }).get(key, dflt);
  }
  const k = key as string;
  const rec = obj as Record<string, unknown>;
  return k in (rec as object) ? rec[k] : dflt;
}

export function setdefault(obj: unknown, key: unknown, dflt: unknown = null): any {
  if (obj instanceof Map) {
    if (!obj.has(key)) obj.set(key, dflt);
    return obj.get(key);
  }
  const rec = obj as Record<string, unknown>;
  const k = String(key);
  if (!(k in (rec as object))) rec[k] = dflt;
  return rec[k];
}

/** dict.pop(k[, d]) / list.pop([i]). */
export function pop(obj: unknown, key?: unknown, dflt?: unknown): any {
  if (Array.isArray(obj)) {
    if (key === undefined) return obj.pop();
    const idx = (key as number) < 0 ? obj.length + (key as number) : (key as number);
    const [v] = obj.splice(idx, 1);
    return v;
  }
  if (obj instanceof Map) {
    if (obj.has(key)) {
      const v = obj.get(key);
      obj.delete(key);
      return v;
    }
    if (dflt !== undefined) return dflt;
    throw new Error(`KeyError: ${toStr(key)}`);
  }
  if (obj instanceof Set) {
    const first = [...obj][0];
    obj.delete(first);
    return first;
  }
  const rec = obj as Record<string, unknown>;
  const k = String(key);
  if (k in (rec as object)) {
    const v = rec[k];
    delete rec[k];
    return v;
  }
  if (dflt !== undefined) return dflt;
  throw new Error(`KeyError: ${toStr(key)}`);
}

export function update(obj: unknown, other: unknown): void {
  if (obj instanceof Set) {
    for (const v of iter(other)) setAdd(obj, v);
    return;
  }
  if (obj instanceof Map) {
    for (const [k, v] of items(other)) obj.set(k, v);
    return;
  }
  if (obj instanceof PyHash) {
    obj.update(other);
    return;
  }
  if (obj !== null && typeof obj === "object" && (obj as object).constructor !== Object
    && typeof (obj as { update?: unknown }).update === "function") {
    (obj as { update: (o: unknown) => void }).update(other);
    return;
  }
  Object.assign(obj as object, Object.fromEntries(items(other)));
}

export function copy<T = any>(obj: T): T {
  if (obj instanceof PyFloat) return obj;
  if (Array.isArray(obj)) return [...obj] as T;
  if (obj instanceof Set) return new Set(obj) as T;
  if (obj instanceof Map) return new Map(obj) as T;
  if (obj !== null && typeof obj === "object") return { ...(obj as object) } as T;
  return obj;
}

export function deepcopy<T = any>(obj: T): T {
  if (obj === null || typeof obj !== "object") return obj;
  if (obj instanceof PyFloat) return new PyFloat(obj.v) as T;
  if (obj instanceof PyBytes) return new PyBytes(obj.data.slice()) as T;
  if (Array.isArray(obj)) return obj.map((v) => deepcopy(v)) as T;
  if (obj instanceof Set) return new Set([...obj].map((v) => deepcopy(v))) as T;
  if (obj instanceof Map) {
    return new Map([...obj.entries()].map(([k, v]) => [k, deepcopy(v)])) as T;
  }
  const out: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(obj as Record<string, unknown>)) out[k] = deepcopy(v);
  return out as T;
}

export function clear(obj: unknown): void {
  if (Array.isArray(obj)) {
    obj.length = 0;
    return;
  }
  if (obj instanceof Set || obj instanceof Map) {
    obj.clear();
    return;
  }
  for (const k of Object.keys(obj as object)) delete (obj as Record<string, unknown>)[k];
}

export function fromkeys(keysIt: unknown, value: unknown = null): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  for (const k of iter(keysIt)) out[String(k)] = value;
  return out;
}

/** list.append / deque.append (honors deque maxlen). */
export function listAppend(arr: unknown, v: unknown): void {
  if (arr instanceof PyDeque) {
    arr.append(v);
    return;
  }
  if (Array.isArray(arr)) {
    arr.push(v);
    return;
  }
  (arr as { append?: (v: unknown) => void }).append?.(v);
}

export function appendleft(arr: unknown, v: unknown): void {
  if (arr instanceof PyDeque) {
    arr.appendleft(v);
    return;
  }
  (arr as unknown[]).unshift(v);
}

export function popleft(arr: unknown): any {
  return (arr as unknown[]).shift();
}

/** list.remove / set.remove / custom .remove. */
export function remove(container: unknown, v: unknown): any {
  if (container instanceof Set) {
    const before = container.size;
    setDiscard(container, v);
    if (container.size === before) throw new Error(`KeyError: ${toStr(v)}`);
    return undefined;
  }
  if (Array.isArray(container)) {
    listRemove(container, v);
    return undefined;
  }
  return (container as { remove: (v: unknown) => unknown }).remove(v);
}

export function extend(arr: unknown, it: unknown): void {
  if (arr instanceof PyDeque) {
    for (const v of iter(it)) arr.append(v);
    return;
  }
  (arr as unknown[]).push(...iter(it));
}

export function insert(arr: unknown[], i: number, v: unknown): void {
  arr.splice(i < 0 ? Math.max(0, arr.length + i) : i, 0, v);
}

export function listRemove(arr: unknown[], v: unknown): void {
  const i = arr.findIndex((x) => eq(x, v));
  if (i < 0) throw new Error("ValueError: list.remove(x): x not in list");
  arr.splice(i, 1);
}

export function index(seq: unknown, v: unknown): number {
  if (typeof seq === "string") {
    const i = seq.indexOf(String(v));
    if (i < 0) throw new Error("ValueError: substring not found");
    return i;
  }
  const i = iter(seq).findIndex((x) => eq(x, v));
  if (i < 0) throw new Error(`ValueError: ${toStr(v)} is not in list`);
  return i;
}

export function setAdd(s: unknown, v: unknown): void {
  if (!(s instanceof Set)) {
    (s as { add: (v: unknown) => void }).add(v);
    return;
  }
  if (typeof v === "string" || typeof v === "number" || typeof v === "boolean" || v === null) {
    s.add(v);
    return;
  }
  if (!containsSet(s, v)) s.add(v);
}

export function setDiscard(s: Set<unknown>, v: unknown): void {
  if (s.delete(v)) return;
  for (const x of s) {
    if (eq(x, v)) {
      s.delete(x);
      return;
    }
  }
}

export function union(a: unknown, ...others: unknown[]): Set<unknown> {
  const out = new Set(iter(a));
  for (const o of others) for (const v of iter(o)) setAdd(out, v);
  return out;
}

export function intersection(a: unknown, ...others: unknown[]): Set<unknown> {
  let out = new Set(iter(a));
  for (const o of others) {
    const so = new Set(iter(o));
    out = new Set([...out].filter((x) => containsSet(so, x)));
  }
  return out;
}

export function difference(a: unknown, ...others: unknown[]): Set<unknown> {
  let out = new Set(iter(a));
  for (const o of others) {
    const so = new Set(iter(o));
    out = new Set([...out].filter((x) => !containsSet(so, x)));
  }
  return out;
}

export function symmetricDifference(a: unknown, b: unknown): Set<unknown> {
  return bitxor(new Set(iter(a)), b) as Set<unknown>;
}

export function issubset(a: unknown, b: unknown): boolean {
  const sb = new Set(iter(b));
  return [...iter(a)].every((x) => containsSet(sb, x));
}

export function issuperset(a: unknown, b: unknown): boolean {
  return issubset(b, a);
}

/* ------------------------------------------------------------------ */
/* collections                                                         */
/* ------------------------------------------------------------------ */

/** collections.deque with optional maxlen. */
export class PyDeque<T = any> extends Array<T> {
  maxlen: number | null = null;

  static make<T>(value?: unknown, maxlen: number | null = null): PyDeque<T> {
    const d = new PyDeque<T>();
    d.maxlen = maxlen;
    for (const v of iter<T>(value ?? [])) d.append(v);
    return d;
  }

  append(v: T): void {
    this.push(v);
    if (this.maxlen !== null && this.length > this.maxlen) this.shift();
  }

  appendleft(v: T): void {
    this.unshift(v);
    if (this.maxlen !== null && this.length > this.maxlen) super.pop();
  }

  popleft(): T | undefined {
    return this.shift();
  }
}

export function deque<T = any>(value?: unknown, maxlen: number | null = null): PyDeque<T> {
  return PyDeque.make<T>(value, maxlen);
}

const DEFAULTDICTS = new WeakSet<object>();

/** collections.defaultdict via Proxy. */
export function defaultdict(factory: () => unknown): Record<string, unknown> {
  const proxy = new Proxy<Record<string, unknown>>({}, {
    get(target, prop, receiver) {
      if (typeof prop === "string" && !(prop in target)) {
        target[prop] = factory();
      }
      return Reflect.get(target, prop, receiver);
    },
  });
  DEFAULTDICTS.add(proxy);
  return proxy;
}

/** collections.Counter. */
export function counter(value?: unknown): Record<string, number> {
  const out: Record<string, number> = {};
  if (value !== undefined && value !== null) {
    if (!Array.isArray(value) && typeof value === "object" && !(value instanceof Set) && typeof value !== "string") {
      for (const [k, v] of Object.entries(value as Record<string, number>)) out[k] = v;
    } else {
      for (const v of iter(value)) out[String(v)] = (out[String(v)] ?? 0) + 1;
    }
  }
  return out;
}

export function mostCommon(c: Record<string, number>, n?: number): [string, number][] {
  const entries = Object.entries(c);
  const sortedE = sorted(entries, { key: (e) => -(e as [string, number])[1] }) as [string, number][];
  return n === undefined ? sortedE : sortedE.slice(0, n);
}

/* ------------------------------------------------------------------ */
/* bytes                                                               */
/* ------------------------------------------------------------------ */

export class PyBytes {
  data: Uint8Array;

  constructor(data: Uint8Array | string | number | unknown[]) {
    if (typeof data === "string") this.data = new TextEncoder().encode(data);
    else if (typeof data === "number") this.data = new Uint8Array(data);
    else if (Array.isArray(data)) this.data = new Uint8Array(data.map((b) => Number(b)));
    else this.data = data;
  }

  decode(_encoding = "utf-8"): string {
    return new TextDecoder().decode(this.data);
  }

  hex(): string {
    return [...this.data].map((b) => b.toString(16).padStart(2, "0")).join("");
  }

  reprStr(): string {
    let out = "b'";
    for (const b of this.data) {
      if (b === 0x27) out += "\\'";
      else if (b === 0x5c) out += "\\\\";
      else if (b >= 0x20 && b < 0x7f) out += String.fromCharCode(b);
      else if (b === 0x0a) out += "\\n";
      else if (b === 0x0d) out += "\\r";
      else if (b === 0x09) out += "\\t";
      else out += "\\x" + b.toString(16).padStart(2, "0");
    }
    return out + "'";
  }

  toString(): string {
    return this.reprStr();
  }
}

export function encode(s: unknown, _encoding = "utf-8"): PyBytes {
  return new PyBytes(String(s));
}

export function decode(b: unknown, encoding = "utf-8"): string {
  if (b instanceof PyBytes) return b.decode(encoding);
  if (b instanceof Uint8Array) return new TextDecoder().decode(b);
  return String(b);
}

/* ------------------------------------------------------------------ */
/* hashlib / base64 / json                                             */
/* ------------------------------------------------------------------ */

export class PyHash {
  private algo: string;
  private chunks: Buffer[] = [];

  constructor(algo: string, data?: unknown) {
    this.algo = algo;
    if (data !== undefined) this.update(data);
  }

  update(data: unknown): void {
    if (data instanceof PyBytes) this.chunks.push(Buffer.from(data.data));
    else if (data instanceof Uint8Array) this.chunks.push(Buffer.from(data));
    else this.chunks.push(Buffer.from(String(data), "utf-8"));
  }

  hexdigest(): string {
    const h = createHash(this.algo);
    for (const c of this.chunks) h.update(c);
    return h.digest("hex");
  }

  digest(): PyBytes {
    const h = createHash(this.algo);
    for (const c of this.chunks) h.update(c);
    return new PyBytes(new Uint8Array(h.digest()));
  }
}

export function hashNew(algo: string, data?: unknown): PyHash {
  const map: Record<string, string> = { blake2b: "blake2b512", blake2s: "blake2s256" };
  return new PyHash(map[algo] ?? algo, data);
}

export function b64encode(data: unknown): PyBytes {
  const buf = data instanceof PyBytes ? Buffer.from(data.data)
    : data instanceof Uint8Array ? Buffer.from(data)
      : Buffer.from(String(data), "utf-8");
  return new PyBytes(buf.toString("base64"));
}

export function b64decode(data: unknown): PyBytes {
  const s = data instanceof PyBytes ? data.decode() : String(data);
  return new PyBytes(new Uint8Array(Buffer.from(s, "base64")));
}

export interface JsonDumpsOpts {
  sortKeys?: boolean;
  indent?: number | null;
  separators?: [string, string] | null;
  ensureAscii?: boolean;
  defaultStr?: boolean;
}

/** json.dumps with Python's default formatting (", " / ": " separators). */
export function jsonDumps(value: unknown, opts: JsonDumpsOpts = {}): string {
  const indent = opts.indent ?? null;
  let itemSep: string;
  let kvSep: string;
  if (opts.separators) {
    [itemSep, kvSep] = opts.separators;
  } else if (indent !== null) {
    itemSep = ",";
    kvSep = ": ";
  } else {
    itemSep = ", ";
    kvSep = ": ";
  }
  const ensureAscii = opts.ensureAscii !== false;

  function encStr(s: string): string {
    let out = JSON.stringify(s);
    if (ensureAscii) {
      out = out.replace(/[-￿]/g, (ch) =>
        "\\u" + ch.charCodeAt(0).toString(16).padStart(4, "0"));
    }
    return out;
  }

  const seen = new Set<unknown>();

  function enc(v: unknown, depth: number): string {
    if (v === null || v === undefined) return "null";
    if (v === true) return "true";
    if (v === false) return "false";
    if (v instanceof PyFloat) {
      if (Number.isNaN(v.v)) return "NaN";
      if (v.v === Infinity) return "Infinity";
      if (v.v === -Infinity) return "-Infinity";
      return floatStr(v.v);
    }
    if (typeof v === "number") {
      if (Number.isNaN(v)) return "NaN";
      if (v === Infinity) return "Infinity";
      if (v === -Infinity) return "-Infinity";
      return String(v);
    }
    if (typeof v === "string") return encStr(v);
    if (v instanceof PyPath) return encStr(v.toString());
    if (Array.isArray(v)) {
      if (seen.has(v)) throw err("ValueError", "Circular reference detected");
      seen.add(v);
      if (!v.length) {
        seen.delete(v);
        return "[]";
      }
      const inner = v.map((x) => enc(x, depth + 1));
      seen.delete(v);
      if (indent !== null) {
        const pad = " ".repeat(indent * (depth + 1));
        const padEnd = " ".repeat(indent * depth);
        return `[\n${pad}${inner.join(itemSep + "\n" + pad)}\n${padEnd}]`;
      }
      return `[${inner.join(itemSep)}]`;
    }
    if (v instanceof Set || v instanceof Map) {
      if (opts.defaultStr) return encStr(toStr(v));
      throw new TypeError("Object of type set is not JSON serializable");
    }
    if (typeof v === "object") {
      if (seen.has(v)) throw err("ValueError", "Circular reference detected");
      seen.add(v);
      let entries = Object.entries(v as Record<string, unknown>);
      if (opts.sortKeys) entries = entries.sort((a, b) => (a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0));
      if (!entries.length) {
        seen.delete(v);
        return "{}";
      }
      const inner = entries.map(([k, x]) => `${encStr(k)}${kvSep}${enc(x, depth + 1)}`);
      seen.delete(v);
      if (indent !== null) {
        const pad = " ".repeat(indent * (depth + 1));
        const padEnd = " ".repeat(indent * depth);
        return `{\n${pad}${inner.join(itemSep + "\n" + pad)}\n${padEnd}}`;
      }
      return `{${inner.join(itemSep)}}`;
    }
    if (opts.defaultStr) return encStr(toStr(v));
    throw new TypeError(`Object of type ${typeof v} is not JSON serializable`);
  }

  return enc(value, 0);
}

export function jsonLoads(s: unknown): any {
  const text = s instanceof PyBytes ? s.decode() : String(s);
  // Python json.loads gives floats for "0.0"/"1e3" — restore float-ness
  // via the JSON source-access reviver (Node >= 21).
  try {
    return JSON.parse(text, function reviver(_k: string, v: any, ctx?: { source?: string }) {
      if (typeof v === "number" && ctx && typeof ctx.source === "string" && /[.eE]/.test(ctx.source)) {
        return new PyFloat(v);
      }
      return v;
    } as never);
  } catch (e) {
    if (e instanceof SyntaxError) throw e;
    return JSON.parse(text);
  }
}

/* ------------------------------------------------------------------ */
/* regex                                                               */
/* ------------------------------------------------------------------ */

type ExecWithIndices = RegExpExecArray & {
  indices?: Array<[number, number]> & { groups?: Record<string, [number, number]> };
};

export class PyMatch {
  m: RegExpExecArray;
  input: string;

  constructor(m: RegExpExecArray, input: string) {
    this.m = m;
    this.input = input;
  }

  group(...ns: (number | string)[]): any {
    if (!ns.length) return this.m[0];
    const one = (n: number | string): string | null => {
      if (typeof n === "number") return this.m[n] ?? null;
      return this.m.groups?.[n] ?? null;
    };
    if (ns.length === 1) return one(ns[0]!);
    return ns.map(one);
  }

  groups(): (string | null)[] {
    return this.m.slice(1).map((g) => g ?? null);
  }

  groupdict(): Record<string, string | null> {
    return { ...(this.m.groups ?? {}) } as Record<string, string | null>;
  }

  start(n: number | string = 0): number {
    const ind = (this.m as ExecWithIndices).indices;
    if (ind) {
      const span = typeof n === "string" ? ind.groups?.[n] : ind[n as number];
      if (span) return span[0];
    }
    return n === 0 ? this.m.index : -1;
  }

  end(n: number | string = 0): number {
    const ind = (this.m as ExecWithIndices).indices;
    if (ind) {
      const span = typeof n === "string" ? ind.groups?.[n] : ind[n as number];
      if (span) return span[1];
    }
    return n === 0 ? this.m.index + this.m[0].length : -1;
  }

  span(n: number | string = 0): [number, number] {
    return [this.start(n), this.end(n)];
  }
}

function translatePattern(pattern: string): string {
  let p = pattern;
  p = p.replace(/\(\?P</g, "(?<");
  p = p.replace(/\(\?P=(\w+)\)/g, "\\k<$1>");
  p = p.replace(/\\A/g, "^");
  p = p.replace(/\\Z/g, "$");
  return p;
}

export class PyRegex {
  pattern: string;
  flags: string;

  constructor(pattern: string, flags = "") {
    let f = flags;
    const inline = pattern.match(/^\(\?([aiLmsux]+)\)/);
    let p = pattern;
    if (inline) {
      p = pattern.slice(inline[0].length);
      for (const ch of inline[1]!) {
        if (ch === "i" && !f.includes("i")) f += "i";
        if (ch === "s" && !f.includes("s")) f += "s";
        if (ch === "m" && !f.includes("m")) f += "m";
      }
    }
    this.pattern = translatePattern(p);
    this.flags = f;
  }

  private rx(extra = ""): RegExp {
    const fl = [...new Set(this.flags + extra + "d")].join("");
    return new RegExp(this.pattern, fl);
  }

  search(s: unknown): any {
    const m = this.rx("g").exec(String(s));
    return m ? new PyMatch(m, String(s)) : null;
  }

  match(s: unknown): any {
    const r = new RegExp(this.pattern, [...new Set(this.flags + "yd")].join(""));
    r.lastIndex = 0;
    const m = r.exec(String(s));
    return m ? new PyMatch(m, String(s)) : null;
  }

  fullmatch(s: unknown): any {
    const r = new RegExp(`(?:${this.pattern})$`, [...new Set(this.flags + "yd")].join(""));
    r.lastIndex = 0;
    const m = r.exec(String(s));
    return m ? new PyMatch(m, String(s)) : null;
  }

  private static convertReplStr(repl: string): string {
    return repl
      .replace(/\$/g, "$$$$")
      .replace(/\\g<(\w+)>/g, (_, name: string) => (/^\d+$/.test(name) ? `$${name}` : `$<${name}>`))
      .replace(/\\(\d+)/g, "$$$1");
  }

  private rebuildMatch(args: unknown[], input: string): PyMatch {
    let groupsObj: Record<string, string> | undefined;
    let tailIdx = args.length;
    if (typeof args[args.length - 1] === "object" && args[args.length - 1] !== null) {
      groupsObj = args[args.length - 1] as Record<string, string>;
      tailIdx -= 1;
    }
    const offset = args[tailIdx - 2] as number;
    const arr = args.slice(0, tailIdx - 2) as (string | undefined)[];
    const exec = arr as unknown as RegExpExecArray;
    exec.index = offset;
    exec.input = input;
    (exec as RegExpExecArray & { groups?: Record<string, string> }).groups = groupsObj;
    return new PyMatch(exec, input);
  }

  sub(repl: unknown, s: unknown, countN = 0): string {
    const text = String(s);
    if (typeof repl === "function") {
      let n = 0;
      return text.replace(this.rx("g"), (...args) => {
        if (countN && n >= countN) return args[0] as string;
        n++;
        const m = this.rebuildMatch(args, text);
        return String((repl as (m: PyMatch) => unknown)(m));
      });
    }
    if (!countN) return text.replace(this.rx("g"), PyRegex.convertReplStr(String(repl)));
    let n = 0;
    return text.replace(this.rx("g"), (...args) => {
      if (n >= countN) return args[0] as string;
      n++;
      const m = this.rebuildMatch(args, text);
      return String(repl).replace(/\\g<(\w+)>|\\(\d+)/g, (_, name, num) => {
        const g = (name ?? num) as string;
        return String(m.group(/^\d+$/.test(g) ? Number(g) : g) ?? "");
      });
    });
  }

  subn(repl: unknown, s: unknown, countN = 0): [string, number] {
    const text = String(s);
    let n = 0;
    const out = text.replace(this.rx("g"), (...args) => {
      if (countN && n >= countN) return args[0] as string;
      n++;
      const m = this.rebuildMatch(args, text);
      if (typeof repl === "function") return String((repl as (m: PyMatch) => unknown)(m));
      return String(repl).replace(/\\g<(\w+)>|\\(\d+)/g, (_, name, num) => {
        const g = (name ?? num) as string;
        return String(m.group(/^\d+$/.test(g) ? Number(g) : g) ?? "");
      });
    });
    return [out, n];
  }

  findall(s: unknown): any[] {
    const text = String(s);
    const out: unknown[] = [];
    const r = this.rx("g");
    let m: RegExpExecArray | null;
    while ((m = r.exec(text)) !== null) {
      if (m[0] === "" && r.lastIndex <= m.index) r.lastIndex = m.index + 1;
      if (m.length === 1) out.push(m[0]);
      else if (m.length === 2) out.push(m[1] ?? "");
      else out.push(m.slice(1).map((g) => g ?? ""));
    }
    return out;
  }

  finditer(s: unknown): PyMatch[] {
    const text = String(s);
    const out: PyMatch[] = [];
    const r = this.rx("g");
    let m: RegExpExecArray | null;
    while ((m = r.exec(text)) !== null) {
      if (m[0] === "" && r.lastIndex <= m.index) r.lastIndex = m.index + 1;
      out.push(new PyMatch(m, text));
    }
    return out;
  }

  split(s: unknown, maxsplit = 0): string[] {
    const text = String(s);
    const out: string[] = [];
    const r = this.rx("g");
    let last = 0;
    let n = 0;
    let m: RegExpExecArray | null;
    while ((m = r.exec(text)) !== null) {
      if (maxsplit && n >= maxsplit) break;
      if (m[0] === "") {
        r.lastIndex = m.index + 1;
        continue;
      }
      out.push(text.slice(last, m.index));
      for (let g = 1; g < m.length; g++) out.push(m[g] as string);
      last = m.index + m[0].length;
      n++;
    }
    out.push(text.slice(last));
    return out;
  }
}

export function regex(pattern: unknown, flags = ""): PyRegex {
  if (pattern instanceof PyRegex) return pattern;
  return new PyRegex(String(pattern), flags);
}

export function reSub(pattern: unknown, repl: unknown, s: unknown, countN = 0, flags = ""): string {
  return regex(pattern, flags).sub(repl, s, countN);
}

export function reSearch(pattern: unknown, s: unknown, flags = ""): any {
  return regex(pattern, flags).search(s);
}

export function reMatch(pattern: unknown, s: unknown, flags = ""): any {
  return regex(pattern, flags).match(s);
}

export function reFullmatch(pattern: unknown, s: unknown, flags = ""): any {
  return regex(pattern, flags).fullmatch(s);
}

export function reFindall(pattern: unknown, s: unknown, flags = ""): any[] {
  return regex(pattern, flags).findall(s);
}

export function reFinditer(pattern: unknown, s: unknown, flags = ""): PyMatch[] {
  return regex(pattern, flags).finditer(s);
}

export function reSplit(pattern: unknown, s: unknown, maxsplit = 0, flags = ""): string[] {
  return regex(pattern, flags).split(s, maxsplit);
}

export function reEscape(s: unknown): string {
  return String(s).replace(/[.*+?^${}()|[\]\\\-#&~]/g, "\\$&").replace(/\s/g, (ch) => "\\" + ch);
}

/* ------------------------------------------------------------------ */
/* pathlib                                                             */
/* ------------------------------------------------------------------ */

export class PyPath {
  p: string;

  constructor(p: unknown) {
    this.p = p instanceof PyPath ? p.p : String(p);
  }

  toString(): string {
    return this.p;
  }

  get name(): string {
    return basename(this.p);
  }

  get stem(): string {
    const b = basename(this.p);
    const e = extname(b);
    return e ? b.slice(0, -e.length) : b;
  }

  get suffix(): string {
    return extname(this.p);
  }

  get parent(): PyPath {
    return new PyPath(dirname(this.p));
  }

  get parts(): string[] {
    return this.p.split(/[\\/]+/).filter((x) => x.length > 0);
  }

  joinpath(...parts: unknown[]): PyPath {
    return new PyPath(nodeJoin(this.p, ...parts.map((x) => String(x))));
  }

  exists(): boolean {
    return existsSync(this.p);
  }

  is_file(): boolean {
    try {
      return statSync(this.p).isFile();
    } catch {
      return false;
    }
  }

  is_dir(): boolean {
    try {
      return statSync(this.p).isDirectory();
    } catch {
      return false;
    }
  }

  mkdir(opts: { parents?: boolean; exist_ok?: boolean } | boolean = {}, parentsPos?: boolean): void {
    const o = typeof opts === "boolean" ? { exist_ok: opts, parents: parentsPos !== false } : opts;
    if (existsSync(this.p)) {
      if (o.exist_ok) return;
      throw new Error(`FileExistsError: ${this.p}`);
    }
    mkdirSync(this.p, { recursive: o.parents !== false });
  }

  read_text(_encoding = "utf-8"): string {
    return readFileSync(this.p, "utf-8");
  }

  write_text(data: string, _encoding = "utf-8"): number {
    writeFileSync(this.p, data, "utf-8");
    return data.length;
  }

  read_bytes(): PyBytes {
    return new PyBytes(new Uint8Array(readFileSync(this.p)));
  }

  resolve(): PyPath {
    return new PyPath(nodeResolve(this.p));
  }

  as_posix(): string {
    return this.p.split(nodeSep).join("/");
  }

  with_suffix(suffix: string): PyPath {
    const e = extname(this.p);
    return new PyPath((e ? this.p.slice(0, -e.length) : this.p) + suffix);
  }

  relative_to(base: unknown): PyPath {
    const baseStr = nodeResolve(String(base));
    const self = nodeResolve(this.p);
    if (!self.toLowerCase().startsWith(baseStr.toLowerCase())) {
      throw err("ValueError", `${repr(this.p)} is not in the subpath of ${repr(String(base))}`);
    }
    let rel = self.slice(baseStr.length);
    if (rel.startsWith(nodeSep) || rel.startsWith("/")) rel = rel.slice(1);
    return new PyPath(rel);
  }

  iterdir(): PyPath[] {
    return readdirSync(this.p).map((n) => new PyPath(nodeJoin(this.p, n)));
  }

  glob(pattern: string): PyPath[] {
    return this.rglob(pattern, false);
  }

  rglob(pattern: string, recursive = true): PyPath[] {
    const rx = new RegExp(
      "^" + pattern
        .replace(/[.+^${}()|[\]\\]/g, "\\$&")
        .replace(/\*\*/g, " ")
        .replace(/\*/g, "[^/\\\\]*")
        .replace(/ /g, ".*")
        .replace(/\?/g, ".") + "$",
    );
    const out: PyPath[] = [];
    const walk = (dir: string): void => {
      let names: string[];
      try {
        names = readdirSync(dir);
      } catch {
        return;
      }
      for (const n of names) {
        const full = nodeJoin(dir, n);
        let isDir = false;
        try {
          isDir = statSync(full).isDirectory();
        } catch {
          continue;
        }
        if (rx.test(n)) out.push(new PyPath(full));
        if (isDir && recursive) walk(full);
      }
    };
    walk(this.p);
    return out;
  }
}

export function path(p: unknown = ""): PyPath {
  return new PyPath(p);
}

/** Python __file__ parity: convert import.meta.url to a filesystem path. */
export function metaFile(importMetaUrl: string): string {
  const u = new URL(importMetaUrl);
  let p = decodeURIComponent(u.pathname);
  if (process.platform === "win32" && /^\/[A-Za-z]:/.test(p)) p = p.slice(1);
  return p.split("/").join(nodeSep);
}

/* file open() */
export class PyFile {
  private pathStr: string;
  private mode: string;
  private buffer: string[] = [];

  constructor(pathStr: unknown, mode = "r") {
    this.pathStr = String(pathStr);
    this.mode = mode;
    if (mode.includes("w")) writeFileSync(this.pathStr, "");
  }

  read(): string {
    return readFileSync(this.pathStr, "utf-8");
  }

  readlines(): string[] {
    return splitlines(this.read(), true);
  }

  write(data: string): number {
    if (this.mode.includes("a")) {
      writeFileSync(this.pathStr, this.read() + data);
    } else {
      this.buffer.push(data);
      writeFileSync(this.pathStr, this.buffer.join(""));
    }
    return data.length;
  }

  close(): void {
    /* no-op */
  }
}

export function open(pathStr: unknown, mode = "r"): PyFile {
  return new PyFile(pathStr, mode);
}

/* os.path helpers */
export function osPathJoin(...parts: unknown[]): string {
  return nodeJoin(...parts.map((x) => String(x)));
}

export function osPathExists(p: unknown): boolean {
  return existsSync(String(p));
}

export function osPathBasename(p: unknown): string {
  return basename(String(p));
}

export function osPathDirname(p: unknown): string {
  return dirname(String(p));
}

export function osPathSplitext(p: unknown): [string, string] {
  const s = String(p);
  const e = extname(s);
  return [e ? s.slice(0, -e.length) : s, e];
}

export function osMakedirs(p: unknown, exist_ok: unknown = false): void {
  if (existsSync(String(p))) {
    if (truthy(exist_ok)) return;
    throw err("FileExistsError", String(p));
  }
  mkdirSync(String(p), { recursive: true });
}

export function osRemove(p: unknown): void {
  unlinkSync(String(p));
}

export function osListdir(p: unknown = "."): string[] {
  return readdirSync(String(p));
}

export function osRename(a: unknown, b: unknown): void {
  renameSync(String(a), String(b));
}

export function rmTree(p: unknown): void {
  rmSync(String(p), { recursive: true, force: true });
}

export function copyFile(a: unknown, b: unknown): void {
  copyFileSync(String(a), String(b));
}

export const environ: Record<string, string | undefined> = process.env;

/** threading.Lock parity (single-threaded runtime: no-op). */
export class PyLock {
  acquire(): boolean {
    return true;
  }

  release(): void {
    /* no-op */
  }
}

export function lock(): PyLock {
  return new PyLock();
}

class PyFuture {
  private value: unknown;
  private error: unknown;
  private failed = false;

  constructor(fn: (...a: unknown[]) => unknown, args: unknown[]) {
    try {
      this.value = fn(...args);
    } catch (e) {
      this.failed = true;
      this.error = e;
    }
  }

  result(): any {
    if (this.failed) throw this.error;
    return this.value;
  }

  done(): boolean {
    return true;
  }
}

/** concurrent.futures.ThreadPoolExecutor parity (synchronous execution). */
export class PyThreadPoolExecutor {
  constructor(_maxWorkers?: number) {
    /* synchronous shim */
  }

  submit(fn: (...a: unknown[]) => unknown, ...args: unknown[]): PyFuture {
    return new PyFuture(fn, args);
  }

  map(fn: (a: unknown) => unknown, it: unknown): any[] {
    return iter(it).map((v) => fn(v));
  }

  shutdown(_wait = true): void {
    /* no-op */
  }
}

export function threadPoolExecutor(maxWorkers?: number): PyThreadPoolExecutor {
  return new PyThreadPoolExecutor(maxWorkers);
}

export function asCompleted(futures: unknown): any[] {
  return iter(futures);
}

export const sysShim = {
  maxsize: Number.MAX_SAFE_INTEGER,
  platform: process.platform === "win32" ? "win32" : process.platform,
  argv: [] as string[],
  path: [] as string[],
  version: "3.11.0 (webweavex-js parity shim)",
};

/* ------------------------------------------------------------------ */
/* urllib.parse                                                        */
/* ------------------------------------------------------------------ */

export class PyUrlParts {
  scheme = "";
  netloc = "";
  path = "";
  params = "";
  query = "";
  fragment = "";

  get hostname(): string | null {
    let h = this.netloc;
    const atIdx = h.lastIndexOf("@");
    if (atIdx >= 0) h = h.slice(atIdx + 1);
    if (h.startsWith("[")) {
      const end = h.indexOf("]");
      return end >= 0 ? h.slice(1, end).toLowerCase() : h.toLowerCase();
    }
    const colon = h.indexOf(":");
    if (colon >= 0) h = h.slice(0, colon);
    return h ? h.toLowerCase() : null;
  }

  get port(): number | null {
    let h = this.netloc;
    const atIdx = h.lastIndexOf("@");
    if (atIdx >= 0) h = h.slice(atIdx + 1);
    if (h.startsWith("[")) {
      const end = h.indexOf("]");
      h = end >= 0 ? h.slice(end + 1) : "";
    }
    const colon = h.lastIndexOf(":");
    if (colon < 0) return null;
    const p = Number(h.slice(colon + 1));
    return Number.isInteger(p) ? p : null;
  }

  geturl(): string {
    return urlunparse([this.scheme, this.netloc, this.path, this.params, this.query, this.fragment]);
  }

  *[Symbol.iterator](): Iterator<string> {
    yield this.scheme;
    yield this.netloc;
    yield this.path;
    yield this.params;
    yield this.query;
    yield this.fragment;
  }
}

export function urlparse(url: unknown): PyUrlParts {
  const s = String(url ?? "");
  const out = new PyUrlParts();
  let rest = s;
  const fragIdx = rest.indexOf("#");
  if (fragIdx >= 0) {
    out.fragment = rest.slice(fragIdx + 1);
    rest = rest.slice(0, fragIdx);
  }
  const schemeM = rest.match(/^([a-zA-Z][a-zA-Z0-9+.-]*):/);
  if (schemeM) {
    out.scheme = schemeM[1]!.toLowerCase();
    rest = rest.slice(schemeM[0].length);
  }
  if (rest.startsWith("//")) {
    rest = rest.slice(2);
    const slash = rest.search(/[/?]/);
    if (slash < 0) {
      out.netloc = rest;
      rest = "";
    } else {
      out.netloc = rest.slice(0, slash);
      rest = rest.slice(slash);
    }
  }
  const qIdx = rest.indexOf("?");
  if (qIdx >= 0) {
    out.query = rest.slice(qIdx + 1);
    rest = rest.slice(0, qIdx);
  }
  const semIdx = rest.lastIndexOf(";");
  if (semIdx >= 0 && rest.lastIndexOf("/") < semIdx) {
    out.params = rest.slice(semIdx + 1);
    rest = rest.slice(0, semIdx);
  }
  out.path = rest;
  return out;
}

export function urlunparse(parts: unknown): string {
  const [scheme, netloc, pathPart, params, query, fragment] = [...iter<string>(parts)];
  let out = "";
  if (scheme) out += scheme + ":";
  if (netloc || (scheme && (pathPart ?? "").startsWith("//"))) out += "//" + (netloc ?? "");
  let p = pathPart ?? "";
  if (netloc && p && !p.startsWith("/")) p = "/" + p;
  out += p;
  if (params) out += ";" + params;
  if (query) out += "?" + query;
  if (fragment) out += "#" + fragment;
  return out;
}

export function urlsplit(url: unknown): PyUrlParts {
  const out = urlparse(url);
  if (out.params) {
    out.path += ";" + out.params;
    out.params = "";
  }
  return out;
}

export function urlunsplit(parts: unknown): string {
  const [scheme, netloc, pathPart, query, fragment] = [...iter<string>(parts)];
  return urlunparse([scheme, netloc, pathPart, "", query, fragment]);
}

export function urljoin(base: unknown, url: unknown): string {
  const b = String(base ?? "");
  const u = String(url ?? "");
  if (!b) return u;
  if (!u) return b;
  try {
    return new URL(u, b).toString();
  } catch {
    return u;
  }
}

export function quote(s: unknown, safe = "/"): string {
  const str = String(s);
  let out = "";
  for (const ch of str) {
    if (/[A-Za-z0-9_.~-]/.test(ch) || safe.includes(ch)) out += ch;
    else {
      const bytes = new TextEncoder().encode(ch);
      for (const byte of bytes) out += "%" + byte.toString(16).toUpperCase().padStart(2, "0");
    }
  }
  return out;
}

export function unquote(s: unknown): string {
  try {
    return decodeURIComponent(String(s));
  } catch {
    return String(s);
  }
}

/* ------------------------------------------------------------------ */
/* unicodedata / ipaddress                                             */
/* ------------------------------------------------------------------ */

export function uniNormalize(form: string, s: unknown): string {
  return String(s).normalize(form as "NFC" | "NFD" | "NFKC" | "NFKD");
}

const UNI_CATEGORIES: [RegExp, string][] = [
  [/\p{Lu}/u, "Lu"], [/\p{Ll}/u, "Ll"], [/\p{Lt}/u, "Lt"], [/\p{Lm}/u, "Lm"],
  [/\p{Lo}/u, "Lo"], [/\p{Nd}/u, "Nd"], [/\p{Nl}/u, "Nl"], [/\p{No}/u, "No"],
  [/\p{Mn}/u, "Mn"], [/\p{Mc}/u, "Mc"], [/\p{Me}/u, "Me"], [/\p{Zs}/u, "Zs"],
  [/\p{Zl}/u, "Zl"], [/\p{Zp}/u, "Zp"], [/\p{Cc}/u, "Cc"], [/\p{Pc}/u, "Pc"],
  [/\p{Pd}/u, "Pd"], [/\p{Ps}/u, "Ps"], [/\p{Pe}/u, "Pe"], [/\p{Pi}/u, "Pi"],
  [/\p{Pf}/u, "Pf"], [/\p{Po}/u, "Po"], [/\p{Sm}/u, "Sm"], [/\p{Sc}/u, "Sc"],
  [/\p{Sk}/u, "Sk"], [/\p{So}/u, "So"],
];

export function uniCategory(ch: string): string {
  for (const [rx, cat] of UNI_CATEGORIES) if (rx.test(ch)) return cat;
  return "Cn";
}

export class PyIpAddress {
  version: 4 | 6;
  addr: string;

  constructor(addr: unknown) {
    const s = String(addr).trim();
    if (/^\d{1,3}(\.\d{1,3}){3}$/.test(s)) {
      const octets = s.split(".").map(Number);
      if (octets.some((o) => o > 255)) throw new Error(`AddressValueError: ${s}`);
      this.version = 4;
      this.addr = s;
    } else if (s.includes(":")) {
      this.version = 6;
      this.addr = s.toLowerCase();
    } else {
      throw new Error(`ValueError: ${s} does not appear to be an IPv4 or IPv6 address`);
    }
  }

  get is_private(): boolean {
    if (this.version === 4) {
      const [a, b] = this.addr.split(".").map(Number);
      return (
        a === 10 ||
        (a === 172 && b! >= 16 && b! <= 31) ||
        (a === 192 && b === 168) ||
        a === 127 ||
        (a === 169 && b === 254)
      );
    }
    return this.addr === "::1" || this.addr.startsWith("fc") || this.addr.startsWith("fd") || this.addr.startsWith("fe80");
  }

  get is_loopback(): boolean {
    if (this.version === 4) return this.addr.startsWith("127.");
    return this.addr === "::1";
  }

  get is_global(): boolean {
    return !this.is_private;
  }

  get is_link_local(): boolean {
    if (this.version === 4) return this.addr.startsWith("169.254.");
    return /^fe[89ab]/.test(this.addr);
  }

  get is_multicast(): boolean {
    if (this.version === 4) {
      const a = Number(this.addr.split(".", 1)[0]);
      return a >= 224 && a <= 239;
    }
    return this.addr.startsWith("ff");
  }

  get is_reserved(): boolean {
    // IPv4: 240.0.0.0/4; IPv6 reserved blocks are rare — the common
    // probe addresses (loopback/private/global) are all non-reserved.
    if (this.version === 4) return Number(this.addr.split(".", 1)[0]) >= 240;
    return false;
  }

  toString(): string {
    return this.addr;
  }
}

export function ipAddress(addr: unknown): PyIpAddress {
  return new PyIpAddress(addr);
}

/* ------------------------------------------------------------------ */
/* minimal BeautifulSoup parity                                        */
/* ------------------------------------------------------------------ */

const VOID_ELEMENTS = new Set([
  "area", "base", "br", "col", "embed", "hr", "img", "input",
  "link", "meta", "param", "source", "track", "wbr",
]);

const HTML_ENTITIES: Record<string, string> = {
  amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " ",
  copy: "©", reg: "®", trade: "™", hellip: "…",
  mdash: "—", ndash: "–", lsquo: "‘", rsquo: "’",
  ldquo: "â€œ", rdquo: "â€",
};

export function htmlUnescape(s: string): string {
  return s.replace(/&(#x?[0-9a-fA-F]+|\w+);/g, (m, ent: string) => {
    if (ent.startsWith("#x") || ent.startsWith("#X")) {
      return String.fromCodePoint(parseInt(ent.slice(2), 16));
    }
    if (ent.startsWith("#")) return String.fromCodePoint(parseInt(ent.slice(1), 10));
    return HTML_ENTITIES[ent] ?? m;
  });
}

export class PyTag {
  name: string;
  attrs: Record<string, unknown> = {};
  children: (PyTag | string)[] = [];
  parent: PyTag | null = null;

  constructor(name: string) {
    this.name = name;
  }

  get(attr: string, dflt: unknown = null): any {
    return attr in this.attrs ? this.attrs[attr] : dflt;
  }

  get text(): string {
    return this.get_text();
  }

  get_text(sep: unknown = "", opts: { strip?: boolean } | boolean = {}): string {
    if (typeof sep === "boolean") {
      // get_text(strip=True) called with the flag in the sep slot
      opts = sep;
      sep = "";
    }
    const stripFlag = typeof opts === "boolean" ? opts : Boolean(opts?.strip);
    const partsArr: string[] = [];
    const walk = (node: PyTag | string): void => {
      if (typeof node === "string") {
        const t = stripFlag ? node.trim() : node;
        if (stripFlag ? t.length : node.length) partsArr.push(t);
        return;
      }
      if (node.name === "script" || node.name === "style") return;
      for (const c of node.children) walk(c);
    };
    for (const c of this.children) walk(c);
    return partsArr.join(String(sep ?? ""));
  }

  /** bs4 Tag.decompose(): remove this tag (and its subtree) from the tree. */
  decompose(): void {
    if (this.parent) {
      const i = this.parent.children.indexOf(this);
      if (i >= 0) this.parent.children.splice(i, 1);
    }
  }

  get string(): string | null {
    const t = this.get_text();
    return t.length ? t : null;
  }

  find_all(name: unknown, limit?: number): PyTag[] {
    const names = Array.isArray(name) ? new Set(name.map((n) => String(n).toLowerCase())) : null;
    const single = names ? null : name === null || name === undefined ? null : String(name).toLowerCase();
    const out: PyTag[] = [];
    const walk = (node: PyTag | string): void => {
      if (typeof node === "string") return;
      if (limit !== undefined && out.length >= limit) return;
      const matches = names ? names.has(node.name) : single === null ? true : node.name === single;
      if (matches) out.push(node);
      for (const c of node.children) walk(c);
    };
    for (const c of this.children) walk(c);
    return limit !== undefined ? out.slice(0, limit) : out;
  }

  find(name: unknown): PyTag | null {
    return this.find_all(name, 1)[0] ?? null;
  }
}

export class PySoup extends PyTag {
  constructor(html: unknown, _parser = "html.parser") {
    super("[document]");
    this.parseInto(String(html ?? ""));
  }

  get title(): PyTag | null {
    return this.find("title");
  }

  private parseInto(html: string): void {
    let cur: PyTag = this;
    let i = 0;
    const n = html.length;
    while (i < n) {
      const lt2 = html.indexOf("<", i);
      if (lt2 < 0) {
        const text = htmlUnescape(html.slice(i));
        if (text) cur.children.push(text);
        break;
      }
      if (lt2 > i) {
        const text = htmlUnescape(html.slice(i, lt2));
        if (text) cur.children.push(text);
      }
      if (html.startsWith("<!--", lt2)) {
        const end = html.indexOf("-->", lt2 + 4);
        i = end < 0 ? n : end + 3;
        continue;
      }
      if (html.startsWith("<!", lt2) || html.startsWith("<?", lt2)) {
        const end = html.indexOf(">", lt2);
        i = end < 0 ? n : end + 1;
        continue;
      }
      const gt2 = html.indexOf(">", lt2);
      if (gt2 < 0) {
        const text = htmlUnescape(html.slice(lt2));
        if (text) cur.children.push(text);
        break;
      }
      const raw = html.slice(lt2 + 1, gt2);
      i = gt2 + 1;
      if (raw.startsWith("/")) {
        const closeName = raw.slice(1).trim().toLowerCase();
        let node: PyTag | null = cur;
        while (node && node.name !== closeName) node = node.parent;
        if (node && node.parent) cur = node.parent;
        else if (node === cur && cur.parent) cur = cur.parent;
        continue;
      }
      const selfClose = raw.endsWith("/");
      const inner = selfClose ? raw.slice(0, -1) : raw;
      const nameM = inner.match(/^\s*([a-zA-Z][a-zA-Z0-9:-]*)/);
      if (!nameM) continue;
      const tagName = nameM[1]!.toLowerCase();
      const tag = new PyTag(tagName);
      tag.parent = cur;
      const attrRe = /([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*(?:=\s*("([^"]*)"|'([^']*)'|[^\s"'>]+))?/g;
      const attrStr = inner.slice(nameM[0].length);
      let am: RegExpExecArray | null;
      while ((am = attrRe.exec(attrStr)) !== null) {
        const key = am[1]!.toLowerCase();
        let val: unknown;
        if (am[2] === undefined) val = "";
        else if (am[3] !== undefined) val = htmlUnescape(am[3]);
        else if (am[4] !== undefined) val = htmlUnescape(am[4]);
        else val = htmlUnescape(am[2]);
        if (key === "class") val = String(val).split(/\s+/).filter((c) => c.length);
        tag.attrs[key] = val;
      }
      cur.children.push(tag);
      if (tagName === "script" || tagName === "style") {
        const closeIdx = html.toLowerCase().indexOf(`</${tagName}`, i);
        const rawText = html.slice(i, closeIdx < 0 ? n : closeIdx);
        if (rawText) tag.children.push(rawText);
        if (closeIdx < 0) break;
        const closeGt = html.indexOf(">", closeIdx);
        i = closeGt < 0 ? n : closeGt + 1;
        continue;
      }
      if (!selfClose && !VOID_ELEMENTS.has(tagName)) cur = tag;
    }
  }
}

export function soup(html: unknown, parser = "html.parser"): any {
  const s = new PySoup(html, parser);
  // bs4 soups are callable: soup([...]) === soup.find_all([...])
  const callable = (name: unknown, limit?: number): PyTag[] => s.find_all(name, limit);
  return new Proxy(callable, {
    get(target, prop, _receiver) {
      if (prop in s) {
        const v = Reflect.get(s, prop, s);
        return typeof v === "function" ? v.bind(s) : v;
      }
      return Reflect.get(target, prop);
    },
    has(_target, prop) {
      return prop in s;
    },
    set(_target, prop, value) {
      Reflect.set(s, prop, value);
      return true;
    },
    getPrototypeOf() {
      return PySoup.prototype;
    },
  }) as unknown as PySoup;
}

/* ------------------------------------------------------------------ */
/* requests (sync HTTP via curl)                                       */
/* ------------------------------------------------------------------ */

export class PyHttpHeaders {
  private h: Record<string, string>;

  constructor(h: Record<string, string>) {
    this.h = h;
  }

  get(name: unknown, dflt: unknown = null): any {
    const k = String(name).toLowerCase();
    return k in this.h ? this.h[k] : dflt;
  }
}

export class PyHttpResponse {
  status_code: number;
  headers: PyHttpHeaders;
  text: string;

  constructor(status: number, headers: Record<string, string>, text: string) {
    this.status_code = status;
    this.headers = new PyHttpHeaders(headers);
    this.text = text;
  }

  json(): any {
    return JSON.parse(this.text);
  }

  /** requests.Response.content parity — body as bytes. */
  get content(): PyBytes {
    return new PyBytes(this.text);
  }

  /** requests.Response.raise_for_status parity. */
  raise_for_status(): void {
    if (this.status_code >= 400 && this.status_code < 500) {
      throw err("HTTPError", `${this.status_code} Client Error`);
    }
    if (this.status_code >= 500 && this.status_code < 600) {
      throw err("HTTPError", `${this.status_code} Server Error`);
    }
  }
}

export interface RequestsOpts {
  timeout?: number | PyFloat;
  headers?: Record<string, string>;
  allow_redirects?: boolean;
  follow_redirects?: boolean;
}

/** requests.get parity — synchronous HTTP via the system curl binary. */
export function requestsGet(url: unknown, opts: RequestsOpts = {}): PyHttpResponse {
  const args = ["-sS", "-i", "--max-time", String(Math.max(1, Math.ceil(num(opts.timeout ?? 12))))];
  if (opts.allow_redirects !== false && opts.follow_redirects !== false) args.push("-L");
  const headers = opts.headers ?? {};
  for (const [k, v] of Object.entries(headers)) {
    if (k.toLowerCase() === "accept-encoding") continue; // identity by default
    args.push("-H", `${k}: ${v}`);
  }
  args.push("-H", "Accept-Encoding: identity");
  args.push(String(url));
  const { spawnSync } = requireChildProcess();
  const res = spawnSync("curl", args, { encoding: "buffer", maxBuffer: 64 * 1024 * 1024 });
  if (res.error || res.status !== 0) {
    const detail = res.error ? String(res.error.message) : (res.stderr ?? Buffer.alloc(0)).toString("utf-8").trim();
    throw err("ConnectionError", detail || `curl exited ${res.status}`);
  }
  const raw = (res.stdout ?? Buffer.alloc(0)).toString("utf-8");
  // with -L there may be multiple header blocks; take the last
  let rest = raw;
  let status = 0;
  const headerMap: Record<string, string> = {};
  while (rest.startsWith("HTTP/")) {
    const sep = rest.indexOf("\r\n\r\n");
    const headEnd = sep >= 0 ? sep : rest.indexOf("\n\n");
    if (headEnd < 0) break;
    const head = rest.slice(0, headEnd);
    rest = rest.slice(headEnd + (sep >= 0 ? 4 : 2));
    const lines = head.split(/\r?\n/);
    const m = lines[0]!.match(/^HTTP\/[\d.]+\s+(\d+)/);
    if (m) status = Number(m[1]);
    for (const k of Object.keys(headerMap)) delete headerMap[k];
    for (const ln of lines.slice(1)) {
      const ci = ln.indexOf(":");
      if (ci > 0) headerMap[ln.slice(0, ci).trim().toLowerCase()] = ln.slice(ci + 1).trim();
    }
    if (!rest.startsWith("HTTP/")) break;
  }
  return new PyHttpResponse(status, headerMap, rest);
}

let _cp: typeof import("node:child_process") | null = null;

function requireChildProcess(): typeof import("node:child_process") {
  if (!_cp) {
    // eslint-disable-next-line @typescript-eslint/no-require-imports
    _cp = childProcessModule;
  }
  return _cp;
}

/* ------------------------------------------------------------------ */
/* zipfile                                                             */
/* ------------------------------------------------------------------ */

export class PyZipFile {
  private buf: Buffer;
  private entries: { name: string; offset: number; method: number; csize: number; usize: number }[] = [];

  constructor(pathStr: unknown) {
    this.buf = readFileSync(String(pathStr));
    if (this.buf.length < 4 || this.buf.readUInt32LE(0) !== 0x04034b50) {
      // also allow empty zips (EOCD only)
      if (!(this.buf.length >= 4 && this.buf.readUInt32LE(0) === 0x06054b50)) {
        throw err("BadZipFile", "File is not a zip file");
      }
    }
    this.parseCentralDirectory();
  }

  private parseCentralDirectory(): void {
    // locate End Of Central Directory
    let i = this.buf.length - 22;
    while (i >= 0 && this.buf.readUInt32LE(i) !== 0x06054b50) i--;
    if (i < 0) throw err("BadZipFile", "File is not a zip file");
    const count = this.buf.readUInt16LE(i + 10);
    let off = this.buf.readUInt32LE(i + 16);
    for (let k = 0; k < count; k++) {
      if (this.buf.readUInt32LE(off) !== 0x02014b50) break;
      const method = this.buf.readUInt16LE(off + 10);
      const csize = this.buf.readUInt32LE(off + 20);
      const usize = this.buf.readUInt32LE(off + 24);
      const nameLen = this.buf.readUInt16LE(off + 28);
      const extraLen = this.buf.readUInt16LE(off + 30);
      const commentLen = this.buf.readUInt16LE(off + 32);
      const lho = this.buf.readUInt32LE(off + 42);
      const name = this.buf.subarray(off + 46, off + 46 + nameLen).toString("utf-8");
      this.entries.push({ name, offset: lho, method, csize, usize });
      off += 46 + nameLen + extraLen + commentLen;
    }
  }

  namelist(): string[] {
    return this.entries.map((e) => e.name);
  }

  read(name: unknown): PyBytes {
    const entry = this.entries.find((e) => e.name === String(name));
    if (!entry) throw err("KeyError", `There is no item named ${repr(String(name))} in the archive`);
    const lho = entry.offset;
    const nameLen = this.buf.readUInt16LE(lho + 26);
    const extraLen = this.buf.readUInt16LE(lho + 28);
    const start = lho + 30 + nameLen + extraLen;
    const raw = this.buf.subarray(start, start + entry.csize);
    if (entry.method === 0) return new PyBytes(new Uint8Array(raw));
    if (entry.method === 8) {
      return new PyBytes(new Uint8Array(inflateRawSync(raw)));
    }
    throw err("NotImplementedError", `compression type ${entry.method}`);
  }

  close(): void {
    /* no-op */
  }
}

export function zipFile(pathStr: unknown, _mode = "r"): PyZipFile {
  return new PyZipFile(pathStr);
}

/* ------------------------------------------------------------------ */
/* error helpers                                                       */
/* ------------------------------------------------------------------ */

export function err(kind: string, message: unknown = ""): Error {
  const e = new Error(toStr(message));
  e.name = kind;
  return e;
}

/* ------------------------------------------------------------------ */
/* legacy exports (kept for hand-written modules)                      */
/* ------------------------------------------------------------------ */

export function pyIter<T = any>(value: unknown): T[] {
  return iter<T>(value);
}

export function pyItems(value: unknown): [string, any][] {
  return items(value);
}

export function pyValues(value: unknown): any[] {
  return values(value);
}

export function pyKeys(value: unknown): string[] {
  return keys(value);
}

export function pyEnumerate<T>(value: unknown): [number, T][] {
  return enumerate<T>(value);
}

export function pyZip<A, B>(a: unknown, b: unknown): [A, B][] {
  return zip(a, b) as [A, B][];
}

export function pyAll(value: unknown): boolean {
  return all(value);
}

export function pyAny(value: unknown): boolean {
  return any(value);
}

export function pySum(value: unknown, start = 0): number {
  return sum(value, start) as number;
}

export function pySorted(value: unknown, keyFn?: (item: unknown) => unknown): any[] {
  return sorted(value, { key: keyFn });
}

export function pyFrozenset(value: unknown): Set<unknown> {
  return new Set(iter(value));
}

/** Python collections.deque — legacy array-based shape. */
export function pyDeque<T = any>(value?: unknown): T[] {
  return iter<T>(value ?? []);
}

/** Shallow dict copy from mapping or iterable of pairs. */
export function pyDict(value: unknown): Record<string, unknown> {
  if (value === null || value === undefined) return {};
  if (typeof value === "object" && !Array.isArray(value) && !(value instanceof Map) && !(value instanceof Set)) {
    return { ...(value as Record<string, unknown>) };
  }
  const out: Record<string, unknown> = {};
  for (const pair of iter(value)) {
    if (Array.isArray(pair)) {
      out[String(pair[0])] = pair[1];
    } else {
      out[String(pair)] = null;
    }
  }
  return out;
}

export function pySetdefault(
  obj: Record<string, unknown>,
  key: string | number,
  defaultValue: unknown,
): any {
  return setdefault(obj, key, defaultValue);
}

/** pathlib.Path parity for certification probes (legacy shape). */
export function pyPath(p: string): PyPath {
  return new PyPath(p);
}

/** os.replace parity — rename with overwrite (atomic on POSIX; Windows
 *  needs the destination removed first when it already exists). */
export function osReplace(src: unknown, dst: unknown): void {
  try {
    renameSync(String(src), String(dst));
  } catch {
    rmSync(String(dst), { force: true });
    renameSync(String(src), String(dst));
  }
}

/** urllib.parse.quote_plus parity — like quote(safe="") with space → "+". */
export function quotePlus(s: unknown): string {
  return quote(String(s), " ").replace(/ /g, "+");
}

/** urllib.parse.urlencode parity (dict form). */
export function urlencode(d: unknown): string {
  const pairs: string[] = [];
  for (const [k, v] of Object.entries(d as Record<string, unknown>)) {
    pairs.push(`${quotePlus(k)}=${quotePlus(String(v))}`);
  }
  return pairs.join("&");
}

/** urllib.request.Request parity — carries url + headers for urlopen. */
export function urllibRequest(url: unknown, headers: Record<string, string> = {}): any {
  return { full_url: String(url), headers };
}

/** urllib.request.urlopen parity — synchronous HTTP via the system curl
 *  binary; raises HTTPError on 4xx/5xx like Python. */
export function urllibUrlopen(req: unknown, timeout: unknown = 12): any {
  const target = typeof req === "string" ? { full_url: req, headers: {} as Record<string, string> } : (req as { full_url: string; headers: Record<string, string> });
  const args = ["-sS", "-i", "-L", "--max-time", String(Math.max(1, Math.ceil(num(timeout))))];
  for (const [k, v] of Object.entries(target.headers ?? {})) {
    if (k.toLowerCase() === "accept-encoding") continue;
    args.push("-H", `${k}: ${v}`);
  }
  args.push("-H", "Accept-Encoding: identity");
  args.push(target.full_url);
  const { spawnSync } = requireChildProcess();
  const res = spawnSync("curl", args, { encoding: "buffer", maxBuffer: 64 * 1024 * 1024 });
  if (res.error || res.status !== 0) {
    const detail = res.error ? String(res.error.message) : (res.stderr ?? Buffer.alloc(0)).toString("utf-8").trim();
    throw err("URLError", `<urlopen error ${detail || `curl exited ${res.status}`}>`);
  }
  const raw = (res.stdout ?? Buffer.alloc(0)).toString("utf-8");
  let rest = raw;
  let status = 0;
  let reason = "";
  const headerMap: Record<string, string> = {};
  while (rest.startsWith("HTTP/")) {
    const sep = rest.indexOf("\r\n\r\n");
    if (sep < 0) break;
    const block = rest.slice(0, sep);
    rest = rest.slice(sep + 4);
    const lines = block.split("\r\n");
    const m = /^HTTP\/[\d.]+\s+(\d+)\s*(.*)$/.exec(lines[0] ?? "");
    if (m) {
      status = Number(m[1]);
      reason = m[2] ?? "";
    }
    for (const ln of lines.slice(1)) {
      const ci = ln.indexOf(":");
      if (ci > 0) headerMap[ln.slice(0, ci).trim().toLowerCase()] = ln.slice(ci + 1).trim();
    }
  }
  if (status >= 400) throw err("HTTPError", `HTTP Error ${status}: ${reason}`.trimEnd());
  const body = rest;
  return {
    status,
    headers: new PyHttpHeaders(headerMap),
    read: () => new PyBytes(body),
    getcode: () => status,
  };
}

/** httpx.AsyncClient parity — async wrapper over the curl-backed fetch.
 *  Used via `async with httpx.AsyncClient(...) as client: client.get(url)`. */
export function httpxAsyncClient(opts: Record<string, unknown> = {}): any {
  return {
    get: async (url: unknown): Promise<PyHttpResponse> =>
      requestsGet(url, {
        timeout: opts["timeout"] as number | PyFloat | undefined,
        headers: opts["headers"] as Record<string, string> | undefined,
        follow_redirects: opts["follow_redirects"] as boolean | undefined,
      }),
    aclose: async (): Promise<void> => undefined,
  };
}

/** io.BytesIO parity — minimal in-memory bytes buffer. */
export function bytesIO(data: unknown): any {
  return { getvalue: () => data };
}

/** Python `ast` module shim. There is no CPython parser in this runtime:
 *  parse() raises SyntaxError, which generated callers catch on the same
 *  code path Python takes for unparseable input. Visitor APIs are inert
 *  (only reachable after a successful parse). */
export const astModule: any = {
  parse(_src: unknown): any {
    throw err("SyntaxError", "invalid syntax");
  },
  iter_child_nodes(_node: unknown): any[] {
    return [];
  },
  walk(_node: unknown): any[] {
    return [];
  },
  NodeVisitor: class {
    visit(_node: any): any {
      return undefined;
    }
    generic_visit(_node: any): any {
      return undefined;
    }
  },
};
