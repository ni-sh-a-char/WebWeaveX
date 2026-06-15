package io.webweavex.crypto;

import io.webweavex.determinism.StableSerialize;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Public Kaalka cryptography facade — the WebWeaveX &rarr; Kaalka v5 adapter.
 * Mirrors Python {@code core/crypto/kaalka_runtime_engine.py} and the Dart
 * {@code kaalka_runtime.dart}.
 *
 * <p>Contract:
 * {@code normalizeRuntimeValue} &rarr; {@code stableSerialize} &rarr; UTF-8
 * &rarr; {@code deriveKaalkaTimeKey} &rarr; Kaalka v5 byte {@code _proc} &rarr;
 * base64.
 */
public final class Kaalka {

    private Kaalka() {
    }

    public static final String KAALKA_ALGORITHM = "webweavex-formula+kaalka@5.0.0";
    public static final String KAALKA_NPM_VERSION = "5.0.0";

    /** Deterministic content hash (alias of {@link Hashing#computeDeterministicHash}). */
    public static String computeKaalkaHash(Object value) {
        return Hashing.computeDeterministicHash(value);
    }

    /** Encrypts a canonical runtime value to base64 ciphertext (Kaalka v5 byte path). */
    public static String encryptValue(Object value, String key) {
        String payload = StableSerialize.stableSerialize(value);
        String timeKey = TimeKey.deriveKaalkaTimeKey(key);
        byte[] raw = KaalkaV5Proc.encryptBytes(
                payload.getBytes(StandardCharsets.UTF_8), timeKey);
        return Base64.getEncoder().encodeToString(raw);
    }

    /** Decrypts base64 ciphertext back to the canonical serialized string. */
    public static String decryptValue(String encrypted, String key) {
        String timeKey = TimeKey.deriveKaalkaTimeKey(key);
        byte[] raw = Base64.getDecoder().decode(encrypted);
        byte[] decrypted = KaalkaV5Proc.decryptBytes(raw, timeKey);
        return new String(decrypted, StandardCharsets.UTF_8);
    }

    /** Encryption envelope matching the Python/Dart {@code encrypt_value} dict. */
    public static Map<String, Object> encryptValueEnvelope(Object value, String key) {
        Map<String, Object> env = new LinkedHashMap<>();
        env.put("encrypted", encryptValue(value, key));
        env.put("algorithm", KAALKA_ALGORITHM);
        env.put("deterministic", true);
        env.put("bounded", true);
        return env;
    }

    /** Decryption envelope matching the Python/Dart {@code decrypt_value} dict. */
    public static Map<String, Object> decryptValueEnvelope(String encrypted, String key) {
        Map<String, Object> env = new LinkedHashMap<>();
        env.put("decrypted", decryptValue(encrypted, key));
        env.put("algorithm", KAALKA_ALGORITHM);
        env.put("deterministic", true);
        env.put("bounded", true);
        return env;
    }
}
