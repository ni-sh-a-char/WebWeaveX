package com.webweavex

class Cleaner {
    fun clean(text: String): String {
        if (text.isEmpty()) return ""
        
        var result = text.replace("\\s+".toRegex(), " ")
        result = result.trim()
        
        return result
    }
}
