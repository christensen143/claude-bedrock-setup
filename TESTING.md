# Testing Documentation for claude-setup CLI

This document describes the comprehensive test suite for the claude-setup CLI application.

## Test Coverage

The test suite achieves **98% code coverage**, exceeding the target of 95%. The only uncovered lines are:
- Lines 74-76 in `cli.py`: KeyboardInterrupt handling (edge case)
- Line 137 in `cli.py`: `if __name__ == '__main__'` block

## Test Structure

```
tests/
├── __init__.py                 # Test package marker
├── conftest.py                 # Pytest configuration and shared fixtures
├── test_auth_checker.py        # Tests for AWS authentication checking
├── test_aws_client.py          # Tests for AWS Bedrock client
├── test_cli.py                 # Tests for CLI commands and integration
├── test_config_manager.py      # Tests for configuration management
├── test_gitignore_manager.py   # Tests for .gitignore management
├── test_integration.py         # End-to-end integration tests
└── test_utils.py               # Test utilities and helper functions
```

## Test Categories

### Unit Tests

#### `test_auth_checker.py`
- Tests for AWS authentication verification
- Covers all error conditions: CalledProcessError, FileNotFoundError, PermissionError, TimeoutExpired
- Mocks subprocess calls to avoid actual AWS API calls

#### `test_aws_client.py`  
- Tests for BedrockClient class and Claude model listing
- Comprehensive error handling: access denied, authentication errors, JSON parsing errors
- Tests model filtering (only Claude models) and sorting
- Mocks subprocess calls to AWS CLI

#### `test_config_manager.py`
- Tests for configuration file management in `.claude/settings.local.json`
- Covers file creation, loading, updating, and deletion
- Tests error conditions: permission errors, corrupted JSON, IO errors
- Mocks file system operations

#### `test_gitignore_manager.py`
- Tests for automatic .gitignore management
- Covers all scenarios: new file, existing file, pattern already present
- Tests edge cases: whitespace-only files, files without trailing newlines
- Mocks file system operations

### Integration Tests

#### `test_cli.py`
- Tests for Click CLI commands: setup, status, reset
- Tests interactive and non-interactive modes
- Tests error handling and user input validation
- Uses Click's CliRunner for isolated testing

#### `test_integration.py`
- End-to-end workflow testing
- Tests complete setup → status → reset workflows
- Tests error recovery scenarios
- Tests file system edge cases: symlinks, special characters

## Test Configuration

### `pytest.ini`
```ini
[tool:pytest]
testpaths = tests
addopts = 
    --verbose
    --cov=src/claude_setup
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-fail-under=95
```

### Fixtures (`conftest.py`)
- `temp_dir`: Temporary directory for file system tests
- `mock_settings`: Sample configuration settings
- `mock_claude_models`: Sample Claude model data
- `mock_aws_response`: Mock AWS API responses
- `mock_subprocess_run`: Configurable subprocess mock

## Running Tests

### Using pipenv (Recommended)
```bash
# Run all tests with coverage
pipenv run pytest tests/ -v --cov=src/claude_setup --cov-report=term-missing

# Run specific test file
pipenv run pytest tests/test_cli.py -v

# Run with HTML coverage report
pipenv run pytest tests/ --cov=src/claude_setup --cov-report=html
```

### Using the test runner script
```bash
# Make executable and run
chmod +x run_tests.py
python run_tests.py
```

### Test Markers
```bash
# Run only unit tests
pipenv run pytest tests/ -m unit

# Run only integration tests  
pipenv run pytest tests/ -m integration

# Skip slow tests
pipenv run pytest tests/ -m "not slow"
```

## Mocking Strategy

The test suite uses extensive mocking to avoid external dependencies:

- **Subprocess calls**: All AWS CLI calls are mocked to prevent actual API requests
- **File system operations**: File reads/writes are mocked using `unittest.mock.mock_open`
- **Path operations**: Directory and file existence checks are mocked
- **Click CLI**: Uses Click's built-in `CliRunner` for isolated command testing

## Test Data

### Mock AWS Response
```python
{
    'inferenceProfileSummaries': [
        {
            'inferenceProfileId': 'anthropic.claude-3-sonnet-20240229-v1:0',
            'inferenceProfileName': 'Claude 3 Sonnet',
            'inferenceProfileArn': 'arn:aws:bedrock:us-west-2:...',
            'status': 'ACTIVE'
        }
    ]
}
```

### Mock Configuration
```python
{
    "CLAUDE_CODE_USE_BEDROCK": "1",
    "AWS_REGION": "us-west-2", 
    "ANTHROPIC_MODEL": "arn:aws:bedrock:us-west-2:...",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "4096",
    "MAX_THINKING_TOKENS": "1024"
}
```

## Error Scenarios Tested

### AWS Authentication
- Credentials not configured
- AWS CLI not installed
- Permission denied
- Network timeouts
- Unexpected errors

### AWS Bedrock API
- Access denied errors
- Authentication failures
- No models available
- API rate limiting
- JSON parsing errors

### File System
- Permission denied
- Disk full
- Corrupted files
- Missing directories
- Symlink handling

### User Input
- Invalid model selection
- Keyboard interrupts
- Empty inputs
- Special characters

## Coverage Reports

HTML coverage reports are generated in `htmlcov/index.html` and show:
- Line-by-line coverage for each module
- Missing lines highlighted in red
- Branch coverage information
- Summary statistics

## Continuous Integration

The test suite is designed to run in CI environments:
- No external dependencies (all mocked)
- Deterministic results
- Fast execution (< 1 second)
- Clear pass/fail criteria

## Best Practices

1. **Isolation**: Each test is completely isolated using mocks and temporary directories
2. **Deterministic**: Tests produce consistent results regardless of environment
3. **Fast**: Entire suite runs in under 1 second
4. **Comprehensive**: Tests cover happy paths, error conditions, and edge cases
5. **Maintainable**: Clear test names and good documentation
6. **Mock External Dependencies**: No real AWS API calls or file system modifications