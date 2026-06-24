package io.webweavex.parity;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.webweavex.WebWeaveX;
import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.StableSerialize;
import io.webweavex.documents.DocumentSemanticIr;
import io.webweavex.interaction.InfiniteScroll;
import io.webweavex.interaction.InteractionReplay;
import io.webweavex.interaction.ScrollPage;
import io.webweavex.repository.RepositoryQuery;
import io.webweavex.streaming.StreamPage;
import io.webweavex.streaming.StreamingRuntime;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;

/**
 * Session-28 cross-language parity: the frontier-reduced portable APIs proven in Session 28 are
 * byte-identical to canonical Python 2.1.0 ({@code golden_vectors_s28.json}):
 * {@code version}/{@code __version__} (module constants), {@code query_repo} (pure passthrough),
 * {@code compile_document} (= {@code compile_document_ir}), and the four browser-free stub-page
 * stream/interaction engines ({@code capture_websocket_frames}, {@code track_websocket_connections},
 * {@code capture_dom_mutations}, {@code extract_infinite_scroll}, {@code replay_interactions}).
 */
class CrossLanguageParityS28Test {

    private static JsonNode golden() {
        try (InputStream in = CrossLanguageParityS28Test.class
                .getResourceAsStream("/parity/golden_vectors_s28.json")) {
            if (in == null) {
                throw new IllegalStateException("golden_vectors_s28.json not on classpath");
            }
            return new ObjectMapper().readTree(in);
        } catch (Exception e) {
            throw new IllegalStateException("failed to load s28 golden vectors", e);
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
    private static Map<String, Object> m(JsonNode in, String f) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? null : (Map<String, Object>) CrossLanguageParityTest.toNative(n);
    }

    @SuppressWarnings("unchecked")
    private static List<Object> l(JsonNode in, String f) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? null : (List<Object>) CrossLanguageParityTest.toNative(n);
    }

    private static String s(JsonNode in, String f, String d) {
        JsonNode n = in.get(f);
        return (n == null || n.isNull()) ? d : n.asText();
    }

    // ---- stub pages mirroring the canonical Python test doubles ----

    static final class StreamStub implements StreamPage {
        List<Object> wsFrames;
        List<Object> wsConns;
        List<Object> domMut;
        String html;

        @Override public boolean hasTestWebsocketFrames() { return wsFrames != null; }
        @Override public List<Object> testWebsocketFrames() { return wsFrames; }
        @Override public boolean hasTestWebsocketConnections() { return wsConns != null; }
        @Override public List<Object> testWebsocketConnections() { return wsConns; }
        @Override public boolean hasTestDomMutations() { return domMut != null; }
        @Override public List<Object> testDomMutations() { return domMut; }
        @Override public boolean hasTestHtml() { return html != null; }
        @Override public String testHtml() { return html; }
    }

    /** Mirror of tests/interaction/test_infinite_scroll.py::_ScrollPage. */
    static final class ScrollStub implements ScrollPage {
        String html = "<html>start</html>";
        String domHash = Kaalka.computeKaalkaHash("<html>start</html>");
        int count = 0;

        @Override public boolean hasTestDomHash() { return true; }
        @Override public Object testDomHash() { return domHash; }
        @Override public boolean hasTestScroll() { return true; }
        @Override public void testScroll() {
            count++;
            if (count > 2) {
                return;
            }
            html += "<div>" + count + "</div>";
            domHash = Kaalka.computeKaalkaHash(html);
        }
    }

    private static StreamPage wsPage(JsonNode in) {
        if (in.has("_test_websocket_connections")) {
            StreamStub p = new StreamStub();
            p.wsConns = l(in, "_test_websocket_connections");
            return p;
        }
        if (in.has("_test_websocket_frames")) {
            StreamStub p = new StreamStub();
            p.wsFrames = l(in, "_test_websocket_frames");
            return p;
        }
        return null;
    }

    private static StreamPage domPage(JsonNode in) {
        if (in.has("page") && in.get("page").isNull()) {
            return null;
        }
        StreamStub p = new StreamStub();
        p.html = s(in, "_test_html", null);
        p.domMut = l(in, "_test_dom_mutations");
        return p;
    }

    @TestFactory
    List<DynamicTest> portableApis() {
        List<DynamicTest> t = new ArrayList<>();

        t.addAll(section("version", in -> WebWeaveX.VERSION));
        t.addAll(section("__version__", in -> WebWeaveX.VERSION));

        t.addAll(section("query_repo", in -> RepositoryQuery.queryRepository(m(in, "result"), "")));

        t.addAll(section("compile_document", in -> DocumentSemanticIr.compileDocumentIr(s(in, "text", ""))));

        t.addAll(section("capture_websocket_frames", in -> StreamingRuntime.captureWebsocketFrames(wsPage(in))));
        t.addAll(section("track_websocket_connections",
                in -> StreamingRuntime.trackWebsocketConnections(wsPage(in))));
        t.addAll(section("capture_dom_mutations", in -> StreamingRuntime.captureDomMutations(domPage(in))));

        t.addAll(section("extract_infinite_scroll", in -> InfiniteScroll.extractInfiniteScroll(new ScrollStub())));

        t.addAll(section("replay_interactions",
                in -> InteractionReplay.replayInteractions(null, l(in, "interaction_log"))));

        return t;
    }
}
