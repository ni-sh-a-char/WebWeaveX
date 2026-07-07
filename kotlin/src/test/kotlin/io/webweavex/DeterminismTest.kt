package io.webweavex

import io.webweavex.determinism.StableSerialize
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Test

/**
 * Smallest possible check on [StableSerialize]: if canonical serialization
 * breaks (sort order, float collapse, or NFC normalization), these fail
 * before any cross-language vector comparison does.
 */
class DeterminismTest {

    @Test
    fun `map keys serialize sorted by code point`() {
        val value = linkedMapOf("b" to 1, "a" to 2)
        assertEquals("""{"a":2,"b":1}""", StableSerialize.stableSerialize(value))
    }

    @Test
    fun `integral float collapses to a bare integer`() {
        assertEquals("0", StableSerialize.stableSerialize(0.0))
        assertEquals("2", StableSerialize.stableSerialize(2.0))
    }

    @Test
    fun `strings are NFC-normalized before serialization`() {
        // "e" + combining acute accent (NFD) must canonicalize to precomposed U+00E9.
        val decomposed = "é"
        assertEquals("é", StableSerialize.stableSerialize(decomposed))
    }
}
