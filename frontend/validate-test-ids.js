#!/usr/bin/env node

/**
 * Validation script to check that required test IDs are present in components
 * 
 * Usage: node validate-test-ids.js
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Required test IDs for case management tests
const requiredTestIds = [
  // Case List
  'case-card',
  'case-title', 
  'case-status',
  'case-client',
  'case-type',
  'case-created-date',
  'case-parties',
  'case-document-count',
  'case-playbook',
  'case-summary',
  'cases-grid',
  
  // Case Detail
  'case-overview',
  'key-parties-section',
  'documents-section',
  'analysis-status-indicators',
  'total-document-count',
  'analysis-completion-status',
  'analysis-progress-bar',
  'document-link',
  'document-analysis-status',
  
  // Shared Layout
  'page-title',
  'page-subtitle',
  'search-input',
  'back-button',
  
  // Loading and Error States
  'loading-spinner',
  'error-message'
];

// Files to check
const filesToCheck = [
  'src/components/CaseManagement/CaseList.tsx',
  'src/components/CaseManagement/CaseDetail.tsx',
  'src/components/layout/SharedLayout.tsx'
];

console.log('🔍 Validating test IDs in components...\n');

let allTestIdsFound = true;
const foundTestIds = new Set();
const missingTestIds = [];

// Check each file
filesToCheck.forEach(filePath => {
  const fullPath = path.join(__dirname, filePath);
  
  if (!fs.existsSync(fullPath)) {
    console.log(`❌ File not found: ${filePath}`);
    allTestIdsFound = false;
    return;
  }
  
  const content = fs.readFileSync(fullPath, 'utf8');
  console.log(`📄 Checking ${filePath}:`);
  
  // Find all test IDs in this file
  const testIdMatches = content.match(/data-testid="([^"]+)"/g) || [];
  const fileTestIds = testIdMatches.map(match => match.match(/data-testid="([^"]+)"/)[1]);
  
  fileTestIds.forEach(testId => {
    foundTestIds.add(testId);
    console.log(`  ✅ ${testId}`);
  });
  
  if (fileTestIds.length === 0) {
    console.log(`  ⚠️  No test IDs found in this file`);
  }
  
  console.log('');
});

// Check for missing required test IDs
requiredTestIds.forEach(testId => {
  if (!foundTestIds.has(testId)) {
    missingTestIds.push(testId);
    allTestIdsFound = false;
  }
});

// Report results
console.log('📊 Validation Results:');
console.log(`  Found test IDs: ${foundTestIds.size}`);
console.log(`  Required test IDs: ${requiredTestIds.length}`);

if (missingTestIds.length > 0) {
  console.log(`\n❌ Missing required test IDs:`);
  missingTestIds.forEach(testId => {
    console.log(`  - ${testId}`);
  });
}

// Check for extra test IDs (not required but present)
const extraTestIds = Array.from(foundTestIds).filter(testId => !requiredTestIds.includes(testId));
if (extraTestIds.length > 0) {
  console.log(`\n📝 Additional test IDs found:`);
  extraTestIds.forEach(testId => {
    console.log(`  + ${testId}`);
  });
}

if (allTestIdsFound && missingTestIds.length === 0) {
  console.log('\n✅ All required test IDs are present!');
  console.log('🚀 Components are ready for E2E testing.');
} else {
  console.log('\n❌ Some required test IDs are missing.');
  console.log('💡 Add the missing test IDs to the components before running E2E tests.');
}

process.exit(allTestIdsFound && missingTestIds.length === 0 ? 0 : 1);