/**
 * Execute a single JavaScript module export probe; stdout JSON result.
 * Usage: npx tsx tools/convergence/js_probe_runner.ts --import <path> --export <name> --args-json '{}'
 */
import { readFileSync } from "node:fs";
import { pathToFileURL, fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import { toStr as pyToStr, jsonLoads as pyJsonLoads } from "../../src/runtime/pyCompat.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

type ProbeResult = {
  ok: boolean;
  error: string | null;
  output: unknown;
  trace?: string;
};

function serialize(value: unknown, depth = 0): unknown {
  if (depth > 8) return pyToStr(value); // Python str() rendering at cutoff
  if (value === null || value === undefined) return null;
  if (typeof value === "boolean" || typeof value === "number" || typeof value === "string") return value;
  if ((value as object)?.constructor?.name === "PyFloat") {
    return (value as { v: number }).v;
  }
  if (Array.isArray(value)) return value.slice(0, 200).map((v) => serialize(v, depth + 1));
  if (typeof value === "object") {
    const ctor = (value as object).constructor?.name;
    const maybeGen = value as { next?: unknown; [Symbol.iterator]?: unknown };
    if (
      typeof maybeGen.next === "function" &&
      typeof maybeGen[Symbol.iterator] === "function" &&
      ctor !== "Object"
    ) {
      const out: unknown[] = [];
      for (const v of value as Iterable<unknown>) {
        if (out.length >= 200) break;
        out.push(serialize(v, depth + 1));
      }
      return out;
    }
    // Python-parity shim types serialize like their Python str() counterparts
    if (ctor === "PyBytes") return String(value);
    if (ctor === "PyPath") return String(value);
    if (ctor === "PyRegex") {
      return `re.compile('${(value as { pattern: string }).pattern}')`;
    }
    if (value instanceof Map) {
      const out: Record<string, unknown> = {};
      for (const [k, v] of [...value.entries()].slice(0, 200)) out[String(k)] = serialize(v, depth + 1);
      return out;
    }
    const out: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(value as Record<string, unknown>).slice(0, 200)) {
      out[k] = serialize(v, depth + 1);
    }
    return out;
  }
  return String(value);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const get = (flag: string): string => {
    const i = args.indexOf(flag);
    return i >= 0 ? String(args[i + 1] ?? "") : "";
  };
  const importPath = get("--import");
  const exportName = get("--export");
  const methodName = get("--method");
  const argsJson = get("--args-json") || "{}";
  const argsFile = get("--args-file");
  const paramOrderRaw = get("--param-order");
  const paramOrder: string[] = paramOrderRaw ? (JSON.parse(paramOrderRaw) as string[]) : [];
  const ctorArgsRaw = get("--ctor-args-json");
  const ctorArgsFile = get("--ctor-args-file");
  const ctorOrderRaw = get("--ctor-param-order");
  const root = resolve(__dirname, "../..");
  const full = resolve(root, importPath);
  let payload: ProbeResult = { ok: false, error: "missing args", output: null };
  try {
    const mod = await import(pathToFileURL(full).href);
    if (exportName === "__constants__") {
      const consts: Record<string, unknown> = {};
      for (const [k, v] of Object.entries(mod as Record<string, unknown>)) {
        if (typeof v === "function") continue;
        consts[k] = v;
      }
      console.log(JSON.stringify({ ok: true, error: null, output: serialize(consts) }));
      process.exit(0);
    }
    const exported = mod[exportName] as unknown;
    const callArgs = argsFile
      ? (pyJsonLoads(readFileSync(argsFile, "utf8")) as Record<string, unknown> | unknown[])
      : (pyJsonLoads(argsJson) as Record<string, unknown> | unknown[]);

    const applyArgs = (f: (...a: unknown[]) => unknown, self: unknown): unknown => {
      if (Array.isArray(callArgs)) return f.apply(self, callArgs);
      if (!Object.keys(callArgs).length) return f.apply(self, []);
      if (paramOrder.length) return f.apply(self, paramOrder.map((name) => (callArgs as Record<string, unknown>)[name]));
      return f.apply(self, Object.values(callArgs));
    };

    const isClass = typeof exported === "function" && /^class[\s{]/.test(Function.prototype.toString.call(exported));

    if (typeof exported !== "function") {
      payload = { ok: false, error: `export ${exportName} not a function`, output: null };
    } else if (methodName || isClass) {
      // instantiate class, then call method (or serialize instance state)
      const ctorArgs = ctorArgsFile
        ? (JSON.parse(readFileSync(ctorArgsFile, "utf8")) as Record<string, unknown>)
        : ctorArgsRaw
          ? (JSON.parse(ctorArgsRaw) as Record<string, unknown>)
          : {};
      const ctorOrder: string[] = ctorOrderRaw ? (JSON.parse(ctorOrderRaw) as string[]) : Object.keys(ctorArgs);
      const Cls = exported as (new (...a: unknown[]) => Record<string, unknown>) & Record<string, unknown>;
      if (!methodName) {
        // method-less probe: the probe args ARE the constructor args
        const useCallArgs = !Array.isArray(callArgs) && Object.keys(callArgs).length > 0;
        const instance = useCallArgs
          ? new Cls(...(paramOrder.length
            ? paramOrder.map((n) => (callArgs as Record<string, unknown>)[n])
            : Object.values(callArgs)))
          : new Cls(...ctorOrder.map((name) => ctorArgs[name]));
        payload = { ok: true, error: null, output: serialize(instance) };
      } else if (typeof Cls[methodName] === "function") {
        // static / class method
        const out = applyArgs(Cls[methodName] as (...a: unknown[]) => unknown, Cls);
        const resolved = out instanceof Promise ? await out : out;
        payload = { ok: true, error: null, output: serialize(resolved) };
      } else {
        const instance = new Cls(...ctorOrder.map((name) => ctorArgs[name]));
        const method = (instance as Record<string, unknown>)[methodName];
        if (typeof method !== "function") {
          payload = { ok: false, error: `method ${methodName} not found`, output: null };
        } else {
          const out = applyArgs(method as (...a: unknown[]) => unknown, instance);
          const resolved = out instanceof Promise ? await out : out;
          payload = { ok: true, error: null, output: serialize(resolved) };
        }
      }
    } else {
      const out = applyArgs(exported as (...a: unknown[]) => unknown, undefined);
      const resolved = out instanceof Promise ? await out : out;
      payload = { ok: true, error: null, output: serialize(resolved) };
    }
  } catch (e) {
    const msg = e instanceof Error
      ? (e.name && e.name !== "Error" ? `${e.name}: ${e.message}` : e.message)
      : String(e);
    payload = {
      ok: false,
      error: msg,
      output: null,
      trace: e instanceof Error ? e.stack?.slice(-500) : undefined,
    };
  }
  console.log(JSON.stringify(payload));
  process.exit(payload.ok ? 0 : 1);
}

main();
