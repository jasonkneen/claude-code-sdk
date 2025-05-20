#!/usr/bin/env node

/**
 * This script prepares the package for publishing by:
 * 1. Cleaning the dist directory
 * 2. Running the build
 * 3. Copying additional files to the dist directory
 */

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';

// Get __dirname equivalent in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Paths
const rootDir = path.resolve(__dirname, '..');
const distDir = path.join(rootDir, 'dist');

// Make sure dist directory exists
if (!fs.existsSync(distDir)) {
  fs.mkdirSync(distDir, { recursive: true });
}

console.log('Building package...');
try {
  execSync('npm run build', { stdio: 'inherit', cwd: rootDir });
} catch (error) {
  console.error('Build failed:', error);
  process.exit(1);
}

// Files to copy to dist
const filesToCopy = [
  'README.md',
  'LICENSE',
  'package.json'
];

console.log('Copying package files to dist...');
filesToCopy.forEach(file => {
  const srcPath = path.join(rootDir, file);
  const destPath = path.join(distDir, file);
  
  if (fs.existsSync(srcPath)) {
    fs.copyFileSync(srcPath, destPath);
    console.log(`Copied ${file} to dist`);
  } else {
    console.warn(`Warning: ${file} not found`);
  }
});

// Create a LICENSE file if it doesn't exist
if (!fs.existsSync(path.join(rootDir, 'LICENSE'))) {
  console.log('Creating LICENSE file...');
  const licenseContent = `MIT License

Copyright (c) ${new Date().getFullYear()}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.`;

  fs.writeFileSync(path.join(rootDir, 'LICENSE'), licenseContent);
  fs.copyFileSync(path.join(rootDir, 'LICENSE'), path.join(distDir, 'LICENSE'));
  console.log('Created and copied LICENSE file');
}

// Create a package.json for the dist directory
const packageJson = JSON.parse(fs.readFileSync(path.join(rootDir, 'package.json'), 'utf8'));

// Remove development-only properties
delete packageJson.devDependencies;
delete packageJson.scripts;

// Update paths
packageJson.main = 'index.js';
packageJson.types = 'index.d.ts';

// Write the modified package.json to dist
fs.writeFileSync(
  path.join(distDir, 'package.json'),
  JSON.stringify(packageJson, null, 2)
);

console.log('Package is ready for publishing!');
console.log('To publish, run: cd dist && npm publish');