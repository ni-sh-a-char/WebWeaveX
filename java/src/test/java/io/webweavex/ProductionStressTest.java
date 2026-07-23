package io.webweavex;

import static org.junit.jupiter.api.Assertions.*;

import io.webweavex.crypto.*;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.graph.RuntimeGraph;
import io.webweavex.replay.ReplayEquivalence;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.Test;

/** Production stress, concurrency, and adversarial validation. */
class ProductionStressTest {

    // === Part 1: Stress Testing ===

    @Test
    void stableSerialize_100kIterations() {
        Map<String, Object> data = Map.of("version", "3.0.0", "nested", Map.of("a", 1, "b", List.of(1, 2, 3)));
        String expected = StableSerialize.stableSerialize(data);
        for (int i = 0; i < 100_000; i++) {
            assertEquals(expected, StableSerialize.stableSerialize(data));
        }
    }

    @Test
    void hashing_100kIterations() {
        Map<String, Object> data = Map.of("key", "value", "count", 42);
        String expected = Hashing.computeDeterministicHash(data);
        for (int i = 0; i < 100_000; i++) {
            assertEquals(expected, Hashing.computeDeterministicHash(data));
        }
    }

    @Test
    void kaalkaEncrypt_100kIterations() {
        Map<String, Object> data = Map.of("data", "payload");
        String first = Kaalka.encryptValue(data, "test-key");
        for (int i = 0; i < 99_999; i++) {
            assertEquals(first, Kaalka.encryptValue(data, "test-key"));
        }
    }

    @Test
    void kaalkaDecrypt_100kIterations() {
        String encrypted = Kaalka.encryptValue(Map.of("data", "payload"), "test-key");
        for (int i = 0; i < 100_000; i++) {
            Map<String, Object> dec = Kaalka.decryptValueEnvelope(encrypted, "test-key");
            assertEquals("webweavex-formula+kaalka@5.0.0", dec.get("algorithm"));
        }
    }

    @Test
    void graphFingerprint_100kIterations() {
        Map<String, Object> graph = Map.of(
            "nodes", List.of(Map.of("id", "n1", "type", "file"), Map.of("id", "n2", "type", "module")),
            "edges", List.of(Map.of("source", "n1", "target", "n2", "type", "imports"))
        );
        String expected = RuntimeGraph.graphFingerprint(graph);
        for (int i = 0; i < 100_000; i++) {
            assertEquals(expected, RuntimeGraph.graphFingerprint(graph));
        }
    }

    @Test
    void replayEquivalence_100kIterations() {
        Map<String, Object> graph = Map.of(
            "nodes", List.of(Map.of("id", "n1")),
            "edges", List.of()
        );
        Map<String, Object> env = Map.of("unified_runtime_graph", graph);
        Map<String, Object> expected = ReplayEquivalence.validate(env, env);
        for (int i = 0; i < 100_000; i++) {
            Map<String, Object> result = ReplayEquivalence.validate(env, env);
            assertEquals(expected.get("equivalent"), result.get("equivalent"));
        }
    }

    @Test
    void memoryStabilityUnderLoad() {
        Runtime runtime = Runtime.getRuntime();
        runtime.gc();
        long before = runtime.totalMemory() - runtime.freeMemory();
        for (int i = 0; i < 10_000; i++) {
            Hashing.computeDeterministicHash(Map.of("key", "value", "i", i));
            StableSerialize.stableSerialize(Map.of("key", "value", "i", i));
            Kaalka.encryptValue(Map.of("data", "payload", "i", i), "key");
        }
        runtime.gc();
        long after = runtime.totalMemory() - runtime.freeMemory();
        long growth = after - before;
        assertTrue(growth < 100_000_000, "Memory grew by " + (growth / 1024) + "KB");
    }

    // === Part 2: Concurrency ===

    @Test
    void concurrentSerialization() throws Exception {
        ExecutorService executor = Executors.newFixedThreadPool(8);
        CountDownLatch latch = new CountDownLatch(10_000);
        AtomicInteger errors = new AtomicInteger(0);
        Map<String, Object> data = Map.of("key", "value");
        String expected = StableSerialize.stableSerialize(data);

        for (int i = 0; i < 10_000; i++) {
            executor.submit(() -> {
                try {
                    if (!expected.equals(StableSerialize.stableSerialize(data))) {
                        errors.incrementAndGet();
                    }
                } catch (Exception e) {
                    errors.incrementAndGet();
                } finally {
                    latch.countDown();
                }
            });
        }
        latch.await(60, TimeUnit.SECONDS);
        executor.shutdown();
        assertEquals(0, errors.get());
    }

    @Test
    void concurrentHashing() throws Exception {
        ExecutorService executor = Executors.newFixedThreadPool(8);
        CountDownLatch latch = new CountDownLatch(10_000);
        AtomicInteger errors = new AtomicInteger(0);
        Map<String, Object> data = Map.of("key", "value");
        String expected = Hashing.computeDeterministicHash(data);

        for (int i = 0; i < 10_000; i++) {
            executor.submit(() -> {
                try {
                    if (!expected.equals(Hashing.computeDeterministicHash(data))) {
                        errors.incrementAndGet();
                    }
                } catch (Exception e) {
                    errors.incrementAndGet();
                } finally {
                    latch.countDown();
                }
            });
        }
        latch.await(60, TimeUnit.SECONDS);
        executor.shutdown();
        assertEquals(0, errors.get());
    }

    @Test
    void concurrentKaalkaEncryption() throws Exception {
        ExecutorService executor = Executors.newFixedThreadPool(8);
        CountDownLatch latch = new CountDownLatch(10_000);
        AtomicInteger errors = new AtomicInteger(0);
        Map<String, Object> data = Map.of("data", "payload");
        String expected = Kaalka.encryptValue(data, "key");

        for (int i = 0; i < 10_000; i++) {
            executor.submit(() -> {
                try {
                    if (!expected.equals(Kaalka.encryptValue(data, "key"))) {
                        errors.incrementAndGet();
                    }
                } catch (Exception e) {
                    errors.incrementAndGet();
                } finally {
                    latch.countDown();
                }
            });
        }
        latch.await(60, TimeUnit.SECONDS);
        executor.shutdown();
        assertEquals(0, errors.get());
    }

    // === Part 3: Adversarial Inputs ===

    @Test
    void emptyInputSerialization() {
        assertEquals("{}", StableSerialize.stableSerialize(Map.of()));
        assertEquals("{}", StableSerialize.stableSerialize(new LinkedHashMap<>()));
    }

    @Test
    void deeplyNestedStructure() {
        Object nested = "leaf";
        for (int i = 0; i < 200; i++) {
            nested = Map.of("level" + i, nested);
        }
        String result = StableSerialize.stableSerialize(nested);
        assertTrue(result.length() > 100);
    }

    @Test
    void extremelyLongString() {
        String longStr = "x".repeat(1_000_000);
        Map<String, Object> data = Map.of("text", longStr);
        String result = StableSerialize.stableSerialize(data);
        assertTrue(result.length() > 1_000_000);
    }

    @Test
    void unicodeEdgeCases() {
        Map<String, Object> data = Map.of(
            "emoji", "\uD83D\uDE80\uD83D\uDE80",
            "arabic", "\u0639\u0631\u0628\u064A",
            "chinese", "\u4E16\u754C",
            "combining", "caf\u0301"
        );
        String result = StableSerialize.stableSerialize(data);
        assertFalse(result.isEmpty());
        String hash = Hashing.computeDeterministicHash(data);
        assertEquals(64, hash.length());
    }

    @Test
    void nullHeavyStructure() {
        java.util.Map<String, Object> data = new LinkedHashMap<>();
        for (int i = 1; i <= 1000; i++) {
            data.put("key" + i, null);
        }
        String result = StableSerialize.stableSerialize(data);
        assertFalse(result.isEmpty());
    }

    @Test
    void largeDAGWorkflow() {
        // Build a 500-step linear workflow
        List<Map<String, Object>> steps = new ArrayList<>();
        for (int i = 1; i <= 500; i++) {
            steps.add(Map.of("name", "step" + i, "depends_on", i > 1 ? List.of("step" + (i - 1)) : List.of()));
        }
        // Verify it can be serialized deterministically
        String serialized = StableSerialize.stableSerialize(steps);
        assertFalse(serialized.isEmpty());
        assertEquals(serialized, StableSerialize.stableSerialize(steps));
    }

    // === Part 4: Long-Run Stability ===

    @Test
    void sustainedDeterminism_500kIterations() {
        Map<String, Object> data = Map.of("version", "3.0.0", "key", "value");
        String expectedHash = Hashing.computeDeterministicHash(data);
        String expectedSer = StableSerialize.stableSerialize(data);
        for (int i = 0; i < 500_000; i++) {
            assertEquals(expectedHash, Hashing.computeDeterministicHash(data));
            assertEquals(expectedSer, StableSerialize.stableSerialize(data));
        }
    }
}
