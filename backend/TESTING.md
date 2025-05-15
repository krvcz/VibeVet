# Testing Guide for VibeVet AI Backend

This document outlines how to run tests and maintain testing standards for the VibeVet AI backend.

## Setup

1. Install test dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

### All Tests

Run all tests:
```bash
pytest
```

### With Coverage

Run tests with coverage reporting:
```bash
pytest --cov=. --cov-report=html
```

This will generate an HTML report in the `htmlcov` directory.

### Run Specific Test Categories

Run only unit tests:
```bash
pytest -m unit
```

Run only integration tests:
```bash
pytest -m integration
```

Run only end-to-end tests:
```bash
pytest -m e2e
```

Run tests for a specific app:
```bash
pytest users/
```

Run a specific test file:
```bash
pytest users/tests/test_models.py
```

Run a specific test class:
```bash
pytest users/tests/test_models.py::TestUserModel
```

Run a specific test method:
```bash
pytest users/tests/test_models.py::TestUserModel::test_create_user
```

## Testing Standards

1. **Test Coverage:** Aim for at least 80% code coverage across the project.
2. **Test Organization:** 
   - Place tests in a `tests` directory within each Django app
   - Use meaningful test class and method names that describe what's being tested
   - Group tests logically by functionality
3. **Test Isolation:** Tests should be independent and not rely on external services or the state from other tests.
4. **Test Data:** Use factory_boy to generate test data when possible.
5. **Test Speed:** Avoid slow tests if possible, mark unavoidably slow tests with `@pytest.mark.slow`.

## Writing New Tests

When adding new functionality:
1. Write tests first (TDD approach)
2. Ensure tests are comprehensive and cover edge cases
3. Follow the existing test structure and naming conventions
4. Add proper docstrings to test methods explaining what they test

## CI/CD Integration

Tests run automatically on GitHub Actions:
- On pushes to main and develop branches
- On pull requests to main and develop branches

Refer to the `.github/workflows/django-tests.yml` file for CI configuration details. 