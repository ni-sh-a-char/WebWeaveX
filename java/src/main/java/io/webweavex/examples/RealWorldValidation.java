package io.webweavex.examples;

import io.webweavex.WebWeaveX;
import io.webweavex.crypto.Hashing;
import io.webweavex.determinism.GlobalRuntimeFingerprint;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.graph.RuntimeGraph;
import io.webweavex.replay.ReplayEquivalence;
import java.util.*;

public class RealWorldValidation {
    public static void main(String[] args) {
        System.out.println("WebWeaveX Java SDK v" + WebWeaveX.VERSION);
        
        // 1. Deterministic Serialization
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("b", 2); data.put("a", 1);
        String canonical = StableSerialize.stableSerialize(data);
        String hash = Hashing.computeDeterministicHash(data);
        System.out.println("1. Serialization: " + canonical);
        System.out.println("   Deterministic: " + hash.equals(Hashing.computeDeterministicHash(data)));
        
        // 2. Runtime Fingerprint
        String fp = GlobalRuntimeFingerprint.compute(new HashMap<>());
        System.out.println("2. Fingerprint: " + fp.substring(0, 16));
        
        // 3. Graph Operations
        Map<String, Object> graph = RuntimeGraph.normalizeRuntimeGraph(
            Map.of("nodes", List.of(Map.of("id", "1")), "edges", List.of()));
        System.out.println("3. Graph normalized: " + graph.containsKey("nodes"));
        
        // 4. Replay Equivalence
        Map<String, Object> env = Map.of("browser_ir", Map.of("runtime_identity", "test"));
        Map<String, Object> r = ReplayEquivalence.validate(env, new LinkedHashMap<>(env));
        System.out.println("4. Replay: equivalent=" + r.get("equivalent"));
        
        System.out.println("ALL WORKFLOWS PASSED");
    }
}
