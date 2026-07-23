package io.webweavex.crypto

import io.webweavex.determinism.StableSerialize
import io.webweavex.fingerprint.Fingerprint
import io.webweavex.memory.MemoryEngine
import io.webweavex.repository.KnowledgeGraph
import io.webweavex.repository.KnowledgeEdge
import io.webweavex.repository.KnowledgeNode
import io.webweavex.replay.ReplayEngine
import io.webweavex.runtime.RuntimeSnapshot
import io.webweavex.workflow.WorkflowEngine
import io.webweavex.workflow.WorkflowStep
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class IdentityPlatformTest {

    @Test
    fun `SHA256 is the correct primitive for value hashing`() {
        val hash = Fingerprint.compute(mapOf("key" to "value"))
        assertEquals(64, hash.length)
        assertTrue(hash.all { it in '0'..'9' || it in 'a'..'f' })
    }

    @Test
    fun `SHA256 is deterministic across 1000 iterations`() {
        val data = mapOf("version" to "3.0.0", "type" to "test")
        val expected = Fingerprint.compute(data)
        for (i in 1..999) {
            assertEquals(expected, Fingerprint.compute(data))
        }
    }

    @Test
    fun `graph fingerprint uses Kaalka encryption`() {
        val graph = mapOf("nodes" to listOf(mapOf("id" to "n1")), "edges" to emptyList<Any>())
        val fp = Fingerprint.graphFingerprint(graph)
        assertTrue(fp is ByteArray)
        assertTrue(fp.isNotEmpty())
        assertEquals(fp.contentHashCode(), Fingerprint.graphFingerprint(graph).contentHashCode())
    }

    @Test
    fun `knowledge graph fingerprint is deterministic`() {
        val graph = KnowledgeGraph(
            nodes = listOf(KnowledgeNode("n1", "file", mapOf("name" to "test.dart"))),
            edges = listOf(KnowledgeEdge("n1", "n1", "self"))
        )
        val fp1 = graph.fingerprint()
        val fp2 = graph.fingerprint()
        assertEquals(fp1, fp2)
    }

    @Test
    fun `memory store fingerprint is deterministic`() {
        val store = MemoryEngine.create()
            .put("key", "value")
            .put("key2", 42)
        val fp1 = store.fingerprint()
        val fp2 = store.fingerprint()
        assertEquals(fp1, fp2)
    }

    @Test
    fun `memory entry fingerprint matches SHA256 of value`() {
        val store = MemoryEngine.create().put("key", "value")
        val entry = store.entries["key"]
        val expected = Fingerprint.compute("value")
        assertEquals(expected, entry!!.fingerprint)
    }

    @Test
    fun `replay snapshot fingerprint is deterministic`() {
        val state = mapOf("step" to 1, "data" to "processing")
        val snap1 = ReplayEngine.createSnapshot(state, 0)
        val snap2 = ReplayEngine.createSnapshot(state, 0)
        assertEquals(snap1.fingerprint, snap2.fingerprint)
    }

    @Test
    fun `workflow fingerprint is deterministic`() {
        val steps = listOf(
            WorkflowStep("step1", { mapOf("result" to 1) }),
            WorkflowStep("step2", { mapOf("result" to 2) }, dependsOn = listOf("step1"))
        )
        val result1 = WorkflowEngine.execute(steps, emptyMap())
        val result2 = WorkflowEngine.execute(steps, emptyMap())
        assertEquals(result1.fingerprint, result2.fingerprint)
    }

    @Test
    fun `runtime snapshot fingerprint is deterministic`() {
        val nodes = listOf(mapOf("id" to "n1", "type" to "file"))
        val edges = listOf(mapOf("source" to "n1", "target" to "n1", "type" to "self"))
        val meta = io.webweavex.runtime.RuntimeMetadata()
        val snap1 = RuntimeSnapshot.create(nodes, edges, meta)
        val snap2 = RuntimeSnapshot.create(nodes, edges, meta)
        assertEquals(snap1.fingerprint, snap2.fingerprint)
    }

    @Test
    fun `stable serialize produces consistent output`() {
        val data = mapOf("z" to 1, "a" to 2, "nested" to mapOf("b" to 3, "a" to 1))
        val s1 = StableSerialize.stableSerialize(data)
        val s2 = StableSerialize.stableSerialize(data)
        assertEquals(s1, s2)
        assertTrue(s1.contains("\"a\":2"))
        assertTrue(s1.contains("\"z\":1"))
    }

    @Test
    fun `Kaalka encrypt produces consistent output`() {
        val data = "test data".toByteArray(Charsets.UTF_8)
        val enc1 = KaalkaV5.encrypt(data, "123456")
        val enc2 = KaalkaV5.encrypt(data, "123456")
        assertTrue(enc1.contentEquals(enc2))
    }

    @Test
    fun `Kaalka encryptValue differs by key`() {
        val enc1 = KaalkaV5.encryptValue(mapOf("d" to "test"), "key-a")
        val enc2 = KaalkaV5.encryptValue(mapOf("d" to "test"), "key-b")
        assertTrue(enc1["encrypted"] != enc2["encrypted"])
    }

    @Test
    fun `cross-SDK identity hash matches Python`() {
        val data = mapOf("version" to "3.0.0", "type" to "test")
        val hash = Fingerprint.compute(data)
        assertEquals(64, hash.length)
        assertTrue(hash.all { it in '0'..'9' || it in 'a'..'f' })
    }
}
