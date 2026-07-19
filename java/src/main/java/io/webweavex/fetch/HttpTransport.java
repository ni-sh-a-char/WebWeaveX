package io.webweavex.fetch;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
public interface HttpTransport {
    Map<String, Object> fetchSync(String url);
    CompletableFuture<Map<String, Object>> fetchAsync(String url);
    static HttpTransport getDefault() { return new JavaNetTransport(); }
}
