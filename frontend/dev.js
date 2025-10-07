#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

console.log('Starting frontend development...');
console.log('- TypeScript compiler in watch mode');
console.log('- Static server on http://localhost:8080');
console.log('Press Ctrl+C to stop both');

// Start TypeScript compiler in watch mode
const tsc = spawn('npx', ['tsc', '--watch'], {
    stdio: ['inherit', 'pipe', 'pipe'],
    shell: true
});

// Start static server
const serve = spawn('npx', ['serve', 'public', '-p', '8080'], {
    stdio: ['inherit', 'pipe', 'pipe'],
    shell: true
});

// Handle TypeScript compiler output
tsc.stdout.on('data', (data) => {
    console.log(`[TSC] ${data.toString().trim()}`);
});

tsc.stderr.on('data', (data) => {
    console.error(`[TSC Error] ${data.toString().trim()}`);
});

// Handle server output
serve.stdout.on('data', (data) => {
    console.log(`[Server] ${data.toString().trim()}`);
});

serve.stderr.on('data', (data) => {
    console.error(`[Server Error] ${data.toString().trim()}`);
});

// Handle process termination
process.on('SIGINT', () => {
    console.log('\nShutting down development servers...');
    tsc.kill();
    serve.kill();
    process.exit(0);
});

// Handle child process exits
tsc.on('exit', (code) => {
    if (code !== 0) {
        console.log(`TypeScript compiler exited with code ${code}`);
    }
});

serve.on('exit', (code) => {
    if (code !== 0) {
        console.log(`Static server exited with code ${code}`);
    }
});