package io.webweavex

import io.webweavex.crypto.KaalkaV5
import io.webweavex.determinism.StableSerialize
import io.webweavex.fingerprint.Fingerprint
import io.webweavex.memory.MemoryEngine
import io.webweavex.repository.*
import io.webweavex.replay.ReplayEngine
import io.webweavex.runtime.RuntimeMetadata
import io.webweavex.runtime.RuntimeSnapshot
import io.webweavex.workflow.WorkflowEngine
import io.webweavex.workflow.WorkflowStep
import kotlin.test.Test
import kotlin.test.assertTrue
import kotlin.test.assertEquals
import java.util.concurrent.CountDownLatch
import java.util.concurrent.Executors
import java.util.concurrent.atomic.AtomicInteger

class ProductionStressTest {

    // --- Part 1: Stress Testing ---

    @Test
    fun `100000 stable serializations`() {
        val data = mapOf("version" to "3.0.0", "nested" to mapOf("a" to 1, "b" to listOf(1, 2, 3)))
        val expected = StableSerialize.stableSerialize(data)
        repeat(100_000) {
            assertEquals(expected, StableSerialize.stableSerialize(data))
        }
    }

    @Test
    fun `100000 fingerprint operations`() {
        val data = mapOf("key" to "value", "count" to 42)
        val expected = Fingerprint.compute(data)
        repeat(100_000) {
            assertEquals(expected, Fingerprint.compute(data))
        }
    }

    @Test
    fun `100000 Kaalka encryptions`() {
        val data = mapOf("data" to "payload")
        val first = KaalkaV5.encryptValue(data, "test-key")
        repeat(99_999) {
            val result = KaalkaV5.encryptValue(data, "test-key")
            assertEquals(first["encrypted"], result["encrypted"])
        }
    }

    @Test
    fun `100000 Kaalka decryptions`() {
        val encrypted = KaalkaV5.encryptValue(mapOf("data" to "payload"), "test-key")
        val ciphertext = encrypted["encrypted"] as String
        repeat(100_000) {
            val decrypted = KaalkaV5.decryptValue(ciphertext, "test-key")
            assertEquals("webweavex-formula+kaalka@5.0.0", decrypted["algorithm"])
        }
    }

    @Test
    fun `100000 graph fingerprints`() {
        val graph = mapOf(
            "nodes" to listOf(mapOf("id" to "n1", "type" to "file"), mapOf("id" to "n2", "type" to "module")),
            "edges" to listOf(mapOf("from" to "n1", "to" to "n2", "type" to "imports"))
        )
        val expected = Fingerprint.graphFingerprint(graph)
        repeat(100_000) {
            val fp = Fingerprint.graphFingerprint(graph)
            assertTrue(fp.contentEquals(expected))
        }
    }

    @Test
    fun `100000 replay snapshots`() {
        val state = mapOf("step" to 1, "data" to "processing")
        val expected = ReplayEngine.createSnapshot(state, 0).fingerprint
        repeat(100_000) {
            assertEquals(expected, ReplayEngine.createSnapshot(state, 0).fingerprint)
        }
    }

    @Test
    fun `memory store under sustained load`() {
        var store = MemoryEngine.create()
        repeat(10_000) { i ->
            store = store.put("key$i", "value$i")
        }
        assertEquals(10_000, store.size())
        val fp1 = store.fingerprint()
        val fp2 = store.fingerprint()
        assertEquals(fp1, fp2)
    }

    @Test
    fun `large workflow execution`() {
        val steps = (1..100).map { i ->
            WorkflowStep("step$i", { mapOf("result" to i) },
                dependsOn = if (i > 1) listOf("step${i - 1}") else emptyList())
        }
        val result = WorkflowEngine.execute(steps, emptyMap())
        assertTrue(result.success)
        assertEquals(100, result.executionOrder.size)
    }

    @Test
    fun `large repository indexing`() {
        val nodes = (1..1000).map { i ->
            KnowledgeNode("n$i", "file", mapOf("name" to "file_$i.kt", "lang" to "kotlin"))
        }
        val edges = (1..999).map { i ->
            KnowledgeEdge("n$i", "n${i + 1}", "imports")
        }
        val graph = KnowledgeGraph(nodes, edges)
        val fp = graph.fingerprint()
        assertTrue(fp.isNotEmpty())
        val index = SearchIndex.build(graph)
        assertTrue(index.search("kotlin").isNotEmpty())
    }

    // --- Part 2: Concurrency Validation ---

    @Test
    fun `concurrent stable serializations`() {
        val executor = Executors.newFixedThreadPool(8)
        val latch = CountDownLatch(10_000)
        val errors = AtomicInteger(0)
        val data = mapOf("key" to "value")
        val expected = StableSerialize.stableSerialize(data)
        repeat(10_000) {
            executor.submit {
                try {
                    val result = StableSerialize.stableSerialize(data)
                    if (result != expected) errors.incrementAndGet()
                } catch (e: Exception) {
                    errors.incrementAndGet()
                } finally {
                    latch.countDown()
                }
            }
        }
        latch.await()
        executor.shutdown()
        assertEquals(0, errors.get())
    }

    @Test
    fun `concurrent fingerprint operations`() {
        val executor = Executors.newFixedThreadPool(8)
        val latch = CountDownLatch(10_000)
        val errors = AtomicInteger(0)
        val data = mapOf("key" to "value")
        val expected = Fingerprint.compute(data)
        repeat(10_000) {
            executor.submit {
                try {
                    val result = Fingerprint.compute(data)
                    if (result != expected) errors.incrementAndGet()
                } catch (e: Exception) {
                    errors.incrementAndGet()
                } finally {
                    latch.countDown()
                }
            }
        }
        latch.await()
        executor.shutdown()
        assertEquals(0, errors.get())
    }

    @Test
    fun `concurrent Kaalka encryptions`() {
        val executor = Executors.newFixedThreadPool(8)
        val latch = CountDownLatch(10_000)
        val errors = AtomicInteger(0)
        val data = mapOf("data" to "payload")
        val expected = KaalkaV5.encryptValue(data, "key")["encrypted"]
        repeat(10_000) {
            executor.submit {
                try {
                    val result = KaalkaV5.encryptValue(data, "key")["encrypted"]
                    if (result != expected) errors.incrementAndGet()
                } catch (e: Exception) {
                    errors.incrementAndGet()
                } finally {
                    latch.countDown()
                }
            }
        }
        latch.await()
        executor.shutdown()
        assertEquals(0, errors.get())
    }

    // --- Part 3: Adversarial Inputs ---

    @Test
    fun `empty input to all subsystems`() {
        assertEquals("{}", StableSerialize.stableSerialize(emptyMap<String, Any>()))
        assertTrue(StableSerialize.stableSerialize(emptyList<Any>()).isNotEmpty())
        assertTrue(Fingerprint.compute(emptyMap<String, Any>()).length == 64)
        val enc = KaalkaV5.encryptValue(emptyMap<String, Any>(), "key")
        assertTrue(enc["encrypted"] is String)
    }

    @Test
    fun `deeply nested structures`() {
        var nested: Any = "leaf"
        repeat(200) { i -> nested = mapOf("level$i" to nested) }
        val result = StableSerialize.stableSerialize(nested)
        assertTrue(result.length > 100)
    }

    @Test
    fun `extremely long strings`() {
        val longStr = "x".repeat(1_000_000)
        val data = mapOf("text" to longStr)
        val result = StableSerialize.stableSerialize(data)
        assertTrue(result.length > 1_000_000)
    }

    @Test
    fun `unicode edge cases`() {
        val data = mapOf(
            "emoji" to "\ud83d\ude80\ud83d\ude80",
            "arabic" to "\u0639\u0631\u0628\u064a",
            "chinese" to "\u4e16\u754c",
            "combining" to "caf\u0301"
        )
        val result = StableSerialize.stableSerialize(data)
        assertTrue(result.isNotEmpty())
        val hash = Fingerprint.compute(data)
        assertEquals(64, hash.length)
    }

    @Test
    fun `null-heavy structures`() {
        val data = (1..1000).associate { "key$it" to null }
        val result = StableSerialize.stableSerialize(data)
        assertTrue(result.isNotEmpty())
    }

    @Test
    fun `large DAG workflow`() {
        val steps = (1..500).map { i ->
            WorkflowStep("step$i", { mapOf("i" to i) },
                dependsOn = if (i > 1) listOf("step${i - 1}") else emptyList())
        }
        val result = WorkflowEngine.execute(steps, emptyMap())
        assertTrue(result.success)
        assertEquals(500, result.executionOrder.size)
    }

    // --- Part 4: Memory Stability ---

    @Test
    fun `memory does not leak across repeated operations`() {
        val before = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()
        repeat(10_000) {
            Fingerprint.compute(mapOf("key" to it))
            StableSerialize.stableSerialize(mapOf("key" to it))
            KaalkaV5.encryptValue(mapOf("data" to it), "key")
        }
        System.gc()
        val after = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()
        val growth = after - before
        assertTrue(growth < 100_000_000, "Memory grew by ${growth / 1024}KB — possible leak")
    }
}
