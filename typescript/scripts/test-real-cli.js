#!/usr/bin/env node

// This script tests the actual CLI interaction to verify it works correctly

const { spawn } = require('child_process');
const { exec } = require('child_process');

// Check if the claude CLI is installed
exec('which claude || echo "not-found"', (error, stdout, stderr) => {
  if (error) {
    console.error('Error checking for Claude CLI:', error);
    return;
  }

  if (stdout.trim() === 'not-found') {
    console.error('\x1b[31mERROR: Claude CLI not found in PATH\x1b[0m');
    console.log('Please install the Claude CLI first:');
    console.log('npm install -g @anthropic-ai/claude-code');
    return;
  }

  console.log(`\x1b[32mFound Claude CLI at: ${stdout.trim()}\x1b[0m`);

  // Test a simple command to verify CLI works
  console.log('\nTesting basic CLI functionality...');
  const claudeProcess = spawn('claude', ['-h'], { stdio: 'pipe' });

  let output = '';

  claudeProcess.stdout.on('data', (data) => {
    output += data.toString();
  });

  claudeProcess.stderr.on('data', (data) => {
    console.error(`\x1b[31mCLI Error: ${data.toString()}\x1b[0m`);
  });

  claudeProcess.on('close', (code) => {
    if (code === 0) {
      console.log('\x1b[32mBasic CLI functionality works!\x1b[0m');
      console.log('Sample CLI help output:');
      console.log('-'.repeat(50));
      console.log(output.split('\n').slice(0, 10).join('\n') + '\n...');
      console.log('-'.repeat(50));
      console.log('\nYour Claude Code SDK wrapper should be able to interact with the CLI.');
      console.log('\nNext steps:');
      console.log('1. Build the TypeScript wrapper: npm run build');
      console.log('2. Run a test example: node dist/examples/basic.js');
    } else {
      console.error(`\x1b[31mCLI test failed with code ${code}\x1b[0m`);
      console.log('Please ensure the Claude CLI is correctly installed and working.');
    }
  });
});