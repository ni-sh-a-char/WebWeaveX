/** Entity extraction using regex patterns */

export class EntityEngine {
  constructor(config = {}) {
    this.patterns = {
      email: {
        regex: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g,
        type: "email"
      },
      url: {
        regex: /https?:\/\/[^\s<>\"']+/g,
        type: "url"
      },
      number: {
        regex: /\b\d+(?:\.\d+)?\b/g,
        type: "number"
      },
      phone: {
        regex: /\+?[0-9]{1,4}?[-.\s]?\(?[0-9]{1,4}\)?[-.\s]?[0-9]{1,4}[-.\s]?[0-9]{1,9}/g,
        type: "phone"
      },
      capitalized: {
        regex: /\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b/g,
        type: "capitalized"
      }
    };
  }

  extract(text) {
    if (!text) return [];
    
    const entities = [];
    const seen = new Set();
    
    for (const [name, pattern] of Object.entries(this.patterns)) {
      const matches = text.matchAll(pattern.regex);
      for (const match of matches) {
        const value = match[0];
        const key = `${name}:${value}`;
        if (!seen.has(key)) {
          seen.add(key);
          entities.push({
            type: pattern.type,
            value: value
          });
        }
      }
    }
    
    return entities;
  }
}
