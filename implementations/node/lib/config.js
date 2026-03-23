/** Default configuration - mirrors Python DEFAULT_CONFIG */

export const DEFAULT_CONFIG = {
  version: "1.0.0",
  meta: {
    url: "",
    title: ""
  },
  fetch: {
    timeout: 10,
    retries: 3,
    retryDelay: 1,
    retryBackoff: 2,
    userAgent: "WebWeaveX/1.0 (Node.js Library)"
  },
  parse: {
    extractVisibleText: true,
    removeScripts: true,
    removeStyles: true,
    removeComments: true,
    removeHidden: true
  },
  clean: {
    normalizeWhitespace: true,
    strip: true,
    removeEmptyLines: true,
    lowercase: false
  },
  chunking: {
    size: 500,
    overlap: 50,
    method: "sliding_window",
    preserveWords: true
  },
  entityPatterns: {
    email: {
      regex: "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
      type: "email"
    },
    url: {
      regex: "https?://[^\\s<>\"']+",
      type: "url"
    },
    number: {
      regex: "\\b\\d+(?:\\.\\d+)?\\b",
      type: "number"
    },
    phone: {
      regex: "\\+?[0-9]{1,4}?[-.\\s]?\\(?[0-9]{1,4}\\)?[-.\\s]?[0-9]{1,4}[-.\\s]?[0-9]{1,9}",
      type: "phone"
    },
    capitalized: {
      regex: "\\b[A-Z][a-z]+(?:\\s+[A-Z][a-z]+)*\\b",
      type: "capitalized"
    }
  },
  graph: {
    edgeRule: "cooccurrence",
    nodeTypes: ["email", "url", "number", "capitalized", "phone"],
    minOccurrence: 1,
    directed: false
  },
  relations: {
    enabled: true,
    withinChunks: true,
    edgeType: "cooccurrence"
  },
  insights: {
    enabled: true,
    topEntitiesCount: 10,
    includeStats: true
  }
};

export function getConfig(overrides = {}) {
  return deepMerge(DEFAULT_CONFIG, overrides);
}

function deepMerge(base, overrides) {
  const result = { ...base };
  for (const key in overrides) {
    if (typeof overrides[key] === 'object' && !Array.isArray(overrides[key]) && overrides[key] !== null) {
      result[key] = deepMerge(base[key] || {}, overrides[key]);
    } else {
      result[key] = overrides[key];
    }
  }
  return result;
}
