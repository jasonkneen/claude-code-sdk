# Contributing to Claude Code SDK (TypeScript)

Thank you for your interest in contributing to the Claude Code SDK! This document provides guidelines and instructions for contributing to the TypeScript implementation.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## Getting Started

1. **Fork the repository** and clone it locally
2. **Install dependencies**:
   ```bash
   npm install
   ```
3. **Build the project**:
   ```bash
   npm run build
   ```
4. **Run tests**:
   ```bash
   npm run test
   ```

## Development Workflow

1. **Create a branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines

3. **Write tests** for your changes

4. **Run linting and type checking**:
   ```bash
   npm run lint
   npm run typecheck
   ```

5. **Format your code**:
   ```bash
   npm run format:fix
   ```

6. **Commit your changes** with a descriptive commit message

7. **Push your branch** and submit a pull request

## Code Style Guidelines

- Follow the existing code style (no semicolons, single quotes, 2-space indentation)
- Use explicit function return types
- Avoid using `any` type
- Use camelCase for variables/functions and PascalCase for classes/interfaces
- Write comprehensive JSDoc comments for public APIs
- Use named exports rather than default exports
- Follow ESM module patterns

## Testing

- Write unit tests for all new functionality
- Ensure all tests pass before submitting a pull request
- Mock external dependencies in tests

## Documentation

- Update documentation for any changed functionality
- Document all public APIs with JSDoc comments
- Include examples for new features

## Pull Request Process

1. Ensure your code follows the style guidelines
2. Update the README.md with details of changes if appropriate
3. The PR should work on the main branch
4. Include a description of the changes in your PR

## Release Process

Releases are managed by the maintainers. The general process is:

1. Update version in package.json
2. Update CHANGELOG.md
3. Create a new release on GitHub

## Getting Help

If you have questions or need help, please open an issue on GitHub.

Thank you for contributing to the Claude Code SDK!