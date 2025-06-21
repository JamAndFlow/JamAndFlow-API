# Setting Up and Running Pre-commit Hooks

# Setting Up and Running Pre-commit Hooks

1. Install pre-commit if you haven't already:
   ```bash
   pip install pre-commit

2. install pre-commit hooks:
   ```bash
   pre-commit install
   ```

3. stage your changes: and run `pre-commit` to check if your staged files pass the checks.

4. Run pre-commit to check your every files:
   ```bash
   pre-commit run --all-files
   ```

### To update pre-commit hooks:
```bash
pre-commit autoupdate
```
