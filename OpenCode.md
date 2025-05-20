# Claude Code SDK Development Guide

## Commands
- Build TypeScript: `npm run build`
- Watch mode: `npm run build:dev`
- Test all: `npm run test`
- Test single file: `npx vitest run src/tests/file.test.ts`
- Lint: `npm run lint`
- Format check: `npm run format`
- Format fix: `npm run format:fix`
- Type check: `npm run typecheck`
- Python install: `pip install -e ./python`
- Python test: `pytest python/tests`

## Code Style
- **TypeScript**:
  - No semicolons, single quotes, 100 char line limit, 2-space indentation
  - Explicit function return types, no `any` type
  - camelCase for variables/functions, PascalCase for classes/interfaces
  - Use `createError` method with proper status codes
  - Named exports preferred over default exports
  - ESM modules (type: "module" in package.json)

- **Python**:
  - Follow PEP 8 style guide
  - Use type hints for all functions and methods
  - Use docstrings for all public functions and classes
  - snake_case for variables/functions, PascalCase for classes
  - Proper error handling with status codes
  - Async/await for streaming operations