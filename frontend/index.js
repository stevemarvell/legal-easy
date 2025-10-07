const { spawn } = require('child_process');

const port = process.env.PORT || 3000;

console.log(`Starting static server on port ${port}...`);

// First, build the project
console.log('Building project...');
const build = spawn('npm', ['run', 'build'], {
  stdio: 'inherit',
  shell: true
});

build.on('exit', (buildCode) => {
  if (buildCode !== 0) {
    console.error('Build failed');
    process.exit(buildCode);
  }
  
  console.log('Build complete, starting server...');
  
  // Then start the server
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
});