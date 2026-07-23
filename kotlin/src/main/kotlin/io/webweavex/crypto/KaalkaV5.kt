package io.webweavex.crypto

import java.util.Base64

/**
 * Kaalka v5 deterministic encryption � faithful Kotlin implementation
 * of the canonical algorithm from Python/Dart.
 *
 * Algorithm: byte-level XOR-add offset transform
 *   offset = (clock + index) % 256
 *   encrypt: (byte + offset) % 256
 *   decrypt: (byte - offset + 256) % 256
 *
 * Cross-language guaranteed: outputs byte-identical to Python and Dart.
 */
object KaalkaV5 {

    const val ALGORITHM = "webweavex-formula+kaalka@5.0.0"
    const val PACKAGE_VERSION = "5.0.0"
    const val FALLBACK_TIME_KEY = "12:0:0"
    private val ROUNDTRIP_PROBE = "\u0000\u007f\ufffd\ud83d\ude80probe".toByteArray(Charsets.UTF_8)

    /**
     * Parse time key string (HH:MM:SS) into (hours, minutes, seconds).
     */
    fun parseTimeKey(timeKey: String): Triple<Int, Int, Int> {
        val parts = timeKey.split(":")
        return when (parts.size) {
            3 -> Triple(parts[0].toInt() % 12, parts[1].toInt(), parts[2].toInt())
            2 -> Triple(0, parts[0].toInt(), parts[1].toInt())
            1 -> Triple(0, 0, if (parts[0].isNotEmpty()) parts[0].toInt() else 0)
            else -> Triple(0, 0, 0)
        }
    }

    /**
     * Core Kaalka v5 byte transform.
     */
    fun proc(data: ByteArray, encrypt: Boolean, timeKey: String): ByteArray {
        val (h, m, s) = parseTimeKey(timeKey)
        val clock = (h * 3600 + m * 60 + s).let { if (it == 0) 1 else it }
        val result = ByteArray(data.size)
        for (idx in data.indices) {
            val offset = (clock + idx) % 256
            result[idx] = if (encrypt) {
                ((data[idx].toInt() and 0xFF) + offset).toByte()
            } else {
                ((data[idx].toInt() and 0xFF) - offset + 256).toByte()
            }
        }
        return result
    }

    /**
     * Check if a time key produces valid round-trips.
     */
    fun timeKeyRoundTrips(timeKey: String): Boolean {
        return try {
            val enc = proc(ROUNDTRIP_PROBE, true, timeKey)
            val dec = proc(enc, false, timeKey)
            dec.contentEquals(ROUNDTRIP_PROBE)
        } catch (e: Exception) {
            false
        }
    }

    /**
     * Derive deterministic time key from encryption key.
     * Matches Python derive_kaalka_time_key and Dart deriveKaalkaTimeKey.
     */
    fun deriveTimeKey(encryptionKey: String): String {
        val normalized = io.webweavex.determinism.Normalization.normalizeRuntimeValue(encryptionKey)
        val digest = java.security.MessageDigest.getInstance("SHA-256")
            .digest(normalized.toByteArray(Charsets.UTF_8))
        for (i in 0..digest.size - 3) {
            val candidate = "${(digest[i].toInt() and 0xFF) % 12}:${(digest[i + 1].toInt() and 0xFF) % 60}:${(digest[i + 2].toInt() and 0xFF) % 60}"
            if (timeKeyRoundTrips(candidate)) return candidate
        }
        if (timeKeyRoundTrips(FALLBACK_TIME_KEY)) return FALLBACK_TIME_KEY
        return "12:34:56"
    }

    /**
     * Encrypt bytes with Kaalka v5.
     */
    fun encrypt(data: ByteArray, timeKey: String): ByteArray = proc(data, true, timeKey)

    /**
     * Decrypt bytes with Kaalka v5.
     */
    fun decrypt(data: ByteArray, timeKey: String): ByteArray = proc(data, false, timeKey)

    /**
     * Encrypt value ? base64 ciphertext.
     * Matches Python encrypt_bytes and Dart encryptValue.
     */
    fun encryptValue(value: Any?, key: String): Map<String, Any> {
        val payload = io.webweavex.determinism.StableSerialize.stableSerialize(value)
            .toByteArray(Charsets.UTF_8)
        val timeKey = deriveTimeKey(key)
        val encrypted = encrypt(payload, timeKey)
        return mapOf(
            "encrypted" to Base64.getEncoder().encodeToString(encrypted),
            "algorithm" to ALGORITHM,
            "deterministic" to true,
            "bounded" to true
        )
    }

    /**
     * Decrypt base64 ciphertext ? value.
     * Matches Python decrypt_bytes and Dart decryptValue.
     */
    fun decryptValue(ciphertext: String, key: String): Map<String, Any> {
        val timeKey = deriveTimeKey(key)
        val raw = Base64.getDecoder().decode(ciphertext)
        val decrypted = decrypt(raw, timeKey)
        val text = String(decrypted, Charsets.UTF_8)
        return mapOf(
            "decrypted" to text,
            "algorithm" to ALGORITHM,
            "deterministic" to true,
            "bounded" to true
        )
    }
}
