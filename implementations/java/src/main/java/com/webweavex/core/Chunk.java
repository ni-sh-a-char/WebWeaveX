package com.webweavex.core;

import java.util.*;

public class Chunk {
    private final String text;
    private final int index;
    private final int start;
    private final int end;

    public Chunk(String text, int index, int start, int end) {
        this.text = text;
        this.index = index;
        this.start = start;
        this.end = end;
    }

    public String getText() { return text; }
    public int getIndex() { return index; }
    public int getStart() { return start; }
    public int getEnd() { return end; }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new LinkedHashMap<>();
        map.put("text", text);
        map.put("index", index);
        map.put("start", start);
        map.put("end", end);
        return map;
    }
}
