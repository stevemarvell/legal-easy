#!/usr/bin/env node

/**
 * Simple test runner for Case Management Cucumber tests
 * 
 * Usage:
 *   node run-case-tests.js
 *   npm run test:e2e:cases
 */

import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🧪 Running Case Management E2E Tests...\n');

// Run Cypress with the case management feature
const cypress = spawn('npx', [
  'cypress', 
  'run',
  '--spec', 
  'cypress/cucumber/features/case-management.feature',
  '--browser', 
  'chrome',
  '--headless'
], {
  cwd: __dirname,
  stdio: 'inherit'
});

cypress.on('close', (code) => {
  if (code === 0) {
    console.log('\n✅ All Case Management tests passed!');
  } else {
    console.log('\n❌ Some tests failed. Check the output above for details.');
  }
  process.exit(code);
});

cypress.on('error', (err) => {
  console.error('❌ Failed to start Cypress:', err);
  process.exit(1);
});