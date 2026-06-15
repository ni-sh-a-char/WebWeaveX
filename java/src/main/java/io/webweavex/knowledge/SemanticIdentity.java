package io.webweavex.knowledge;

import io.webweavex.crypto.Hashing;
import io.webweavex.determinism.Py;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Ports of {@code core.knowledge.semantic_identity_resolver.resolve_semantic_identities}
 * and {@code core.knowledge.semantic_identity_calculus.identity_hash}.
 */
public final class SemanticIdentity {

    private SemanticIdentity() {
    }

    public static Map<String, Object> identityHash(String name, String namespace) {
        String raw = namespace + ":" + name;
        String digest = Hashing.sha256Hex(raw.getBytes(StandardCharsets.UTF_8)).substring(0, 16);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("name", name);
        out.put("namespace", namespace);
        out.put("id", digest);
        out.put("deterministic_inputs", List.of("name=" + name, "namespace=" + namespace));
        return out;
    }

    public static Map<String, Object> resolve(List<Object> entities, String namespace) {
        List<Object> resolved = new ArrayList<>();
        Map<String, Object> byId = new LinkedHashMap<>();
        for (Object e : entities == null ? List.of() : entities) {
            if (!Py.truthy(e)) {
                continue;
            }
            Map<String, Object> r = identityHash(Py.str(e), namespace);
            resolved.add(r);
            byId.put((String) r.get("id"), r.get("name"));
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("entities", resolved);
        out.put("index", byId);
        out.put("count", (long) resolved.size());
        return out;
    }
}
