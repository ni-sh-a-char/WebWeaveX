package io.webweavex.kernel;

import io.webweavex.determinism.Normalization;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Canonical ingress descriptor for the runtime pipeline — port of the frozen
 * Python dataclass {@code core.contracts.runtime_contracts.UniversalInput}.
 *
 * <p>{@link #toDict()} is byte-identical to the Python {@code to_dict()}: options
 * sorted by key, {@code session} defaulted to {@code {}}, {@code bounded: true}
 * appended.
 */
public final class UniversalInput {

    /** Canonical runtime phases (mirrors the Python {@code RuntimePhase} enum). */
    public static final List<String> RUNTIME_PHASE_VALUES = List.of(
            "ingestion", "execution", "semantic", "causality",
            "synchronization", "memory", "reconstruction", "graph");

    private final String source;
    private final String sourceType;
    private final String url;
    private final String path;
    private final Map<String, Object> session;
    private final Map<String, Object> options;
    private final long tick;

    private UniversalInput(Builder b) {
        this.source = b.source;
        this.sourceType = b.sourceType;
        this.url = b.url;
        this.path = b.path;
        this.session = b.session;
        this.options = b.options;
        this.tick = b.tick;
    }

    public static Builder of(String source) {
        return new Builder(source);
    }

    /** Deterministic dict matching Python {@code UniversalInput.to_dict}. */
    public Map<String, Object> toDict() {
        List<String> keys = new ArrayList<>(options.keySet());
        keys.sort(Normalization::codePointCompare);
        Map<String, Object> sortedOptions = new LinkedHashMap<>();
        for (String k : keys) {
            sortedOptions.put(k, options.get(k));
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("source", source);
        out.put("source_type", sourceType);
        out.put("url", url);
        out.put("path", path);
        out.put("session", session == null ? new LinkedHashMap<>() : session);
        out.put("options", sortedOptions);
        out.put("tick", tick);
        out.put("bounded", true);
        return out;
    }

    /** Fluent builder mirroring the Python dataclass defaults. */
    public static final class Builder {
        private final String source;
        private String sourceType = "auto";
        private String url = "";
        private String path = "";
        private Map<String, Object> session = null;
        private Map<String, Object> options = new LinkedHashMap<>();
        private long tick = 0;

        private Builder(String source) {
            this.source = source;
        }

        public Builder sourceType(String v) {
            this.sourceType = v;
            return this;
        }

        public Builder url(String v) {
            this.url = v;
            return this;
        }

        public Builder path(String v) {
            this.path = v;
            return this;
        }

        public Builder session(Map<String, Object> v) {
            this.session = v;
            return this;
        }

        public Builder options(Map<String, Object> v) {
            this.options = v == null ? new LinkedHashMap<>() : v;
            return this;
        }

        public Builder tick(long v) {
            this.tick = v;
            return this;
        }

        public UniversalInput build() {
            return new UniversalInput(this);
        }
    }
}
