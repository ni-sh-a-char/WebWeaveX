package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.execution.ExecutionRuntime;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/**
 * Session-9 cross-language parity: the entire {@code core.execution} family
 * (io.webweavex.execution.ExecutionRuntime) is byte-identical to canonical Python 2.1.0
 * ({@code golden_vectors_s9.json}). Every assertion compares Java output to recorded Python
 * output via {@code stable_serialize} + {@code compute_kaalka_hash}.
 */
class CrossLanguageParityS9Test {

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS9Test.class
                .getResourceAsStream("/parity/golden_vectors_s9.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s9.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s9 golden vectors", e);
        }
    }

    private List<DynamicTest> section(String name, Function<JsonNode, Object> fn) {
        List<DynamicTest> tests = new ArrayList<>();
        for (JsonNode v : golden().get(name)) {
            tests.add(DynamicTest.dynamicTest(name + ":" + v.get("name").asText(), () -> {
                Object output = fn.apply(v.get("inputs"));
                assertEquals(v.get("serialized").asText(), StableSerialize.stableSerialize(output));
                assertEquals(v.get("hash").asText(), Kaalka.computeKaalkaHash(output));
            }));
        }
        return tests;
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> mapF(JsonNode in, String f) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? null : (Map<String, Object>) CrossLanguageParityTest.toNative(n);
    }

    @SuppressWarnings("unchecked")
    private static List<Object> listF(JsonNode in, String f) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? null : (List<Object>) CrossLanguageParityTest.toNative(n);
    }

    private static String strF(JsonNode in, String f, String dflt) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? dflt : n.asText();
    }

    private static long longF(JsonNode in, String f, long dflt) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? dflt : n.asLong();
    }

    private static boolean boolF(JsonNode in, String f, boolean dflt) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? dflt : n.asBoolean();
    }

    @TestFactory
    List<DynamicTest> buildRuntimeSandbox() {
        return section("build_runtime_sandbox", in -> ExecutionRuntime.buildRuntimeSandbox(
                strF(in, "runtime", "browser"), listF(in, "allowed_actions"),
                boolF(in, "rollback_enabled", true), longF(in, "max_actions", 1000),
                longF(in, "timeout_ticks", 10000), strF(in, "replay_policy", "strict")));
    }

    @TestFactory
    List<DynamicTest> executeRuntimeAction() {
        return section("execute_runtime_action", in -> ExecutionRuntime.executeRuntimeAction(
                mapF(in, "raw_action"), mapF(in, "sandbox"), mapF(in, "policy"), mapF(in, "permissions"),
                longF(in, "tick", 0), 0, 0));
    }

    @TestFactory
    List<DynamicTest> replayRuntimeExecution() {
        return section("replay_runtime_execution", in -> ExecutionRuntime.replayRuntimeExecution(
                listF(in, "actions"), listF(in, "transactions"), listF(in, "mutations"), longF(in, "tick", 0)));
    }

    @TestFactory
    List<DynamicTest> simulateRuntimeExecution() {
        return section("simulate_runtime_execution", in -> ExecutionRuntime.simulateRuntimeExecution(
                listF(in, "actions"), mapF(in, "sandbox"), longF(in, "tick", 0)));
    }

    @TestFactory
    List<DynamicTest> runExecutionRuntime() {
        return section("run_execution_runtime", in -> ExecutionRuntime.runExecutionRuntime(
                mapF(in, "sources"), mapF(in, "stored"), listF(in, "workers"), strF(in, "runtime", "browser"),
                longF(in, "tick", 0), boolF(in, "simulate", false), boolF(in, "rollback_enabled", true)));
    }

    @TestFactory
    List<DynamicTest> runExecutionForExtraction() {
        return section("run_execution_for_extraction", in -> ExecutionRuntime.runExecutionForExtraction(
                boolF(in, "execution_runtime", true), strF(in, "memory_path", ""), strF(in, "memory_key", ""),
                mapF(in, "sources"), listF(in, "workers"), strF(in, "runtime", "browser"), longF(in, "tick", 0),
                boolF(in, "simulate_execution", false), boolF(in, "rollback_enabled", true),
                boolF(in, "merge_graph", true)));
    }

    // ---- engine-level parity (covers internal branches; Python oracle) ------------------

    @TestFactory
    List<DynamicTest> applyRuntimeTransition() {
        return section("apply_runtime_transition", in -> ExecutionRuntime.applyRuntimeTransition(
                strF(in, "state", "idle"), strF(in, "event", "")));
    }

    @TestFactory
    List<DynamicTest> buildRuntimePolicy() {
        return section("build_runtime_policy", in -> ExecutionRuntime.buildRuntimePolicy(
                boolF(in, "allow_terminal", false)));
    }

    @TestFactory
    List<DynamicTest> enforceRuntimePolicy() {
        return section("enforce_runtime_policy", in -> ExecutionRuntime.enforceRuntimePolicy(
                mapF(in, "policy"), mapF(in, "action"), longF(in, "mutation_count", 0),
                longF(in, "action_count", 0)));
    }

    @TestFactory
    List<DynamicTest> validateRuntimePermissions() {
        return section("validate_runtime_permissions", in -> ExecutionRuntime.validateRuntimePermissions(
                mapF(in, "permissions"), strF(in, "runtime", "browser"), strF(in, "action_type", "")));
    }

    @TestFactory
    List<DynamicTest> trackRuntimeMutations() {
        return section("track_runtime_mutations", in -> ExecutionRuntime.trackRuntimeMutations(
                listF(in, "prior"), mapF(in, "mutation")));
    }

    @TestFactory
    List<DynamicTest> enqueueRuntimeAction() {
        return section("enqueue_runtime_action", in -> ExecutionRuntime.enqueueRuntimeAction(
                listF(in, "queue"), mapF(in, "action"), longF(in, "priority", 0)));
    }

    @TestFactory
    List<DynamicTest> dequeueRuntimeAction() {
        return section("dequeue_runtime_action", in -> ExecutionRuntime.dequeueRuntimeAction(listF(in, "queue")));
    }

    @TestFactory
    List<DynamicTest> scheduleRuntimeExecution() {
        return section("schedule_runtime_execution", in -> ExecutionRuntime.scheduleRuntimeExecution(
                listF(in, "actions"), longF(in, "tick", 0)));
    }

    @TestFactory
    List<DynamicTest> beginRuntimeTransaction() {
        return section("begin_runtime_transaction", in -> ExecutionRuntime.beginRuntimeTransaction(
                longF(in, "tick", 0), strF(in, "checkpoint_id", "")));
    }

    @TestFactory
    List<DynamicTest> commitRuntimeTransaction() {
        return section("commit_runtime_transaction", in -> ExecutionRuntime.commitRuntimeTransaction(
                mapF(in, "transaction")));
    }

    @TestFactory
    List<DynamicTest> buildRuntimeWorkers() {
        return section("build_runtime_workers", in -> ExecutionRuntime.buildRuntimeWorkers(listF(in, "nodes")));
    }

    @TestFactory
    List<DynamicTest> federateRuntimeExecution() {
        return section("federate_runtime_execution", in -> ExecutionRuntime.federateRuntimeExecution(
                listF(in, "workers"), listF(in, "actions")));
    }

    @TestFactory
    List<DynamicTest> coordinateRuntimeExecution() {
        return section("coordinate_runtime_execution", in -> ExecutionRuntime.coordinateRuntimeExecution(
                listF(in, "queue"), mapF(in, "federation"), mapF(in, "workflow"), mapF(in, "sync_state")));
    }

    @TestFactory
    List<DynamicTest> recoverRuntimeExecution() {
        return section("recover_runtime_execution", in -> ExecutionRuntime.recoverRuntimeExecution(
                listF(in, "failed_actions"), mapF(in, "checkpoint"), listF(in, "interrupted_workflows")));
    }

    @TestFactory
    List<DynamicTest> buildRuntimeAction() {
        return section("build_runtime_action", in -> ExecutionRuntime.buildRuntimeAction(
                strF(in, "action_type", ""), strF(in, "runtime", "browser"), mapF(in, "payload"),
                longF(in, "tick", 0)));
    }

    @TestFactory
    List<DynamicTest> buildUnifiedRuntimeGraph() {
        return section("build_unified_runtime_graph", in -> ExecutionRuntime.buildUnifiedRuntimeGraph(
                listF(in, "runtime_irs")));
    }
}
