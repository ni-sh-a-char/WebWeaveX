package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.documents.DocumentRuntime;
import io.webweavex.interaction.PageView;
import io.webweavex.interaction.Pagination;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/**
 * Session-4B cross-language parity: the two pure extraction APIs that survive the
 * dependency proof — {@code extract_document_runtime} (documents/IR) and
 * {@code extract_paginated_content} (interaction) — are byte-identical to canonical
 * Python 2.1.0 ({@code golden_vectors_s4b.json}). Every assertion compares Java output to
 * recorded Python output via {@code stable_serialize} + {@code compute_kaalka_hash}.
 */
class CrossLanguageParityS4BTest {

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS4BTest.class
                .getResourceAsStream("/parity/golden_vectors_s4b.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s4b.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s4b golden vectors", e);
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
    private static List<Object> listField(JsonNode inputs, String field) {
        JsonNode n = inputs.get(field);
        if (n == null || n.isNull()) {
            return null;
        }
        return (List<Object>) CrossLanguageParityTest.toNative(n);
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> mapField(JsonNode inputs, String field) {
        JsonNode n = inputs.get(field);
        if (n == null || n.isNull()) {
            return null;
        }
        return (Map<String, Object>) CrossLanguageParityTest.toNative(n);
    }

    @TestFactory
    List<DynamicTest> extractDocumentRuntime() {
        return section("extract_document_runtime", in -> DocumentRuntime.extractDocumentRuntime(
                in.get("text").asText(), listField(in, "slides"), mapField(in, "workbook")));
    }

    @TestFactory
    List<DynamicTest> extractPaginatedContent() {
        return section("extract_paginated_content", in -> Pagination.extractPaginatedContent(
                buildPage(in.get("page")), in.get("next_selector").asText()));
    }

    private static PageView buildPage(JsonNode pageNode) {
        if (pageNode == null || pageNode.isNull()) {
            return null;
        }
        @SuppressWarnings("unchecked")
        Map<String, Object> spec = (Map<String, Object>) CrossLanguageParityTest.toNative(pageNode);
        return new FixturePage(spec);
    }

    /** Deterministic fixture page mirroring the Python generator's {@code _Page} duck type. */
    private static final class FixturePage implements PageView {
        private String testUrl;
        private final Map<String, Object> paginate; // null when the spec omits "paginate"
        private final boolean hasNext;
        private final String nextUrl;
        private final boolean hasClick;
        private final boolean clickRaises;

        @SuppressWarnings("unchecked")
        FixturePage(Map<String, Object> spec) {
            this.testUrl = (String) spec.get("test_url");
            Object pm = spec.get("paginate");
            this.paginate = pm instanceof Map ? (Map<String, Object>) pm : null;
            Object nu = spec.get("next_url");
            this.hasNext = spec.containsKey("next_url") && nu != null;
            this.nextUrl = nu == null ? "" : nu.toString();
            this.hasClick = Boolean.TRUE.equals(spec.get("has_click"));
            this.clickRaises = Boolean.TRUE.equals(spec.get("click_raises"));
        }

        @Override
        public boolean hasTestUrl() {
            return true;
        }

        @Override
        public Object testUrl() {
            return testUrl;
        }

        @Override
        public void setTestUrl(String url) {
            this.testUrl = url;
        }

        @Override
        public boolean hasTestNextUrl() {
            return hasNext;
        }

        @Override
        public Object testNextUrl() {
            return nextUrl;
        }

        @Override
        public boolean hasTestPaginate() {
            return paginate != null;
        }

        @Override
        public String testPaginate(String currentUrl) {
            Object v = paginate.get(currentUrl);
            return v == null ? "" : v.toString();
        }

        @Override
        public boolean hasClick() {
            return hasClick;
        }

        @Override
        public void click(String selector) {
            if (clickRaises) {
                throw new RuntimeException("click failed");
            }
        }
    }
}
