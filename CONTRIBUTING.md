# Contributing to X12-837-Fake-Data-Generator

Thank you for your interest in contributing to the X12-837-Fake-Data-Generator project! This document provides guidelines for contributing to this open-source healthcare informatics toolkit.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Questions](#questions)

---

## Code of Conduct

### Our Pledge

We as members, contributors, and leaders pledge to make participation in our community a harassment-free experience for everyone, regardless of age, body size, visible or invisible disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

We pledge to act and interact in ways that contribute to an open, welcoming, diverse, inclusive, and healthy community.

### Our Standards

Examples of behavior that contributes to a positive environment:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior:

- The use of sexualized language or imagery and unwelcome sexual attention or advances
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project maintainer at hantsawilliams@gmail.com. All complaints will be reviewed and investigated promptly and fairly.

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, issues, and other contributions that do not align with this Code of Conduct.

---

## How Can I Contribute?

### Types of Contributions

We welcome contributions in many forms:

1. **Bug Reports**: Report issues you encounter while using the toolkit
2. **Feature Requests**: Suggest new features or enhancements
3. **Code Contributions**: Submit bug fixes, new features, or improvements
4. **Documentation**: Improve README, code comments, or create tutorials
5. **Testing**: Add unit tests or integration tests
6. **Educational Content**: Create examples, tutorials, or teaching materials

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git installed on your system
- Familiarity with X12 EDI standards (helpful but not required)
- Understanding of healthcare claims (helpful but not required)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/YOUR-USERNAME/x12-837-fake-data-generator.git
cd x12-837-fake-data-generator
```

3. Add the upstream repository:

```bash
git remote add upstream https://github.com/hantswilliams/x12-837-fake-data-generator.git
```

### Set Up Development Environment

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Test the installation:

```bash
# Test generator
python -m generator_837.cli.main -n 1 -o test_output/

# Test parser
python -m parser_837.cli.main -i test_output/ -o test_parsed/
```

---

## Development Workflow

### Branching Strategy

- `main` branch: Stable, production-ready code
- `develop` branch: Integration branch for features (if it exists)
- Feature branches: `feature/description-of-feature`
- Bug fix branches: `fix/description-of-bug`

### Making Changes

1. Create a new branch from `main`:

```bash
git checkout main
git pull upstream main
git checkout -b feature/my-new-feature
```

2. Make your changes and commit them:

```bash
git add .
git commit -m "Add feature: description of changes"
```

3. Keep your branch up to date:

```bash
git fetch upstream
git rebase upstream/main
```

4. Push your changes:

```bash
git push origin feature/my-new-feature
```

---

## Coding Standards

### Python Style Guide

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Maximum line length: 100 characters (flexible for readability)

### Code Organization

- Place generator code in `generator_837/` directory
- Place parser code in `parser_837/` directory
- Keep web/API code in respective `web/` and `api/` subdirectories

### Documentation

- Add docstrings to all public functions and classes:

```python
def generate_claim(num_diagnoses: int, num_service_lines: int) -> str:
    """
    Generate a synthetic X12 837 claim transaction.

    Args:
        num_diagnoses: Number of diagnosis codes to include (3-8)
        num_service_lines: Number of service line items (1-5)

    Returns:
        String containing complete X12 837 transaction

    Raises:
        ValueError: If parameters are out of valid range
    """
    pass
```

- Comment complex logic inline
- Update README.md if adding new features

### Security Considerations

- Never commit real PHI (Protected Health Information)
- Validate all user inputs
- Avoid hardcoding credentials or API keys
- Use environment variables for sensitive configuration

---

## Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_generator.py

# Run with coverage
pytest --cov=generator_837 --cov=parser_837
```

### Writing Tests

- Place tests in `tests/` directory
- Name test files: `test_<module_name>.py`
- Name test functions: `test_<functionality>()`

Example test structure:

```python
# tests/test_generator.py
import pytest
from generator_837.core.generator import generate_claim

def test_generate_claim_basic():
    """Test basic claim generation."""
    claim = generate_claim(num_diagnoses=5, num_service_lines=2)
    assert claim is not None
    assert "ISA*" in claim  # Check for X12 envelope
    assert "ST*837*" in claim  # Check for 837 transaction set

def test_generate_claim_invalid_params():
    """Test that invalid parameters raise ValueError."""
    with pytest.raises(ValueError):
        generate_claim(num_diagnoses=0, num_service_lines=10)
```

### Test Coverage

- Aim for at least 70% code coverage
- Prioritize testing core functionality (generation and parsing)
- Include edge cases and error handling

---

## Submitting Changes

### Pull Request Process

1. **Update Documentation**: Ensure README and code comments are current
2. **Add Tests**: Include tests for new features or bug fixes
3. **Run Tests**: Verify all tests pass locally
4. **Update Changelog**: Add entry to CHANGELOG.md (if it exists)
5. **Create Pull Request**:
   - Use a clear, descriptive title
   - Reference any related issues (#123)
   - Describe what changed and why
   - Include screenshots for UI changes

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Related Issues
Fixes #(issue number)

## Testing
Describe testing performed:
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] All tests pass locally

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] Tests added for new functionality
- [ ] No breaking changes (or documented if unavoidable)
```

### Review Process

1. Maintainer will review your pull request
2. Address any requested changes
3. Once approved, changes will be merged
4. Your contribution will be acknowledged in release notes

---

## Reporting Bugs

### Before Submitting a Bug Report

- Check existing issues to avoid duplicates
- Update to the latest version and test if bug persists
- Collect relevant information (error messages, logs, environment)

### How to Submit a Bug Report

Create a GitHub issue with the following information:

**Title**: Clear, descriptive summary (e.g., "Parser fails on claims with 8+ diagnoses")

**Bug Report Template**:

```markdown
## Bug Description
A clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Run command '...'
3. See error

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Environment
- OS: [e.g., macOS 14.0, Windows 11, Ubuntu 22.04]
- Python version: [e.g., 3.11.5]
- Package version: [e.g., 1.0.0]

## Additional Context
- Error messages/logs
- Screenshots (if applicable)
- Sample files (if applicable, ensure no real PHI)
```

---

## Suggesting Enhancements

### Before Submitting an Enhancement

- Check if the feature already exists
- Review existing feature requests
- Consider if it aligns with project goals

### How to Submit an Enhancement Request

Create a GitHub issue with the following:

**Title**: Clear, descriptive summary (e.g., "Add support for 837P professional claims")

**Feature Request Template**:

```markdown
## Feature Description
Clear description of the proposed feature

## Use Case
Who would benefit and how?

## Proposed Solution
How you envision this working

## Alternatives Considered
Other approaches you've thought about

## Additional Context
- Related standards/specifications
- Example implementations
- Mockups or diagrams (if applicable)
```

---

## Questions

### Where to Ask

- **General Questions**: Open a GitHub Discussion or Issue
- **Bug Reports**: GitHub Issues
- **Private/Sensitive**: Email hantsawilliams@gmail.com
- **Documentation**: Check README.md and code comments first

### Getting Help

If you're stuck:
1. Review the README.md and inline documentation
2. Check existing GitHub issues and discussions
3. Review X12 837 implementation guide (005010X223A2)
4. Ask for help by opening a discussion

---

## Recognition

Contributors will be acknowledged in:
- Repository README.md
- Release notes
- Academic publications (where appropriate)

Thank you for contributing to healthcare informatics education and open-source software!

---

## Additional Resources

- **X12 Standards**: http://www.x12.org/
- **CMS EDI Resources**: https://www.cms.gov/Regulations-and-Guidance/Administrative-Simplification/
- **HIPAA EDI**: https://www.hhs.gov/hipaa/for-professionals/special-topics/edi/index.html
- **Python Testing**: https://docs.pytest.org/

---

## License

By contributing to this project, you agree that your contributions will be licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0). See the LICENSE file for details.

For commercial use inquiries, contact the project maintainer.
