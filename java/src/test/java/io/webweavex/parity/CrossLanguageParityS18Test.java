package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.identity.IdentityRuntime;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;
import org.junit.jupiter.api.io.TempDir;

/**
 * Session-18 cross-language parity: the {@code core.identity} family
 * (io.webweavex.identity.IdentityRuntime) — the browser-identity orchestrator + its ~11
 * fingerprint engines + the save/load persistence pair — is byte-identical to canonical
 * Python 2.1.0 ({@code golden_vectors_s18.json}) via {@code stable_serialize} +
 * {@code compute_kaalka_hash}.
 */
class CrossLanguageParityS18Test {

    @TempDir
    Path tempDir;

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS18Test.class
                .getResourceAsStream("/parity/golden_vectors_s18.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s18.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s18 golden vectors", e);
        }
    }

    private List<DynamicTest> section(String name, Function<JsonNode, Object> fn) {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get(name)) {
            tests.add(DynamicTest.dynamicTest(name + ":" + v.get("name").asText(), () -> {
                Object output = fn.apply(v.get("inputs"));
                assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(output));
                assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(output));
            }));
        }
        return tests;
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> m(JsonNode in, String f) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? null : (Map<String, Object>) CrossLanguageParityTest.toNative(n);
    }

    private static String s(JsonNode in, String f, String d) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? d : n.asText();
    }

    // ---- orchestrator + engine sections (profile-parameterized) ----

    @TestFactory
    List<DynamicTest> identityAndEngines() {
        List<DynamicTest> t = new ArrayList<>();
        t.addAll(section("build_browser_identity", in -> IdentityRuntime.buildBrowserIdentity(s(in, "profile_id", "default"))));
        t.addAll(section("build_browser_profile", in -> IdentityRuntime.buildBrowserProfile(s(in, "profile_id", "default"))));
        t.addAll(section("build_user_agent_runtime", in -> IdentityRuntime.buildUserAgentRuntime(s(in, "profile_id", "default"))));
        t.addAll(section("build_platform_runtime", in -> IdentityRuntime.buildPlatformRuntime(s(in, "profile_id", "default"))));
        t.addAll(section("build_language_runtime", in -> IdentityRuntime.buildLanguageRuntime(s(in, "profile_id", "default"))));
        t.addAll(section("build_timezone_runtime", in -> IdentityRuntime.buildTimezoneRuntime(s(in, "profile_id", "default"))));
        t.addAll(section("build_webgl_runtime", in -> IdentityRuntime.buildWebglRuntime(s(in, "profile_id", "default"))));
        t.addAll(section("build_canvas_runtime", in -> IdentityRuntime.buildCanvasRuntime(s(in, "profile_id", "default"))));
        t.addAll(section("build_font_runtime", in -> IdentityRuntime.buildFontRuntime(s(in, "profile_id", "default"))));
        t.addAll(section("build_media_device_runtime", in -> IdentityRuntime.buildMediaDeviceRuntime(s(in, "profile_id", "default"))));
        t.addAll(section("build_navigator_runtime", in -> IdentityRuntime.buildNavigatorRuntime(s(in, "profile_id", "default"))));
        t.addAll(section("compute_runtime_entropy", in -> IdentityRuntime.computeRuntimeEntropy(
                m(in, "identity"), m(in, "observed"))));
        t.addAll(section("normalize_browser_fingerprint", in -> IdentityRuntime.normalizeBrowserFingerprint(
                m(in, "identity"))));
        t.addAll(section("fingerprint_browser_identity", in -> {
            Map<String, Object> wrap = new LinkedHashMap<>();
            wrap.put("fingerprint_hash", IdentityRuntime.fingerprintBrowserIdentity(m(in, "identity")));
            return wrap;
        }));
        return t;
    }

    // ---- persistence ----

    @TestFactory
    List<DynamicTest> saveBrowserIdentity() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("save_browser_identity")) {
            tests.add(DynamicTest.dynamicTest("save:" + v.get("name").asText(), () -> {
                JsonNode in = v.get("inputs");
                Path target = tempDir.resolve(in.get("filename").asText());
                Map<String, Object> ret = IdentityRuntime.saveBrowserIdentity(
                        target.toString(), m(in, "identity"), in.get("key").asText());
                String written = new String(Files.readAllBytes(target), StandardCharsets.UTF_8);
                assertEquals(v.get("file_content").asText(), written);
                assertEquals(true, ret.get("saved"));
                assertEquals("kaalka", ret.get("algorithm"));
            }));
        }
        return tests;
    }

    @TestFactory
    List<DynamicTest> loadBrowserIdentity() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("load_browser_identity")) {
            tests.add(DynamicTest.dynamicTest("load:" + v.get("name").asText(), () -> {
                Map<String, Object> out;
                if (v.has("missing") && v.get("missing").asBoolean()) {
                    out = IdentityRuntime.loadBrowserIdentity(
                            tempDir.resolve("nope.json").toString(), v.get("key").asText());
                } else {
                    Path target = tempDir.resolve(v.get("name").asText() + ".json");
                    Files.write(target, v.get("file_content").asText().getBytes(StandardCharsets.UTF_8));
                    out = IdentityRuntime.loadBrowserIdentity(target.toString(), v.get("key").asText());
                }
                assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(out));
                assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(out));
            }));
        }
        return tests;
    }
}
