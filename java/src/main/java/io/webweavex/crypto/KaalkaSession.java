package io.webweavex.crypto;

import io.webweavex.determinism.PyJson;
import io.webweavex.determinism.PyJsonParse;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Kaalka session encryption — encrypts/decrypts session state.
 * Mirrors Python {@code core/crypto/kaalka_session_engine.py}.
 */
public final class KaalkaSession {
    private KaalkaSession() {}

    public static Map<String, Object> encryptSessionState(Map<String, Object> state, String key) {
        String json = PyJson.dumpsDefaultAscii(state);
        String encrypted = Kaalka.encryptValue(json, key);
        Map<String, Object> envelope = new LinkedHashMap<>();
        envelope.put("encrypted", encrypted);
        envelope.put("algorithm", Kaalka.KAALKA_ALGORITHM);
        envelope.put("deterministic", true);
        envelope.put("bounded", true);
        envelope.put("session", state);
        return envelope;
    }

    @SuppressWarnings("unchecked")
    public static Map<String, Object> decryptSessionState(Map<String, Object> envelope, String key) {
        String encrypted = (String) envelope.get("encrypted");
        if (encrypted == null) {
            return envelope;
        }
        String decrypted = Kaalka.decryptValue(encrypted, key);
        Object state;
        try {
            state = PyJsonParse.loads(decrypted);
        } catch (Exception e) {
            state = decrypted;
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("session", state);
        return out;
    }
}
