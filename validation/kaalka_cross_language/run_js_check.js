
const { encryptValue } = require('./kaalka.js');
const fs = require('fs');
const fixtures = JSON.parse(fs.readFileSync('fixtures.json','utf8'));
const out = {};
for (const v of fixtures.vectors) {
  const e1 = encryptValue(v.plaintext, v.key);
  const e2 = encryptValue(v.plaintext, v.key);
  out[v.id] = { stable: e1 === e2, encrypted: e1 };
}
console.log(JSON.stringify(out));
