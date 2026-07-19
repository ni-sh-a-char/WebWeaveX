package io.webweavex.fetch;
import java.util.*;
import java.util.regex.*;
public class Crawler {
    private final HttpTransport transport;
    private final Set<String> visited = new LinkedHashSet<>();
    private final List<String> discovered = new ArrayList<>();
    public Crawler() { this.transport = HttpTransport.getDefault(); }
    public Crawler(HttpTransport t) { this.transport = t; }
    public Map<String, Object> crawl(String url) { crawlRecursive(url, 0); Map<String, Object> r = new LinkedHashMap<>(); r.put("visited", new ArrayList<>(visited)); r.put("discovered", new ArrayList<>(discovered)); return r; }
    private void crawlRecursive(String url, int depth) {
        if (depth > 3 || visited.contains(url)) return;
        visited.add(url);
        Map<String, Object> resp = transport.fetchSync(url);
        if (!(boolean) resp.getOrDefault("ok", false)) return;
        String text = (String) resp.get("text");
        if (text == null) return;
        Matcher m = Pattern.compile("href=\"([^\"]+)\"").matcher(text);
        while (m.find()) { String link = m.group(1); if (!visited.contains(link)) discovered.add(link); }
    }
}
