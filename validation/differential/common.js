const path = require('path');
const fs = require('fs');

function loadVectorFamily(family) {
  const dir = path.join('validation', 'vectors', family);
  const canonPath = path.join(dir, 'canonical.json');
  if (!fs.existsSync(canonPath)) {
    return { source: 'webweavex-spec', vectors: [], skip: true };
  }
  const data = JSON.parse(fs.readFileSync(canonPath, 'utf-8'));
  return { source: data.source || 'webweavex-spec', vectors: data.vectors || [], skip: false };
}

module.exports = { loadVectorFamily };
