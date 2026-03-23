package com.webweavex.pipeline;

import com.webweavex.core.*;
import org.jsoup.*;
import org.jsoup.nodes.*;
import org.jsoup.select.*;
import java.util.*;

public class Parser {
    private final boolean extractVisibleText;
    private final boolean removeScripts;
    private final boolean removeStyles;

    public Parser() {
        this.extractVisibleText = true;
        this.removeScripts = true;
        this.removeStyles = true;
    }

    public String parse(String html, String url) {
        if (html == null || html.isEmpty()) return "";

        try {
            Document doc = Jsoup.parse(html);

            if (removeScripts) {
                doc.select("script").remove();
            }

            if (removeStyles) {
                doc.select("style").remove();
            }

            if (extractVisibleText) {
                return extractVisibleText(doc);
            }

            return doc.body().text();
        } catch (Exception e) {
            return "";
        }
    }

    private String extractVisibleText(Document doc) {
        Set<String> skipTags = new HashSet<>(Arrays.asList("script", "style", "noscript", "iframe", "svg", "head"));
        List<String> textParts = new ArrayList<>();

        Elements body = doc.body().select("*");
        for (Element el : body) {
            if (skipTags.contains(el.tagName().toLowerCase())) continue;

            String text = el.text().trim();
            if (!text.isEmpty()) {
                textParts.add(text);
            }
        }

        return String.join(" ", textParts).replaceAll("\\s+", " ").trim();
    }

    public Map<String, String> extractMetadata(String html) {
        Map<String, String> metadata = new LinkedHashMap<>();

        try {
            Document doc = Jsoup.parse(html);

            Element title = doc.selectFirst("title");
            if (title != null) {
                metadata.put("title", title.text().trim());
            }

            Elements metaTags = doc.select("meta");
            for (Element meta : metaTags) {
                String name = meta.attr("name");
                if (name.isEmpty()) name = meta.attr("property");
                String content = meta.attr("content");
                if (!name.isEmpty() && !content.isEmpty()) {
                    metadata.put(name, content);
                }
            }
        } catch (Exception e) {
            // Ignore
        }

        return metadata;
    }
}
