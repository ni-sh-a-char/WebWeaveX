package io.webweavex.replay

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertTrue

class ReplayEquivalenceTest {

    private fun envelope(graph: Map<String, Any>): Map<String, Any> {
        return linkedMapOf(
            "unified_runtime_graph" to graph,
            "pipeline_hash" to "test_hash",
            "bounded" to true
        )
    }

    @Test
    fun `identical envelopes are equivalent`() {
        val graph = linkedMapOf<String, Any>(
            "nodes" to listOf(linkedMapOf("id" to "n1", "type" to "file")),
            "edges" to emptyList<Any>()
        )
        val result = ReplayEquivalence.validate(envelope(graph), envelope(graph))
        assertTrue(result["equivalent"] as Boolean)
        assertTrue(result["bounded"] as Boolean)
    }

    @Test
    fun `different graphs are not equivalent`() {
        val g1 = linkedMapOf<String, Any>("nodes" to listOf(linkedMapOf("id" to "n1")), "edges" to emptyList<Any>())
        val g2 = linkedMapOf<String, Any>("nodes" to listOf(linkedMapOf("id" to "n2")), "edges" to emptyList<Any>())
        val result = ReplayEquivalence.validate(envelope(g1), envelope(g2))
        assertFalse(result["equivalent"] as Boolean)
    }

    @Test
    fun `graph hash is deterministic`() {
        val graph = linkedMapOf<String, Any>("nodes" to listOf(linkedMapOf("id" to "n1")), "edges" to emptyList<Any>())
        val h1 = ReplayEquivalence.graphHash(graph)
        val h2 = ReplayEquivalence.graphHash(graph)
        assertEquals(h1, h2)
    }

    @Test
    fun `graph hash produces 64-char hex`() {
        val graph = linkedMapOf<String, Any>("nodes" to listOf(linkedMapOf("id" to "n1")), "edges" to emptyList<Any>())
        val hash = ReplayEquivalence.graphHash(graph)
        assertEquals(64, hash.length)
        assertTrue(hash.all { it in '0'..'9' || it in 'a'..'f' })
    }

    @Test
    fun `checks list has correct structure`() {
        val graph = linkedMapOf<String, Any>("nodes" to emptyList<Any>(), "edges" to emptyList<Any>())
        val result = ReplayEquivalence.validate(envelope(graph), envelope(graph))
        @Suppress("UNCHECKED_CAST")
        val checks = result["checks"] as List<Map<String, Any>>
        assertEquals(3, checks.size)
        assertEquals("graph_hash", checks[0]["name"])
        assertEquals("global_fingerprint", checks[1]["name"])
        assertEquals("browser_identity", checks[2]["name"])
    }

    @Test
    fun `empty envelopes are equivalent`() {
        val result = ReplayEquivalence.validate(emptyMap(), emptyMap())
        assertTrue(result["equivalent"] as Boolean)
    }

    @Test
    fun `envelope with graph key works`() {
        val g = linkedMapOf<String, Any>("nodes" to emptyList<Any>(), "edges" to emptyList<Any>())
        val env = linkedMapOf<String, Any>("graph" to g)
        val result = ReplayEquivalence.validate(env, env)
        assertTrue(result["equivalent"] as Boolean)
    }

    @Test
    fun `deterministic across 1000 iterations`() {
        val graph = linkedMapOf<String, Any>(
            "nodes" to listOf(linkedMapOf("id" to "n1", "type" to "file")),
            "edges" to emptyList<Any>()
        )
        val env = envelope(graph)
        val expected = ReplayEquivalence.validate(env, env)
        for (i in 1..999) {
            val result = ReplayEquivalence.validate(env, env)
            assertEquals(expected["equivalent"], result["equivalent"])
        }
    }

    @Test
    fun `graph with multiple nodes and edges`() {
        val graph = linkedMapOf<String, Any>(
            "nodes" to listOf(
                linkedMapOf("id" to "n1", "type" to "file"),
                linkedMapOf("id" to "n2", "type" to "module")
            ),
            "edges" to listOf(linkedMapOf("source" to "n1", "target" to "n2", "type" to "imports"))
        )
        val result = ReplayEquivalence.validate(envelope(graph), envelope(graph))
        assertTrue(result["equivalent"] as Boolean)
    }

    @Test
    fun `graph with unicode content`() {
        val graph = linkedMapOf<String, Any>(
            "nodes" to listOf(linkedMapOf("id" to "n1", "name" to "\u4e16\u754c")),
            "edges" to emptyList<Any>()
        )
        val result = ReplayEquivalence.validate(envelope(graph), envelope(graph))
        assertTrue(result["equivalent"] as Boolean)
    }
}
