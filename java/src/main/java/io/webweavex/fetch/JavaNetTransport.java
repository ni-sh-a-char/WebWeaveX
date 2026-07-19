package io.webweavex.fetch;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.*;
import java.util.concurrent.CompletableFuture;
public class JavaNetTransport implements HttpTransport {
    private final HttpClient client = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(30)).followRedirects(HttpClient.Redirect.NORMAL).build();
    private static final String UA = "WebWeaveX/3.0.0";
    public Map<String, Object> fetchSync(String url) {
        try {
            HttpRequest req = HttpRequest.newBuilder().uri(URI.create(url)).header("User-Agent", UA).timeout(Duration.ofSeconds(30)).GET().build();
            HttpResponse<String> resp = client.send(req, HttpResponse.BodyHandlers.ofString());
            Map<String, Object> r = new LinkedHashMap<>();
            r.put("text", resp.body()); r.put("status", resp.statusCode());
            r.put("contentType", resp.headers().firstValue("content-type").orElse("text/plain"));
            r.put("ok", resp.statusCode() >= 200 && resp.statusCode() < 400); r.put("error", "");
            return r;
        } catch (Exception e) {
            Map<String, Object> r = new LinkedHashMap<>();
            r.put("text", ""); r.put("status", 0); r.put("contentType", "text/plain");
            r.put("ok", false); r.put("error", e.getMessage()); return r;
        }
    }
    public CompletableFuture<Map<String, Object>> fetchAsync(String url) {
        return CompletableFuture.supplyAsync(() -> fetchSync(url));
    }
}
