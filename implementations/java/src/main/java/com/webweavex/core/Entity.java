package com.webweavex.core;

import java.util.*;

public class Entity {
    private final String type;
    private final String value;

    public Entity(String type, String value) {
        this.type = type;
        this.value = value;
    }

    public String getType() { return type; }
    public String getValue() { return value; }

    public Map<String, String> toMap() {
        Map<String, String> map = new LinkedHashMap<>();
        map.put("type", type);
        map.put("value", value);
        return map;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Entity entity = (Entity) o;
        return Objects.equals(type, entity.type) && Objects.equals(value, entity.value);
    }

    @Override
    public int hashCode() {
        return Objects.hash(type, value);
    }
}
