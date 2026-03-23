package com.webweavex.pipeline;

import com.webweavex.core.*;
import java.util.*;

public class Chunker {
    private final int chunkSize;
    private final int overlap;

    public Chunker() {
        this.chunkSize = 500;
        this.overlap = 50;
    }

    public Chunker(int chunkSize, int overlap) {
        this.chunkSize = chunkSize;
        this.overlap = overlap;
    }

    public List<Chunk> chunk(String text) {
        List<Chunk> chunks = new ArrayList<>();
        if (text == null || text.isEmpty()) {
            return chunks;
        }

        int start = 0;
        int index = 0;

        while (start < text.length()) {
            int end = start + chunkSize;

            if (end < text.length()) {
                end = findWordBoundary(text, end);
            }

            String chunkText = text.substring(start, end);
            if (!chunkText.trim().isEmpty()) {
                chunks.add(new Chunk(chunkText, index, start, end));
                index++;
            }

            start = end - overlap;
            if (start < 0) start = 0;
        }

        return chunks;
    }

    private int findWordBoundary(String text, int position) {
        if (position >= text.length()) return position;

        for (int i = position; Math.max(0, position - 50) <= i; i--) {
            if (Character.isWhitespace(text.charAt(i))) {
                return i;
            }
        }

        return position;
    }
}
