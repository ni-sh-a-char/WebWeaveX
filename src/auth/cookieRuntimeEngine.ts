/**
 * Production parity: core/auth/cookie_runtime_engine.py
 */

const MAX_COOKIES = 1000;

export function extractCookies(context: unknown): Record<string, unknown> {
  if (context == null) {
    return { cookies: [], bounded: true };
  }

  let cookies: unknown[] = [];
  const ctx = context as Record<string, unknown>;
  if ("_test_cookies" in ctx) {
    cookies = [...(ctx._test_cookies as unknown[])];
  } else if (typeof (ctx as { cookies?: () => unknown[] }).cookies === "function") {
    try {
      cookies = [...(ctx as { cookies: () => unknown[] }).cookies()];
    } catch {
      cookies = [];
    }
  }

  const normalized = [...cookies.slice(0, MAX_COOKIES)]
    .map((c) =>
      c && typeof c === "object" && !Array.isArray(c)
        ? { ...(c as Record<string, unknown>) }
        : {},
    )
    .sort((a, b) => {
      const ka = [
        String((a as Record<string, unknown>).name ?? ""),
        String((a as Record<string, unknown>).domain ?? ""),
        String((a as Record<string, unknown>).path ?? ""),
      ];
      const kb = [
        String((b as Record<string, unknown>).name ?? ""),
        String((b as Record<string, unknown>).domain ?? ""),
        String((b as Record<string, unknown>).path ?? ""),
      ];
      for (let i = 0; i < ka.length; i++) {
        const c = ka[i]!.localeCompare(kb[i]!);
        if (c !== 0) return c;
      }
      return 0;
    });

  return { cookies: normalized, bounded: true };
}

export function injectCookies(
  context: unknown,
  cookies: Record<string, unknown>[],
): Record<string, unknown> {
  const bounded = [...cookies.slice(0, MAX_COOKIES)]
    .map((c) => ({ ...c }))
    .sort((a, b) => {
      const ka = [
        String(a.name ?? ""),
        String(a.domain ?? ""),
      ];
      const kb = [
        String(b.name ?? ""),
        String(b.domain ?? ""),
      ];
      for (let i = 0; i < ka.length; i++) {
        const c = ka[i]!.localeCompare(kb[i]!);
        if (c !== 0) return c;
      }
      return 0;
    });

  if (context == null) {
    return { injected: false, cookie_count: 0, bounded: true };
  }

  const ctx = context as Record<string, unknown> & {
    add_cookies?: (c: unknown[]) => void;
    _test_cookies?: unknown[];
  };
  if (typeof ctx.add_cookies === "function" && bounded.length > 0) {
    ctx.add_cookies(bounded);
  }
  if ("_test_cookies" in ctx) {
    ctx._test_cookies = bounded;
  }

  return {
    injected: true,
    cookie_count: bounded.length,
    serialized: JSON.stringify(bounded),
    bounded: true,
  };
}
