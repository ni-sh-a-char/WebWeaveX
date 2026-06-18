package io.webweavex.crypto;

import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyJson;
import io.webweavex.determinism.PyJsonParse;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Port of {@code core.crypto.kaalka_session_engine} — {@code encrypt_session_state} /
 * {@code decrypt_session_state}. Deterministic session-state encryption built on the certified
 * {@link Kaalka} envelope and the {@link PyJson}/{@link PyJsonParse} {@code json.dumps}/
 * {@code json.loads} substrate. No filesystem, no network. Dependency-clean.
 */
public final class KaalkaSession {

    private KaalkaSession() {
    }

    private static final int MAX_SESSION_BYTES = 10_000_000;

    /** {@code encrypt_session_state(session, key)}. */
    public static Map<String, Object> encryptSessionState(Map<String, Object> session, String key) {
        // json.dumps(session, sort_keys=True, separators=(",",":"), ensure_ascii=False)[:MAX]
        String serialized = clip(PyJson.dumpsCompactUnicode(session));
        Map<String, Object> encrypted = Kaalka.encryptValueEnvelope(serialized, key);
        Map<String, Object> out = new LinkedHashMap<>(encrypted);
        out.put("payload_type", "session");
        out.put("bounded", true);
        return out;
    }

    /** {@code decrypt_session_state(payload, key)}. */
    public static Map<String, Object> decryptSessionState(Map<String, Object> payload, String key) {
        String ciphertext = Py.str(Py.get(payload, "encrypted", ""));
        Map<String, Object> decrypted = Kaalka.decryptValueEnvelope(ciphertext, key);
        String text = clip(Py.str(Py.get(decrypted, "decrypted", "")));
        Object session = PyJsonParse.loads(text);

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("session", session);
        out.put("algorithm", "kaalka");
        out.put("deterministic", true);
        out.put("bounded", true);
        return out;
    }

    private static String clip(String s) {
        return s.length() > MAX_SESSION_BYTES ? s.substring(0, MAX_SESSION_BYTES) : s;
    }
}
