#!/bin/bash

# Script to build and publish the package

# Ensure we're running from the correct directory
cd "$(dirname "$0")/.." || exit 1

# Check if NPM_TOKEN is set
if [ -z "$NPM_TOKEN" ]; then
  echo "Error: NPM_TOKEN environment variable is not set"
  exit 1
fi

# Clean the dist directory
rm -rf dist

# Run tests
npm test

# Run linting and type checking
npm run lint
npm run typecheck

# Build the package
npm run build

# Create .npmrc file with auth token
echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > .npmrc

# Publish the package
npm publish --access public

# Remove .npmrc
rm .npmrc

echo "Package published successfully!"