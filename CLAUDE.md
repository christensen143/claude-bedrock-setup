# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Setup is a CLI tool that configures Claude to use AWS Bedrock as its backend provider. It automates the discovery of available Claude models in AWS Bedrock and manages authentication.

## Key Commands

### Development Setup
```bash
# Install dependencies using pipenv
pipenv install

# Install the package in editable mode
pipenv install -e .

# Activate the virtual environment
pipenv shell
```

### Running the CLI
```bash
# Run the CLI directly (after pipenv shell)
claude-setup setup

# Run without activating the environment
pipenv run claude-setup setup

# Available commands
claude-setup setup      # Interactive setup wizard
claude-setup status     # Show current configuration
claude-setup reset      # Reset configuration
```

### Development and Testing
```bash
# Install development dependencies
make install-dev

# Run all checks (lint, type-check, test)
make check

# Individual checks
make lint           # Run flake8
make format         # Format with black
make type-check     # Run mypy
make test           # Run pytest
make test-coverage  # Run tests with coverage

# Pre-commit checks
make pre-commit     # Run format, lint, type-check, and test
```

## Architecture and Key Design Decisions

### Authentication Handling
The codebase uses subprocess calls to AWS CLI instead of boto3 for authentication to avoid double role assumption issues. This is critical when users have AWS profiles with assumed roles. The authentication flow:
1. `auth_checker.py` uses `aws sts get-caller-identity` via subprocess
2. `aws_client.py` uses `aws bedrock list-inference-profiles` via subprocess
3. This avoids the boto3 credential refresh issue that occurs with assumed roles

### Configuration Storage
- Settings are stored in `.claude/settings.local.json` in the user's current directory
- The file contains AWS region, model ARN, and token limits
- `.gitignore` is automatically updated to exclude the settings file

### Module Structure
- `cli.py`: Click-based CLI entry point with commands (setup, status, reset)
- `aws_client.py`: Handles AWS Bedrock API calls using subprocess
- `auth_checker.py`: Verifies AWS authentication status
- `config_manager.py`: Manages settings.local.json file operations
- `gitignore_manager.py`: Ensures .gitignore includes the settings file

### AWS Integration Specifics
- Default region: us-west-2
- Model filtering: Looks for patterns containing 'anthropic.claude' in inference profile IDs
- Uses inference profiles instead of direct model ARNs for cross-region support

### Error Handling
The tool provides user-friendly error messages for:
- Missing AWS authentication
- Insufficient permissions for Bedrock
- No available Claude models in the specified region

## Important Implementation Notes

1. **AWS Profile Handling**: The code specifically avoids using boto3 Session() when dealing with assumed roles to prevent "AccessDenied" errors during role assumption.

2. **Model Discovery**: The tool filters Bedrock inference profiles for Claude models using the pattern 'anthropic.claude' in the profile ID.

3. **Pipenv Usage**: The project uses Pipenv for dependency management. The Pipfile.lock is intentionally gitignored as this is a library.

4. **Python Version**: Requires Python 3.7+ (though Pipfile specifies 3.13)