package com.webweavex.pipeline;

import com.webweavex.core.*;
import java.util.*;

public class Cleaner {
    private final boolean normalizeWhitespace;
    private final boolean strip;
    private final boolean removeEmptyLines;

    public Cleaner() {
        this.normalizeWhitespace = true;
        this.strip = true;
        this.removeEmptyLines = true;
    }

    public String clean(String text) {
        if (text == null) return "";

        if (normalizeWhitespace) {
            text = text.replaceAll("\\s+", " ");
        }

        if (strip) {
            text = text.trim();
        }

        if (removeEmptyLines) {
            String[] lines = text.split("\\n");
            StringBuilder sb = new StringBuilder();
            for (String line : lines) {
                String trimmed = line.trim();
                if (!trimmed.isEmpty()) {
                    if (sb.length() > 0) sb.append("\n");
                    sb.append(trimmed);
                }
            }
            text = sb.toString();
        }

        return text;
    }
}
