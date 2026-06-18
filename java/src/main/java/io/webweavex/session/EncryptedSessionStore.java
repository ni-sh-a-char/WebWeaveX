package io.webweavex.session;

import io.webweavex.crypto.KaalkaSession;
import io.webweavex.determinism.PyJson;
import io.webweavex.determinism.PyJsonParse;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Port of {@code core.session.encrypted_session_store} — {@code save_encrypted_session} /
 * {@code load_encrypted_session}. Filesystem-backed roundtrip persistence over the
 * {@link KaalkaSession} engine. The written file content is byte-identical to canonical Python
 * ({@code json.dumps(payload, sort_keys=True)}); the recovered session is byte-identical via the
 * {@link PyJsonParse} {@code json.loads} substrate.
 */
public final class EncryptedSessionStore {

    private EncryptedSessionStore() {
    }

    /** {@code save_encrypted_session(path, session, key)}. */
    public static Map<String, Object> saveEncryptedSession(
            String path, Map<String, Object> session, String key) {
        Map<String, Object> payload = KaalkaSession.encryptSessionState(session, key);
        Path target = Paths.get(path);
        try {
            Path parent = target.getParent();
            if (parent != null) {
                Files.createDirectories(parent);
            }
            // json.dumps(payload, sort_keys=True) -> default separators (", ", ": "), ascii
            Files.write(target, PyJson.dumpsDefaultAscii(payload).getBytes(StandardCharsets.UTF_8));
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("saved", true);
        out.put("path", target.toString());
        out.put("algorithm", "kaalka");
        out.put("bounded", true);
        return out;
    }

    /** {@code load_encrypted_session(path, key)}. */
    @SuppressWarnings("unchecked")
    public static Map<String, Object> loadEncryptedSession(String path, String key) {
        Path target = Paths.get(path);
        if (!Files.exists(target)) {
            return unavailableFull();
        }
        Object payload;
        try {
            String content = new String(Files.readAllBytes(target), StandardCharsets.UTF_8);
            payload = PyJsonParse.loads(content);
        } catch (RuntimeException | IOException exc) {
            return unavailableShort(exc);
        }
        Map<String, Object> decrypted =
                KaalkaSession.decryptSessionState((Map<String, Object>) payload, key);

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("available", true);
        Object session = decrypted.containsKey("session") ? decrypted.get("session") : new LinkedHashMap<>();
        out.put("session", session);
        out.put("algorithm", "kaalka");
        out.put("bounded", true);
        return out;
    }

    /** Missing-file default — full empty session shape. */
    private static Map<String, Object> unavailableFull() {
        Map<String, Object> session = new LinkedHashMap<>();
        session.put("cookies", new ArrayList<>());
        session.put("headers", new LinkedHashMap<>());
        session.put("auth_tokens", new ArrayList<>());
        session.put("local_storage", new LinkedHashMap<>());
        session.put("session_storage", new LinkedHashMap<>());
        session.put("authenticated", false);
        session.put("bounded", true);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("available", false);
        out.put("session", session);
        out.put("bounded", true);
        return out;
    }

    /** Corrupt-file default — short empty session shape + reason. */
    private static Map<String, Object> unavailableShort(Exception exc) {
        Map<String, Object> session = new LinkedHashMap<>();
        session.put("cookies", new ArrayList<>());
        session.put("headers", new LinkedHashMap<>());
        session.put("auth_tokens", new ArrayList<>());
        session.put("bounded", true);
        String reason = String.valueOf(exc.getMessage());
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("available", false);
        out.put("reason", reason.length() > 200 ? reason.substring(0, 200) : reason);
        out.put("session", session);
        out.put("bounded", true);
        return out;
    }
}
