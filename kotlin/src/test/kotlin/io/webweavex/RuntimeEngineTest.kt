package io.webweavex

import io.webweavex.runtime.*
import io.webweavex.fingerprint.Fingerprint
import io.webweavex.serialization.CanonicalSerialization
import io.webweavex.determinism.StableSerialize
import io.webweavex.graph.RuntimeGraph
import io.webweavex.repository.RepositoryAnalyzer
import io.webweavex.exceptions.*
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue
import kotlin.test.assertNotNull

class RuntimeEngineTest {
    @Test
    fun `runtime kernel creates successfully`() {
        val kernel = RuntimeKernel.create()
        assertEquals("3.0.0", kernel.version)
        assertTrue(kernel.capabilities.contains("extraction"))
        assertTrue(kernel.capabilities.contains("fingerprinting"))
    }

    @Test
    fun `universal input and output work`() {
        val input = UniversalInput(source = "test input")
        val kernel = RuntimeKernel.create()
        val output = kernel.extract(input)
        assertTrue(output.isValid())
        assertEquals("3.0.0", output.version)
        assertTrue(output.fingerprint.isNotEmpty())
    }

    @Test
    fun `canonical serialization is deterministic`() {
        val data = mapOf("b" to 2, "a" to 1)
        val s1 = CanonicalSerialization.serialize(data)
        val s2 = CanonicalSerialization.serialize(data)
        assertEquals(s1, s2)
        assertEquals("""{"a":1,"b":2}""", s1)
    }

    @Test
    fun `fingerprint is deterministic`() {
        val data = mapOf("key" to "value")
        val h1 = Fingerprint.compute(data)
        val h2 = Fingerprint.compute(data)
        assertEquals(h1, h2)
        assertEquals(64, h1.length)
    }

    @Test
    fun `fingerprint is stable across key orders`() {
        val a = Fingerprint.compute(mapOf("z" to 1, "a" to 2))
        val b = Fingerprint.compute(mapOf("a" to 2, "z" to 1))
        assertEquals(a, b)
    }

    @Test
    fun `runtime graph normalizes correctly`() {
        val graph = RuntimeGraph(
            nodes = listOf(mapOf("id" to "2"), mapOf("id" to "1")),
            edges = listOf(mapOf("from" to "1", "to" to "2"))
        )
        val normalized = graph.normalize()
        assertEquals("1", normalized.nodes[0]["id"])
        assertEquals("2", normalized.nodes[1]["id"])
    }

    @Test
    fun `runtime snapshot creation`() {
        val nodes = listOf(mapOf("id" to "n1"))
        val edges = listOf(mapOf("from" to "n1", "to" to "n1"))
        val meta = RuntimeMetadata(source = "test")
        val snapshot = RuntimeSnapshot.create(nodes, edges, meta)
        assertTrue(snapshot.fingerprint.isNotEmpty())
        assertTrue(snapshot.timestamp > 0)
    }

    @Test
    fun `repository analyzer works`() {
        val text = "import flask\nGET /api/users\nPOST /api/users"
        val result = RepositoryAnalyzer.analyze(text)
        assertTrue(result.dependencies.isNotEmpty())
        assertTrue(result.apiRoutes.isNotEmpty())
        assertTrue(result.fingerprint.isNotEmpty())
    }

    @Test
    fun `exceptions are properly structured`() {
        val e = ValidationException("test error")
        assertEquals("VALIDATION_ERROR", e.code)
        assertEquals("test error", e.message)
    }

    @Test
    fun `runtime config has correct defaults`() {
        val config = RuntimeConfig()
        assertTrue(config.deterministic)
        assertTrue(config.stableOrdering)
        assertTrue(config.canonicalSerialization)
    }

    @Test
    fun `runtime metadata works`() {
        val meta = RuntimeMetadata(source = "test", version = "3.0.0")
        val map = meta.toMap()
        assertEquals("test", map["source"])
        assertEquals("3.0.0", map["version"])
    }

    @Test
    fun `runtime snapshot fingerprint is stable`() {
        val nodes = listOf(mapOf("id" to "n1"))
        val edges = listOf(mapOf("from" to "n1", "to" to "n1"))
        val meta = RuntimeMetadata()
        val s1 = RuntimeSnapshot.create(nodes, edges, meta)
        val s2 = RuntimeSnapshot.create(nodes, edges, meta)
        assertEquals(s1.fingerprint, s2.fingerprint)
    }
}
