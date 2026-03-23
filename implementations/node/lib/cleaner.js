/** Text cleaner - normalizes whitespace */

export class Cleaner {
  constructor(config = {}) {
    this.normalizeWhitespace = true;
    this.strip = true;
    this.removeEmptyLines = true;
    this.lowercase = false;
  }

  clean(text) {
    if (!text) return "";
    
    let result = text;
    
    if (this.normalizeWhitespace) {
      result = result.replace(/\s+/g, " ");
    }
    
    if (this.strip) {
      result = result.trim();
    }
    
    if (this.removeEmptyLines) {
      result = result.replace(/^\s*$/gm, "");
      result = result.replace(/\n{3,}/g, "\n\n");
      result = result.trim();
    }
    
    if (this.lowercase) {
      result = result.toLowerCase();
    }
    
    return result;
  }
}
