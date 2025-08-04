# claude-bedrock-setup

[![PyPI version](https://badge.fury.io/py/claude-bedrock-setup.svg)](https://badge.fury.io/py/claude-bedrock-setup)
[![Python Versions](https://img.shields.io/pypi/pyversions/claude-bedrock-setup.svg)](https://pypi.org/project/claude-bedrock-setup/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/christensen143/claude-bedrock-setup/actions/workflows/ci.yml/badge.svg)](https://github.com/christensen143/claude-bedrock-setup/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen.svg)](https://github.com/christensen143/claude-bedrock-setup)

A command-line tool to configure Claude Desktop to use AWS Bedrock as its AI provider. This tool simplifies the process of discovering available Claude models in your AWS account and automatically configures Claude Desktop with the appropriate settings.

## Features

- 🔐 **Automatic AWS authentication detection** - Verifies your AWS credentials before proceeding
- 🔍 **Model discovery** - Automatically lists all available Claude models in your AWS Bedrock account
- ⚙️ **Simple configuration** - Interactive setup wizard guides you through the process
- 🌍 **Multi-region support** - Works with any AWS region that supports Bedrock
- 🔒 **Secure** - Credentials are handled by AWS SDK, settings are stored locally
- 🚀 **Fast setup** - Get up and running in under 30 seconds

## Prerequisites

- Python 3.10 or higher
- AWS CLI configured with valid credentials
- AWS account with access to Amazon Bedrock
- Claude Desktop application installed

## Installation

### Via pip (recommended)

```bash
pip install claude-bedrock-setup
```

### Via pipenv

```bash
pipenv install claude-bedrock-setup
```

### From source

```bash
git clone https://github.com/christensen143/claude-bedrock-setup.git
cd claude-bedrock-setup
pip install -e .
```

## Quick Start

1. **Ensure AWS authentication is configured:**

   ```bash
   aws configure
   # or
   aws sso login --profile your-profile
   ```

2. **Run the setup wizard:**

   ```bash
   claude-bedrock-setup setup
   ```

3. **Follow the interactive prompts** to select your preferred Claude model

That's it! Claude Desktop is now configured to use AWS Bedrock.

## Usage

### Interactive Setup (Recommended)

The easiest way to configure Claude is using the interactive setup wizard:

```bash
claude-bedrock-setup setup
```

This will:

1. Verify your AWS authentication
2. List available Claude models in your account
3. Let you select your preferred model
4. Save the configuration for Claude Desktop

### Manual Configuration

If you prefer to configure specific settings manually:

```bash
claude-bedrock-setup configure --model <model-arn> --region us-west-2
```

### Check Current Configuration

To view your current configuration:

```bash
claude-bedrock-setup status
```

Example output:

```
Claude Bedrock Configuration Status
===================================

✅ AWS Authentication: Valid
   Account: 123456789012
   User: user@example.com

✅ Configuration File: .claude/settings.local.json

Current Settings:
- AWS_REGION: us-west-2
- Model: Claude 3.5 Sonnet v2
- Max Output Tokens: 4096
```

### Reset Configuration

To reset your configuration:

```bash
claude-bedrock-setup reset
```

## Configuration Details

The tool creates a `.claude/settings.local.json` file in your current directory with the following settings:

```json
{
  "CLAUDE_CODE_USE_BEDROCK": "1",
  "AWS_REGION": "us-west-2",
  "ANTHROPIC_MODEL": "arn:aws:bedrock:...",
  "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "4096",
  "MAX_THINKING_TOKENS": "1024"
}
```

The tool also automatically updates your `.gitignore` to exclude the settings file.

## AWS Authentication

claude-bedrock-setup supports all standard AWS authentication methods:

- **AWS CLI profiles**: `aws configure`
- **AWS SSO**: `aws sso login --profile your-profile`
- **Environment variables**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- **IAM roles**: When running on EC2 or with assumed roles

### Required AWS Permissions

Your AWS credentials need the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:ListInferenceProfiles",
        "bedrock:GetInferenceProfile"
      ],
      "Resource": "*"
    }
  ]
}
```

## Troubleshooting

### "No Claude models found"

This usually means your AWS account doesn't have access to Claude models in Bedrock. To fix:

1. Log into AWS Console
2. Navigate to Amazon Bedrock
3. Go to Model Access
4. Request access to Anthropic Claude models
5. Wait for approval (usually immediate)
6. Run `claude-bedrock-setup setup` again

### "Access Denied" errors

If you're using AWS SSO or assumed roles, ensure your profile is active:

```bash
aws sso login --profile your-profile
export AWS_PROFILE=your-profile
claude-bedrock-setup setup
```

### Region-specific issues

Some AWS regions don't support Bedrock. Supported regions include:

- us-east-1 (N. Virginia)
- us-west-2 (Oregon)
- eu-west-1 (Ireland)
- ap-southeast-1 (Singapore)

Use the `--region` flag to specify a different region:

```bash
claude-bedrock-setup setup --region us-east-1
```

## Development

### Setting up for development

```bash
git clone https://github.com/christensen143/claude-bedrock-setup.git
cd claude-bedrock-setup
make install-dev
```

### Running tests

```bash
make test                 # Run tests
make test-coverage        # Run tests with coverage report
make lint                 # Run linting
make format              # Format code
make check               # Run all checks
```

### Building for distribution

```bash
make build               # Build distribution packages
make upload-test         # Upload to TestPyPI
make upload              # Upload to PyPI
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make check`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

Please ensure:

- All tests pass
- Code coverage remains above 95%
- Code follows the project style (run `make format`)
- Commit messages are clear and descriptive

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for the CLI interface
- Uses [Rich](https://rich.readthedocs.io/) for beautiful terminal output
- AWS SDK ([boto3](https://boto3.amazonaws.com/)) for AWS interactions

## Support

- **Issues**: [GitHub Issues](https://github.com/christensen143/claude-bedrock-setup/issues)
- **Discussions**: [GitHub Discussions](https://github.com/christensen143/claude-bedrock-setup/discussions)
- **Security**: For security issues, please email security@nexusweblabs.com

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## Roadmap

- [ ] Support for multiple configuration profiles
- [ ] Configuration templates for different use cases
- [ ] Direct integration with Claude Desktop API
- [ ] Support for other AI providers
- [ ] Configuration validation and testing

---

Made with ❤️ by the Claude Setup team
