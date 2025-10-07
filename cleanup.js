#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🧹 Cleaning up project...');

// Clean backend
console.log('Cleaning backend...');
try {
  if (fs.existsSync('backend/__pycache__')) {
    fs.rmSync('backend/__pycache__', { recursive: true, force: true });
    console.log('✓ Removed Python cache files');
  }
} catch (err) {
  console.log('⚠️ Could not clean backend cache:', err.message);
}

// Clean frontend
console.log('Cleaning frontend...');
try {
  execSync('npm run clean', { cwd: 'frontend', stdio: 'inherit' });
  console.log('✓ Cleaned frontend build files');
} catch (err) {
  console.log('⚠️ Could not clean frontend:', err.message);
}

// Clean IDE files
console.log('Cleaning IDE files...');
const ideFiles = ['.idea', '.vscode', '*.sublime-*'];
ideFiles.forEach(pattern => {
  try {
    if (fs.existsSync(pattern)) {
      fs.rmSync(pattern, { recursive: true, force: true });
      console.log(`✓ Removed ${pattern}`);
    }
  } catch (err) {
    console.log(`⚠️ Could not remove ${pattern}:`, err.message);
  }
});

console.log('✨ Cleanup complete!');