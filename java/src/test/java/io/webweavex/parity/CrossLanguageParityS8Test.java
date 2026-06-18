package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.crypto.KaalkaSession;
import io.webweavex.determinism.PyJsonParse;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.session.EncryptedSessionStore;
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
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestFactory;
import org.junit.jupiter.api.io.TempDir;

/**
 * Session-8 cross-language parity: the session-crypto cluster (encrypt/decrypt_session_state,
 * save/load_encrypted_session) and the {@code json.loads} substrate are byte-identical to
 * canonical Python 2.1.0 ({@code golden_vectors_s8.json}). encrypt/decrypt assert
 * {@code stable_serialize} + {@code compute_kaalka_hash}; save asserts the written file content
 * (Python-recorded) byte-for-byte; load asserts the recovered output serialize+hash.
 */
class CrossLanguageParityS8Test {

    @TempDir
    Path tempDir;

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS8Test.class
                .getResourceAsStream("/parity/golden_vectors_s8.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s8.json not on classpath");
            }
            // canonical Python json.dump emits non-standard Infinity/NaN tokens (sess_nonfinite)
            ObjectMapper mapper = new ObjectMapper()
                    .configure(JsonParser.Feature.ALLOW_NON_NUMERIC_NUMBERS, true);
            return mapper.readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s8 golden vectors", e);
        }
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> mapField(JsonNode inputs, String field) {
        JsonNode n = inputs.get(field);
        if (n == null || n.isNull()) {
            return null;
        }
        return (Map<String, Object>) CrossLanguageParityTest.toNative(n);
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

    @TestFactory
    List<DynamicTest> encryptSessionState() {
        return section("encrypt_session_state", in -> KaalkaSession.encryptSessionState(
                mapField(in, "session"), in.get("key").asText()));
    }

    @TestFactory
    List<DynamicTest> decryptSessionState() {
        return section("decrypt_session_state", in -> KaalkaSession.decryptSessionState(
                mapField(in, "payload"), in.get("key").asText()));
    }

    @TestFactory
    List<DynamicTest> saveEncryptedSession() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("save_encrypted_session")) {
            tests.add(DynamicTest.dynamicTest("save:" + v.get("name").asText(), () -> {
                JsonNode in = v.get("inputs");
                Path target = tempDir.resolve(in.get("filename").asText());
                Map<String, Object> ret = EncryptedSessionStore.saveEncryptedSession(
                        target.toString(), mapField(in, "session"), in.get("key").asText());
                // file content byte-identical to canonical Python (json.dumps(payload, sort_keys=True))
                String written = new String(Files.readAllBytes(target), StandardCharsets.UTF_8);
                assertEquals(v.get("file_content").asText(), written);
                // structural return (path is environment-specific -> equals what we passed)
                assertEquals(true, ret.get("saved"));
                assertEquals("kaalka", ret.get("algorithm"));
                assertEquals(true, ret.get("bounded"));
                assertEquals(target.toString(), ret.get("path"));
            }));
        }
        return tests;
    }

    @TestFactory
    List<DynamicTest> jsonLoadsSubstrate() {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("json_loads")) {
            String text = v.get("text").asText();
            String nm = v.get("name").asText();
            if (v.get("error").asBoolean()) {
                tests.add(DynamicTest.dynamicTest("json_loads:" + nm,
                        () -> assertThrows(RuntimeException.class, () -> PyJsonParse.loads(text))));
            } else {
                tests.add(DynamicTest.dynamicTest("json_loads:" + nm, () -> {
                    Object out = PyJsonParse.loads(text);
                    assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(out));
                    assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(out));
                }));
            }
        }
        return tests;
    }

    /** Corrupt-file branch: Python returns {available:false, short session, reason}; the reason
     * string is environment-specific so only the deterministic contract is asserted. */
    @Test
    void loadCorruptFileContract() throws Exception {
        Path target = tempDir.resolve("corrupt.json");
        Files.write(target, "{not valid json".getBytes(StandardCharsets.UTF_8));
        Map<String, Object> out = EncryptedSessionStore.loadEncryptedSession(target.toString(), "k");
        assertEquals(false, out.get("available"));
        assertEquals(true, out.get("bounded"));
        assertNotNull(out.get("reason"));
        @SuppressWarnings("unchecked")
        Map<String, Object> session = (Map<String, Object>) out.get("session");
        assertEquals(new ArrayList<>(), session.get("cookies"));
        assertEquals(new LinkedHashMap<>(), session.get("headers"));
        assertEquals(new ArrayList<>(), session.get("auth_tokens"));
        assertEquals(true, session.get("bounded"));
    }

    @TestFactory
    List<DynamicTest> loadEncryptedSession() throws Exception {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get("load_encrypted_session")) {
            tests.add(DynamicTest.dynamicTest("load:" + v.get("name").asText(), () -> {
                Map<String, Object> out;
                if (v.has("missing") && v.get("missing").asBoolean()) {
                    out = EncryptedSessionStore.loadEncryptedSession(
                            tempDir.resolve("does_not_exist.json").toString(), v.get("key").asText());
                } else {
                    Path target = tempDir.resolve(v.get("name").asText() + ".json");
                    Files.write(target, v.get("file_content").asText().getBytes(StandardCharsets.UTF_8));
                    out = EncryptedSessionStore.loadEncryptedSession(target.toString(), v.get("key").asText());
                }
                assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(out));
                assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(out));
            }));
        }
        return tests;
    }
}
