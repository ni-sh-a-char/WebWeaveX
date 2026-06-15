package io.webweavex.connectors;

import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/**
 * Port of {@code core.connectors.api_connector_engine.extract_api_runtime} and its
 * graphql/grpc sub-engines. Deterministic transform over a caller-supplied snapshot.
 */
public final class ApiConnectors {

    private ApiConnectors() {
    }

    /** {@code extract_api_runtime}. */
    public static Map<String, Object> extractApiRuntime(String apiType, Map<String, Object> snapshot) {
        Map<String, Object> s = Connectors.snap(snapshot);
        String normalized = apiType.toLowerCase(Locale.ROOT);

        Map<String, Object> base = new LinkedHashMap<>();
        base.put("api_type", normalized);
        base.put("endpoints", Connectors.sortedByStr(Connectors.getList(s, "endpoints", new ArrayList<>())));
        base.put("schemas", Connectors.getList(s, "schemas", new ArrayList<>()));
        base.put("auth_state", Connectors.getMap(s, "auth"));
        base.put("rate_limits", Connectors.getMap(s, "rate_limits"));
        base.put("response_topology", Connectors.getList(s, "responses", new ArrayList<>()));
        base.put("pagination_models", Connectors.getList(s, "pagination", new ArrayList<>()));
        base.put("bounded", true);

        if (normalized.equals("graphql")) {
            base.put("graphql", extractGraphqlRuntime(Py.asMap(Py.get(s, "graphql", null))));
        } else if (normalized.equals("grpc")) {
            base.put("grpc", extractGrpcRuntime(Py.asMap(Py.get(s, "grpc", null))));
        }
        return base;
    }

    /** {@code extract_graphql_runtime}. */
    public static Map<String, Object> extractGraphqlRuntime(Map<String, Object> snapshot) {
        Map<String, Object> s = Connectors.snap(snapshot);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("protocol", "graphql");
        out.put("endpoints", Connectors.getList(s, "endpoints", Connectors.list("/graphql")));
        out.put("schemas", Connectors.getList(s, "schemas", new ArrayList<>()));
        out.put("types", Connectors.sortedByStr(Connectors.getList(s, "types", new ArrayList<>())));
        out.put("bounded", true);
        return out;
    }

    /** {@code extract_grpc_runtime}. */
    public static Map<String, Object> extractGrpcRuntime(Map<String, Object> snapshot) {
        Map<String, Object> s = Connectors.snap(snapshot);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("protocol", "grpc");
        out.put("services", Connectors.sortedByStr(Connectors.getList(s, "services", new ArrayList<>())));
        out.put("methods", Connectors.sortedByStr(Connectors.getList(s, "methods", new ArrayList<>())));
        out.put("schemas", Connectors.getList(s, "protobuf", new ArrayList<>()));
        out.put("bounded", true);
        return out;
    }
}
