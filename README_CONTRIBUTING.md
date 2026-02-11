# Contributing Guide

Thanks for contributing to Aadhaar Insight AI! This file describes the process for contributing code, reporting bugs, and submitting enhancements.

## How to Contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/<short-description>`
3. Commit changes with clear messages
4. Push your branch and open a Pull Request (PR) against `main`

## Branching & Naming
- Feature branches: `feat/<short>`
- Bugfix branches: `fix/<short>`
- Docs: `docs/<short>`
- Hotfix: `hotfix/<short>`

## Code Style
- Follow PEP8 for Python.
- Use 4-space indentation.
- Keep functions small and focused.
- Add type hints where helpful.

## Testing
- Add tests for non-trivial logic using `pytest`.
- Run tests locally before opening PRs.

## Pull Request Checklist
- [ ] Title follows pattern: `[Area] Short description`
- [ ] Link to issue (if any)
- [ ] Tests added / updated
- [ ] Linting passed
- [ ] Docs updated if behavior changed

## Formatting & Linting
- Tools recommended:
  - `black` for formatting
  - `flake8` for linting

Example commands:

```bash
pip install black flake8
black .
flake8 .
```

## Issue Reporting
- Provide minimal reproducible example.
- Include dataset sample (if possible) or a description.
- Provide environment details (Python version, OS).

## Reviews
- At least one maintainer review required before merge.
- Resolve inline comments by updating the branch.

## License
- Document project license in `LICENSE` (if applicable).

---

If you'd like, I can add a PR template and a pre-commit config to automate formatting.