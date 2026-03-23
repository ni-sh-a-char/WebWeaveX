#!/usr/bin/env node
/** Node.js validation script - exports outputs for comparison */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { WebWeaveX } from './lib/client.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const TEST_CASES_PATH = join(__dirname, '..', '..', 'core', 'test_cases', 'test_cases.json');
const OUTPUT_DIR = join(__dirname, '..', '..', 'test_output', 'node');

function exportNodeOutputs() {
  if (!existsSync(TEST_CASES_PATH)) {
    console.error(`Test cases not found: ${TEST_CASES_PATH}`);
    process.exit(1);
  }

  mkdirSync(OUTPUT_DIR, { recursive: true });

  const testCases = JSON.parse(readFileSync(TEST_CASES_PATH, 'utf-8'));
  const wx = new WebWeaveX();

  console.log('Exporting Node.js outputs...');
  console.log('='.repeat(50));

  for (const tc of testCases) {
    const name = tc.name;
    const inputText = tc.input;

    console.log(`Processing: ${name}`);

    const result = wx.extract(inputText);
    const output = result;

    const outputPath = join(OUTPUT_DIR, `${name}.json`);
    writeFileSync(outputPath, JSON.stringify(output, null, 2), 'utf-8');

    console.log(`  Saved: ${outputPath}`);
  }

  console.log('='.repeat(50));
  console.log(`Exported ${testCases.length} test cases to ${OUTPUT_DIR}`);

  const manifestPath = join(OUTPUT_DIR, 'manifest.json');
  writeFileSync(manifestPath, JSON.stringify({
    language: 'node',
    test_cases: testCases.map(tc => tc.name)
  }, null, 2), 'utf-8');
  console.log(`Manifest: ${manifestPath}`);
}

exportNodeOutputs();
