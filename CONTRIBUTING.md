# Contributing

## Instruction Guard Rule
Any change to application code (`app/**` or `main.py`) that alters:
- Models / fields / enums
- Endpoints / paths / query parameters
- Seeding logic
- Directory/file layout
- Required dependencies or versions

MUST update both:
- `.github/application-setup.yml`
- `.cursor/rules/application-setup.mdc`

Include the change in the same commit. Increment `guard_version` if the spec meaningfully changes.

## Pre-Commit Setup
Install pre-commit locally to enforce the guard:
```bash
pip install pre-commit
pre-commit install
```
Now commits touching code without spec updates will fail.

## CI Enforcement
GitHub Actions workflow `instruction-guard.yml` runs on push and PR to ensure instruction files were updated alongside code changes.

## Updating Instructions
1. Edit both instruction files.
2. Adjust directory layout, endpoints, enum lists, and example curl commands.
3. Increment `guard_version` value.
4. Commit changes with code.

## Why This Exists
Keeps AI-assisted regeneration prompts synchronized with the real codebase to avoid drift and incorrect scaffolding during future automation sessions.

## Additional Recommendations
- After large refactors, manually review curl examples.
- Keep filenames consistent; if you rename legacy `item.py`, update the spec accordingly.
- Add migrations for DB schema changes and reference them in instruction files.

Happy contributing!
