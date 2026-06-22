package io.webweavex.auth;

import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyRepr;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Port of {@code core.auth.authentication_runtime_engine.authenticate_runtime} for the
 * page-independent contract. Dependency-clean (0 forbidden, importable). The cookie/token/form
 * authentication methods require a live Playwright {@code page} (side-effecting injection); they
 * are page-coupled and not byte-exact-testable here. The {@code page=None} contract is a pure
 * function of {@code config} (always {@code missing_page}) and is certified byte-exact. Zero new
 * substrate.
 */
public final class AuthenticationRuntime {

    private AuthenticationRuntime() {
    }

    private static Map<String, Object> map() {
        return new LinkedHashMap<>();
    }

    /**
     * {@code authenticate_runtime(page=None, credentials, config)} — the page-independent path
     * (returns {@code missing_page} for every input, mirroring canon when no page is available).
     */
    public static Map<String, Object> authenticateRuntime(Map<String, Object> credentials,
            Map<String, Object> config) {
        Map<String, Object> cfg = config == null ? map() : config;
        String method = PyRepr.str(Py.get(cfg, "method", "cookie_injection")).strip();
        Map<String, Object> out = map();
        out.put("authenticated", false);
        out.put("method", method);
        out.put("reason", "missing_page");
        out.put("bounded", true);
        return out;
    }
}
