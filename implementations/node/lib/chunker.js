/** Text chunker - sliding window chunking */

export class Chunker {
  constructor(config = {}) {
    this.size = 500;
    this.overlap = 50;
    this.preserveWords = true;
  }

  chunk(text) {
    if (!text || text.length === 0) return [];
    
    const chunks = [];
    let start = 0;
    let index = 0;
    
    while (start < text.length) {
      let end = start + this.size;
      
      if (this.preserveWords && end < text.length) {
        end = this._findWordBoundary(text, end);
      }
      
      const chunkText = text.substring(start, end);
      if (chunkText.trim()) {
        chunks.push({
          text: chunkText,
          index: index,
          start: start,
          end: end
        });
        index++;
      }
      
      start = end - this.overlap;
      if (start < 0) start = 0;
    }
    
    return chunks;
  }

  _findWordBoundary(text, position) {
    if (position >= text.length) return position;
    
    for (let i = position; i > Math.max(0, position - 50); i--) {
      if (text[i] === ' ' || text[i] === '\t' || text[i] === '\n' || text[i] === '\r') {
        return i;
      }
    }
    
    return position;
  }
}
