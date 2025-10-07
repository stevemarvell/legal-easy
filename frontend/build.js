#!/usr/bin/env node

const fs = require('fs');
const { execSync } = require('child_process');

// Build TypeScript
console.log('Building TypeScript...');
execSync('tsc', { stdio: 'inherit' });

// Inject environment variables into the built JS
const jsFile = 'public/main.js';
if (fs.existsSync(jsFile)) {
  let content = fs.readFileSync(jsFile, 'utf8');
  
  // Inject backend URL as a window variable
  if (process.env.BACKEND_URL) {
    console.log(`Injecting BACKEND_URL: ${process.env.BACKEND_URL}`);
    // Add the backend URL to the top of the file
    content = `window.BACKEND_URL = "${process.env.BACKEND_URL}";\n` + content;
  }
  
  fs.writeFileSync(jsFile, content);
  console.log('Build complete!');
} else {
  console.error('Built JS file not found!');
  process.exit(1);
}