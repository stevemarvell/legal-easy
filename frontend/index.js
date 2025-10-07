#!/usr/bin/env node

// Simple server for Railway deployment
const { spawn } = require('child_process');

const port = process.env.PORT || 3000;

console.log(`Starting static server on port ${port}...`);

const serve = spawn('npx', ['serve', 'public', '-p', port], {
  stdio: 'inherit',
  shell: true
});

serve.on('exit', (code) => {
  console.log(`Server exited with code ${code}`);
  process.exit(code);
});

process.on('SIGINT', () => {
  console.log('Shutting down server...');
  serve.kill();
});

process.on('SIGTERM', () => {
  console.log('Shutting down server...');
  serve.kill();
});