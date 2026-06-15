package io.webweavex.crypto;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.webweavex.determinism.StableSerialize;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import org.junit.jupiter.api.Test;

/** Direct unit coverage for crypto branches not exercised by golden vectors. */
class CryptoUnitTest {

    @Test
    void hashMatchesPlainSha256ForStrings() {
        // stableSerialize("hello") == "hello" → sha256("hello").
        assertEquals("2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
                Hashing.computeDeterministicHash("hello"));
        assertEquals(Hashing.computeDeterministicHash("hello"),
                Kaalka.computeKaalkaHash("hello"));
    }

    @Test
    void encryptDecryptRoundTripsArbitraryValue() {
        Object value = Map.of("a", 1, "b", java.util.List.of(2, 3), "c", "café");
        String key = "round-trip-key";
        String ct = Kaalka.encryptValue(value, key);
        assertEquals(StableSerialize.stableSerialize(value), Kaalka.decryptValue(ct, key));
    }

    @Test
    void envelopesCarryAlgorithmMetadata() {
        Map<String, Object> enc = Kaalka.encryptValueEnvelope(Map.of("k", "v"), "secret");
        assertEquals("webweavex-formula+kaalka@5.0.0", enc.get("algorithm"));
        assertEquals(Boolean.TRUE, enc.get("deterministic"));
        assertEquals(Boolean.TRUE, enc.get("bounded"));

        Map<String, Object> dec =
                Kaalka.decryptValueEnvelope((String) enc.get("encrypted"), "secret");
        assertEquals("{\"k\":\"v\"}", dec.get("decrypted"));
        assertEquals("webweavex-formula+kaalka@5.0.0", dec.get("algorithm"));
    }

    @Test
    void timeKeyParsingHandlesAllPartCounts() {
        assertArrayEquals(new int[] {7, 4, 13}, KaalkaV5Proc.parseKaalkaTimeKey("7:4:13"));
        // Hours fold mod 12.
        assertArrayEquals(new int[] {1, 4, 13}, KaalkaV5Proc.parseKaalkaTimeKey("13:4:13"));
        // Two-part → minutes:seconds; one-part → seconds.
        assertArrayEquals(new int[] {0, 4, 13}, KaalkaV5Proc.parseKaalkaTimeKey("4:13"));
        assertArrayEquals(new int[] {0, 0, 13}, KaalkaV5Proc.parseKaalkaTimeKey("13"));
    }

    @Test
    void procIsZeroSecondsSafe() {
        // key folds to 1 when seconds == 0, so encrypt/decrypt still round-trip.
        byte[] data = "data".getBytes(StandardCharsets.UTF_8);
        byte[] enc = KaalkaV5Proc.encryptBytes(data, "0:0:0");
        assertArrayEquals(data, KaalkaV5Proc.decryptBytes(enc, "0:0:0"));
    }

    @Test
    void deriveTimeKeyIsDeterministicAndRoundTrips() {
        String tk1 = TimeKey.deriveKaalkaTimeKey("my-key");
        String tk2 = TimeKey.deriveKaalkaTimeKey("my-key");
        assertEquals(tk1, tk2);
        assertTrue(TimeKey.kaalkaTimeKeyRoundTrips(tk1));
        // Format HH:MM:SS.
        assertTrue(tk1.matches("\\d+:\\d+:\\d+"));
    }
}
