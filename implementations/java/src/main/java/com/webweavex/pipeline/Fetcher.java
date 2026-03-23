package com.webweavex.pipeline;

import com.webweavex.core.*;
import java.net.http.*;
import java.net.URI;
import java.time.Duration;
import java.util.*;

public class Fetcher {
    private final int timeout;
    private final int retries;
    private final String userAgent;

    public Fetcher() {
        this.timeout = 10;
        this.retries = 3;
        this.userAgent = "WebWeaveX/1.0";
    }

    public String fetch(String url) throws Exception {
        HttpClient client = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(timeout))
            .build();

        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .header("User-Agent", userAgent)
            .header("Accept-Language", "en-US,en;q=0.9")
            .timeout(Duration.ofSeconds(timeout))
            .GET()
            .build();

        Exception lastError = null;
        for (int attempt = 0; attempt < retries; attempt++) {
            try {
                HttpResponse<String> response = client.send(request, 
                    HttpResponse.BodyHandlers.ofString());
                
                if (response.statusCode() >= 200 && response.statusCode() < 300) {
                    return response.body();
                }
                
                if (response.statusCode() >= 400) {
                    throw new Exception("HTTP " + response.statusCode());
                }
            } catch (Exception e) {
                lastError = e;
                if (attempt < retries - 1) {
                    Thread.sleep(1000);
                }
            }
        }

        throw lastError != null ? lastError : new Exception("Failed to fetch " + url);
    }
}
