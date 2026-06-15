package io.webweavex.crypto;

import io.webweavex.determinism.StableSerialize;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/**
 * Deterministic hashing — {@code sha256(utf8(stableSerialize(value)))} rendered
 * as lowercase hex. Byte-identical to Python {@code compute_deterministic_hash}
 * ({@code core/crypto/kaalka_runtime_engine.py}), which is exported as
 * {@code compute_kaalka_hash}, and to the Dart {@code computeDeterministicHash}.
 */
public final class Hashing {

    private Hashing() {
    }

    public static String computeDeterministicHash(Object value) {
        String payload = StableSerialize.stableSerialize(value);
        return sha256Hex(payload.getBytes(StandardCharsets.UTF_8));
    }

    public static String sha256Hex(byte[] data) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(data);
            StringBuilder sb = new StringBuilder(hash.length * 2);
            for (byte b : hash) {
                sb.append(Character.forDigit((b >> 4) & 0xF, 16));
                sb.append(Character.forDigit(b & 0xF, 16));
            }
            return sb.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new IllegalStateException("SHA-256 unavailable", e);
        }
    }
}
