package io.webweavex.crypto

import io.webweavex.fingerprint.Fingerprint
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class KaalkaTest {

    @Test
    fun `kaalka v5 proc encrypt and decrypt round-trip`() {
        val data = "Hello, World!".toByteArray(Charsets.UTF_8)
        val enc = KaalkaV5.proc(data, true, "12:0:0")
        val dec = KaalkaV5.proc(enc, false, "12:0:0")
        assertTrue(data.contentEquals(dec))
    }

    @Test
    fun `kaalka v5 proc is deterministic`() {
        val data = "test data".toByteArray(Charsets.UTF_8)
        val enc1 = KaalkaV5.proc(data, true, "12:0:0")
        val enc2 = KaalkaV5.proc(data, true, "12:0:0")
        assertTrue(enc1.contentEquals(enc2))
    }

    @Test
    fun `kaalka v5 proc produces different output for different time keys`() {
        val data = "test data with enough bytes to see difference".toByteArray(Charsets.UTF_8)
        val enc1 = KaalkaV5.proc(data, true, "12:0:0")
        val enc2 = KaalkaV5.proc(data, true, "6:30:15")
        val differ = enc1.zip(enc2).count { (a, b) -> a != b }
        assertTrue(differ > 0, "Outputs should differ for different time keys")
    }

    @Test
    fun `parse time key 3 parts`() {
        val (h, m, s) = KaalkaV5.parseTimeKey("10:30:45")
        assertEquals(10, h)
        assertEquals(30, m)
        assertEquals(45, s)
    }

    @Test
    fun `parse time key 2 parts`() {
        val (h, m, s) = KaalkaV5.parseTimeKey("5:30")
        assertEquals(0, h)
        assertEquals(5, m)
        assertEquals(30, s)
    }

    @Test
    fun `parse time key 1 part`() {
        val (h, m, s) = KaalkaV5.parseTimeKey("45")
        assertEquals(0, h)
        assertEquals(0, m)
        assertEquals(45, s)
    }

    @Test
    fun `time key round trips`() {
        assertTrue(KaalkaV5.timeKeyRoundTrips("12:0:0"))
        assertTrue(KaalkaV5.timeKeyRoundTrips("0:0:1"))
        assertTrue(KaalkaV5.timeKeyRoundTrips("6:30:15"))
    }

    @Test
    fun `derive time key is deterministic`() {
        val key1 = KaalkaV5.deriveTimeKey("test-key")
        val key2 = KaalkaV5.deriveTimeKey("test-key")
        assertEquals(key1, key2)
    }

    @Test
    fun `derive time key differs by input`() {
        val key1 = KaalkaV5.deriveTimeKey("key-a")
        val key2 = KaalkaV5.deriveTimeKey("key-b")
        assertTrue(key1 != key2)
    }

    @Test
    fun `encrypt value produces correct structure`() {
        val result = KaalkaV5.encryptValue(mapOf("a" to 1), "test-key")
        assertTrue(result.containsKey("encrypted"))
        assertTrue(result.containsKey("algorithm"))
        assertEquals("webweavex-formula+kaalka@5.0.0", result["algorithm"])
        assertEquals(true, result["deterministic"])
        assertEquals(true, result["bounded"])
    }

    @Test
    fun `encrypt and decrypt round-trip`() {
        val original = mapOf("message" to "hello", "count" to 42)
        val encrypted = KaalkaV5.encryptValue(original, "test-key")
        val decrypted = KaalkaV5.decryptValue(encrypted["encrypted"] as String, "test-key")
        assertEquals("webweavex-formula+kaalka@5.0.0", decrypted["algorithm"])
        assertTrue((decrypted["decrypted"] as String).contains("hello"))
    }

    @Test
    fun `encrypt is deterministic across 1000 iterations`() {
        val data = mapOf("key" to "value")
        val first = KaalkaV5.encryptValue(data, "test")
        for (i in 1..999) {
            val result = KaalkaV5.encryptValue(data, "test")
            assertEquals(first["encrypted"], result["encrypted"])
        }
    }

    @Test
    fun `kaalka v5 proc handles empty data`() {
        val data = ByteArray(0)
        val enc = KaalkaV5.proc(data, true, "12:0:0")
        assertEquals(0, enc.size)
    }

    @Test
    fun `kaalka v5 proc handles large data`() {
        val data = ByteArray(100000) { (it % 256).toByte() }
        val enc = KaalkaV5.proc(data, true, "12:0:0")
        val dec = KaalkaV5.proc(enc, false, "12:0:0")
        assertTrue(data.contentEquals(dec))
    }

    @Test
    fun `kaalka v5 proc handles unicode bytes`() {
        val data = "\u4e16\u754c hello \u00e9\u00e8\u00ea".toByteArray(Charsets.UTF_8)
        val enc = KaalkaV5.proc(data, true, "12:0:0")
        val dec = KaalkaV5.proc(enc, false, "12:0:0")
        assertTrue(data.contentEquals(dec))
    }

    @Test
    fun `graph fingerprint is deterministic`() {
        val graph = mapOf("nodes" to listOf(mapOf("id" to "n1")), "edges" to emptyList<Any>())
        val fp1 = Fingerprint.graphFingerprint(graph)
        val fp2 = Fingerprint.graphFingerprint(graph)
        assertTrue(fp1.contentEquals(fp2))
    }

    @Test
    fun `graph fingerprint differs by content`() {
        val g1 = mapOf("nodes" to listOf(mapOf("id" to "n1")))
        val g2 = mapOf("nodes" to listOf(mapOf("id" to "n2")))
        val fp1 = Fingerprint.graphFingerprint(g1)
        val fp2 = Fingerprint.graphFingerprint(g2)
        assertTrue(!fp1.contentEquals(fp2))
    }

    @Test
    fun `cross-language parity - stable serialize key ordering`() {
        val data = mapOf("z" to 1, "a" to 2)
        val serialized = io.webweavex.determinism.StableSerialize.stableSerialize(data)
        assertTrue(serialized.contains("\"a\":2"))
        assertTrue(serialized.contains("\"z\":1"))
        val aIdx = serialized.indexOf("\"a\"")
        val zIdx = serialized.indexOf("\"z\"")
        assertTrue(aIdx < zIdx)
    }
}
