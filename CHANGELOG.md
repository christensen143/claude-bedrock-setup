# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Modern PyPI distribution setup with pyproject.toml
- Enhanced setup.py with complete metadata
- MIT License
- MANIFEST.in for proper package distribution
- Development toolchain configuration (black, mypy, pytest)

### Changed
- Updated package metadata and versioning system

### Fixed
- Package structure for proper PyPI distribution

## [0.1.0] - 2024-08-04

### Added
- Initial release of claude-setup CLI tool
- Interactive setup wizard for Claude Desktop configuration
- AWS Bedrock authentication and model discovery
- Support for multiple AWS authentication methods (CLI profiles, SSO, environment variables, IAM roles)
- Automatic .gitignore management for configuration files
- Rich terminal output with progress indicators
- Configuration validation and status checking
- Reset functionality for easy reconfiguration

### Features
- `claude-setup setup` - Interactive configuration wizard
- `claude-setup configure` - Manual configuration with specific parameters
- `claude-setup status` - Check current configuration and AWS authentication
- `claude-setup reset` - Reset configuration to start fresh

### Supported
- Python 3.7+
- AWS Bedrock regions: us-east-1, us-west-2, eu-west-1, ap-southeast-1
- Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku models
- Multiple AWS authentication methods
- Cross-platform support (Windows, macOS, Linux)

### Dependencies
- click>=8.1.0 - CLI framework
- boto3>=1.34.0 - AWS SDK
- rich>=13.7.0 - Terminal formatting
- python-dotenv>=1.0.0 - Environment variable management