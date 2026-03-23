package com.webweavex;

import java.util.*;

public class Cleaner {
    public String clean(String text) {
        if (text == null || text.isEmpty()) return "";
        
        String result = text;
        result = result.replaceAll("\\s+", " ");
        result = result.trim();
        
        return result;
    }
}
