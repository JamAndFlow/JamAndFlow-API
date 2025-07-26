# Contribution Guide

Thank you for your interest in contributing to JamAndFlow-API! Please follow these steps to ensure a smooth workflow and maintain code quality.

## 1. Fork & Clone
- Fork the repository on GitHub.
- Clone your fork locally:
  ```bash
  git clone <your-fork-url>
  cd JamAndFlow-API
  ```

## 2. Set Up Environment
- Follow the setup instructions in `local_setup.md` to create and activate a Python virtual environment.
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## 3. Pre-commit Hooks
- Install pre-commit:
  ```bash
  pip install pre-commit
  pre-commit install
  ```
- Run pre-commit checks before pushing:
  ```bash
  pre-commit run --all-files
  ```

## 4. Linting
- Ensure code style with flake8 or black:
  ```bash
  pip install flake8 black
  flake8 .
  black .
  ```

## 5. Testing
- Run tests (add your test commands here, e.g. pytest):
  ```bash
  pip install pytest
  pytest
  ```

## 6. Workflow
1. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes and commit with clear messages.
3. Ensure all tests pass and code is linted.
4. Push your branch and open a Pull Request.

## 7. Docker & Database
- Use Docker for local development as described in `local_setup.md`.
- For database migrations, see the migration section in `local_setup.md`.
- For inspecting tables, see the Postgres section in `local_setup.md`.

## 8. Code Review
- All contributions are reviewed before merging.
- Address any requested changes promptly.

---

For more details, refer to `local_setup.md`.
