package io.webweavex.identity;

import io.webweavex.crypto.Kaalka;
import io.webweavex.crypto.KaalkaSession;
import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.PyJson;
import io.webweavex.determinism.PyJsonParse;
import io.webweavex.determinism.PyRepr;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.TreeMap;

/**
 * Port of the {@code core.identity} family — {@code build_browser_identity} (the browser-identity
 * orchestrator fanning to ~11 deterministic fingerprint engines) and the
 * {@code save/load_browser_identity} persistence pair. Dependency-clean (28-module closure, 0
 * forbidden, verified importable). Reuses the certified {@link Kaalka} hash substrate
 * ({@code compute_kaalka_hash} / {@code compute_kaalka_hash_payload} are both the deterministic
 * sha256-of-stable_serialize hash) and {@link KaalkaSession} session envelope. Zero new substrate.
 */
public final class IdentityRuntime {

    private IdentityRuntime() {
    }

    // -------------------------------------------------------------- helpers

    private static Map<String, Object> map() {
        return new LinkedHashMap<>();
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> asMap(Object o) {
        return o instanceof Map ? (Map<String, Object>) o : map();
    }

    private static String str(Object o) {
        return PyRepr.str(o);
    }

    private static Map<String, Object> mapOf(Object... kv) {
        Map<String, Object> m = map();
        for (int i = 0; i < kv.length; i += 2) {
            m.put((String) kv[i], kv[i + 1]);
        }
        return m;
    }

    private static List<Object> listOf(Object... xs) {
        List<Object> l = new ArrayList<>();
        for (Object x : xs) {
            l.add(x);
        }
        return l;
    }

    // -------------------------------------------------------------- static profile tables

    private static final List<String> PROFILE_IDS = List.of("default", "profile_a", "profile_b");

    private static String boundedProfile(String profileId) {
        return PROFILE_IDS.contains(profileId) ? profileId : "default";
    }

    private static final Map<String, String> USER_AGENTS = Map.of(
            "default", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    + "Chrome/120.0.0.0 Safari/537.36",
            "profile_a", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                    + "Chrome/120.0.0.0 Safari/537.36",
            "profile_b", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    + "Chrome/120.0.0.0 Safari/537.36");

    private static final Map<String, String> PLATFORMS = Map.of(
            "default", "Win32", "profile_a", "MacIntel", "profile_b", "Linux x86_64");

    private static final Map<String, List<String>> LANGUAGES = Map.of(
            "default", List.of("en-US", "en"), "profile_a", List.of("en-GB", "en"),
            "profile_b", List.of("en-US", "en"));

    private static final Map<String, String> TIMEZONES = Map.of(
            "default", "America/New_York", "profile_a", "Europe/London", "profile_b", "America/Los_Angeles");

    private static final Map<String, List<String>> FONTS = Map.of(
            "default", List.of("Arial", "Courier New", "Segoe UI", "Times New Roman", "Verdana"),
            "profile_a", List.of("Arial", "Helvetica", "Menlo", "Times New Roman"),
            "profile_b", List.of("DejaVu Sans", "Liberation Sans", "Ubuntu", "Noto Sans"));

    // -------------------------------------------------------------- fingerprint engines

    public static Map<String, Object> buildBrowserProfile(String profileId) {
        String bounded = boundedProfile(profileId);
        Map<String, Object> out = map();
        out.put("profile_id", bounded);
        out.put("profile_seed", Kaalka.computeKaalkaHash(bounded));
        out.put("rotation_index", 0L);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildUserAgentRuntime(String profileId) {
        String p = USER_AGENTS.containsKey(profileId) ? profileId : "default";
        Map<String, Object> out = map();
        out.put("user_agent", USER_AGENTS.get(p));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildPlatformRuntime(String profileId) {
        String p = PLATFORMS.containsKey(profileId) ? profileId : "default";
        Map<String, Object> out = map();
        out.put("platform", PLATFORMS.get(p));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildLanguageRuntime(String profileId) {
        String p = LANGUAGES.containsKey(profileId) ? profileId : "default";
        Map<String, Object> out = map();
        out.put("languages", new ArrayList<Object>(LANGUAGES.get(p)));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildTimezoneRuntime(String profileId) {
        String p = TIMEZONES.containsKey(profileId) ? profileId : "default";
        Map<String, Object> out = map();
        out.put("timezone", TIMEZONES.get(p));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildWebglRuntime(String profileId) {
        Map<String, Object> out = map();
        List<Object> ext;
        if ("profile_a".equals(profileId)) {
            out.put("vendor", "Apple Inc.");
            out.put("renderer", "Apple GPU");
            ext = listOf("WEBGL_debug_renderer_info");
        } else if ("profile_b".equals(profileId)) {
            out.put("vendor", "Google Inc. (NVIDIA)");
            out.put("renderer", "ANGLE (NVIDIA, NVIDIA GeForce GTX 1060)");
            ext = listOf("WEBGL_debug_renderer_info", "EXT_texture_filter_anisotropic");
        } else {
            out.put("vendor", "Google Inc. (Intel)");
            out.put("renderer", "ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0)");
            ext = listOf("WEBGL_debug_renderer_info", "OES_texture_float");
        }
        ext.sort((a, b) -> Normalization.codePointCompare(str(a), str(b)));
        out.put("extensions", ext);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildCanvasRuntime(String profileId) {
        Map<String, Object> payload = map();
        payload.put("profile_id", profileId);
        payload.put("canvas_seed", "webweavex-canvas:" + profileId);
        Map<String, Object> out = map();
        out.put("canvas_fingerprint", Kaalka.computeKaalkaHash(payload));
        out.put("canvas_seed", "webweavex-canvas:" + profileId);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildFontRuntime(String profileId) {
        String p = FONTS.containsKey(profileId) ? profileId : "default";
        List<Object> fonts = new ArrayList<>(FONTS.get(p));
        fonts.sort((a, b) -> Normalization.codePointCompare(str(a), str(b)));
        Map<String, Object> out = map();
        out.put("fonts", fonts);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildMediaDeviceRuntime(String profileId) {
        Map<String, Object> out = map();
        if ("profile_a".equals(profileId)) {
            out.put("audio_inputs", listOf("MacBook Microphone"));
            out.put("video_inputs", listOf("FaceTime HD Camera"));
            out.put("audio_outputs", listOf("MacBook Speakers"));
        } else if ("profile_b".equals(profileId)) {
            out.put("audio_inputs", listOf("USB Audio Device"));
            out.put("video_inputs", listOf("HD Pro Webcam"));
            out.put("audio_outputs", listOf("HDMI Output"));
        } else {
            out.put("audio_inputs", listOf("Default Microphone"));
            out.put("video_inputs", listOf("Integrated Camera"));
            out.put("audio_outputs", listOf("Default Speakers"));
        }
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildNavigatorRuntime(String profileId) {
        Map<String, Object> ua = buildUserAgentRuntime(profileId);
        Map<String, Object> platform = buildPlatformRuntime(profileId);
        Map<String, Object> languages = buildLanguageRuntime(profileId);
        Map<String, Object> permissions = map();
        permissions.put("notifications", "default");
        permissions.put("geolocation", "prompt");
        Map<String, Object> out = map();
        out.put("webdriver", false);
        out.put("plugins", listOf("Chrome PDF Plugin", "Chrome PDF Viewer"));
        out.put("mimeTypes", listOf("application/pdf"));
        out.put("hardwareConcurrency", 8L);
        out.put("deviceMemory", 8L);
        out.put("languages", languages.get("languages"));
        out.put("permissions", permissions);
        out.put("user_agent", ua.get("user_agent"));
        out.put("platform", platform.get("platform"));
        out.put("bounded", true);
        return out;
    }

    /** {@code normalize_browser_fingerprint}. */
    public static Map<String, Object> normalizeBrowserFingerprint(Map<String, Object> identity) {
        Map<String, Object> normalized = map();
        TreeMap<String, Object> sorted = new TreeMap<>(Normalization::codePointCompare);
        sorted.putAll(identity);
        for (Map.Entry<String, Object> e : sorted.entrySet()) {
            if (e.getKey().equals("bounded")) {
                continue;
            }
            Object value = e.getValue();
            if (value instanceof Map) {
                Map<String, Object> inner = asMap(value);
                TreeMap<String, Object> innerSorted = new TreeMap<>(Normalization::codePointCompare);
                innerSorted.putAll(inner);
                Map<String, Object> lowered = map();
                for (Map.Entry<String, Object> ie : innerSorted.entrySet()) {
                    lowered.put(ie.getKey().toLowerCase(Locale.ROOT), ie.getValue());
                }
                normalized.put(e.getKey(), lowered);
            } else if (value instanceof List) {
                List<Object> lowered = new ArrayList<>();
                for (Object item : (List<?>) value) {
                    lowered.add(str(item).toLowerCase(Locale.ROOT));
                }
                lowered.sort((a, b) -> Normalization.codePointCompare((String) a, (String) b));
                normalized.put(e.getKey(), lowered);
            } else {
                normalized.put(e.getKey(), str(value).strip().toLowerCase(Locale.ROOT));
            }
        }
        return normalized;
    }

    /** {@code compute_runtime_entropy} (observed=None path used by the orchestrator). */
    public static Map<String, Object> computeRuntimeEntropy(Map<String, Object> identity,
            Map<String, Object> observed) {
        String baseline = Kaalka.computeKaalkaHash(normalizeBrowserFingerprint(identity));
        Map<String, Object> out = map();
        if (observed == null || observed.isEmpty()) {
            out.put("entropy_score", 0.0);
            out.put("stable", true);
            out.put("baseline_hash", baseline);
            out.put("bounded", true);
            return out;
        }
        String observedHash = Kaalka.computeKaalkaHash(normalizeBrowserFingerprint(observed));
        double drift = observedHash.equals(baseline) ? 0.0 : 1.0;
        out.put("entropy_score", drift);
        out.put("stable", drift == 0.0);
        out.put("baseline_hash", baseline);
        out.put("observed_hash", observedHash);
        out.put("bounded", true);
        return out;
    }

    public static String fingerprintBrowserIdentity(Map<String, Object> identity) {
        return Kaalka.computeKaalkaHash(normalizeBrowserFingerprint(identity));
    }

    private static final Map<String, Map<String, Object>> SCREEN_PROFILES = Map.of(
            "default", mapOf("width", 1920L, "height", 1080L, "colorDepth", 24L),
            "profile_a", mapOf("width", 1440L, "height", 900L, "colorDepth", 24L),
            "profile_b", mapOf("width", 2560L, "height", 1440L, "colorDepth", 24L));

    private static Map<String, Object> screenFor(String boundedId) {
        Map<String, Object> base = SCREEN_PROFILES.getOrDefault(boundedId, SCREEN_PROFILES.get("default"));
        // dict(...) -> insertion order width,height,colorDepth
        Map<String, Object> s = map();
        s.put("width", base.get("width"));
        s.put("height", base.get("height"));
        s.put("colorDepth", base.get("colorDepth"));
        return s;
    }

    // -------------------------------------------------------------- orchestrator

    /** {@code build_browser_identity}. */
    public static Map<String, Object> buildBrowserIdentity(String profileId) {
        Map<String, Object> profile = buildBrowserProfile(profileId);
        String boundedId = (String) profile.get("profile_id");

        Map<String, Object> ua = buildUserAgentRuntime(boundedId);
        Map<String, Object> platform = buildPlatformRuntime(boundedId);
        Map<String, Object> languages = buildLanguageRuntime(boundedId);
        Map<String, Object> timezone = buildTimezoneRuntime(boundedId);
        Map<String, Object> webgl = buildWebglRuntime(boundedId);
        Map<String, Object> canvas = buildCanvasRuntime(boundedId);
        Map<String, Object> fonts = buildFontRuntime(boundedId);
        Map<String, Object> media = buildMediaDeviceRuntime(boundedId);
        Map<String, Object> navigator = buildNavigatorRuntime(boundedId);

        Map<String, Object> mediaDevices = map();
        mediaDevices.put("audio_inputs", media.get("audio_inputs"));
        mediaDevices.put("video_inputs", media.get("video_inputs"));
        mediaDevices.put("audio_outputs", media.get("audio_outputs"));

        Map<String, Object> identity = map();
        identity.put("profile_id", boundedId);
        identity.put("user_agent", ua.get("user_agent"));
        identity.put("platform", platform.get("platform"));
        identity.put("languages", languages.get("languages"));
        identity.put("timezone", timezone.get("timezone"));
        identity.put("screen", screenFor(boundedId));
        identity.put("webgl", webgl);
        identity.put("fonts", fonts.get("fonts"));
        identity.put("media_devices", mediaDevices);
        identity.put("canvas_fingerprint", canvas.get("canvas_fingerprint"));
        identity.put("navigator", navigator);
        identity.put("rotation_index", profile.getOrDefault("rotation_index", 0L));
        identity.put("bounded", true);

        Map<String, Object> entropy = computeRuntimeEntropy(identity, null);
        identity.put("entropy_profile", entropy.get("baseline_hash"));
        identity.put("fingerprint_hash", fingerprintBrowserIdentity(identity));
        return identity;
    }

    // -------------------------------------------------------------- persistence (session envelope)

    /** {@code save_browser_identity(path, identity, key)}. */
    public static Map<String, Object> saveBrowserIdentity(String path, Map<String, Object> identity, String key) {
        Map<String, Object> encrypted = KaalkaSession.encryptSessionState(identity, key);
        Path target = Paths.get(path);
        try {
            Path parent = target.getParent();
            if (parent != null) {
                Files.createDirectories(parent);
            }
            Files.write(target, PyJson.dumpsDefaultAscii(encrypted).getBytes(StandardCharsets.UTF_8));
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        Map<String, Object> out = map();
        out.put("saved", true);
        out.put("path", target.toString());
        out.put("algorithm", "kaalka");
        out.put("bounded", true);
        return out;
    }

    /** {@code load_browser_identity(path, key)} — missing file rebuilds the default identity. */
    public static Map<String, Object> loadBrowserIdentity(String path, String key) {
        Path target = Paths.get(path);
        if (!Files.exists(target)) {
            Map<String, Object> out = map();
            out.put("available", false);
            out.put("identity", buildBrowserIdentity("default"));
            out.put("bounded", true);
            return out;
        }
        try {
            String content = new String(Files.readAllBytes(target), StandardCharsets.UTF_8);
            Map<String, Object> encrypted = asMap(PyJsonParse.loads(content));
            Map<String, Object> decrypted = KaalkaSession.decryptSessionState(encrypted, key);
            Map<String, Object> out = map();
            out.put("available", true);
            out.put("identity", decrypted.containsKey("session") ? decrypted.get("session") : map());
            out.put("algorithm", "kaalka");
            out.put("bounded", true);
            return out;
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }
}
