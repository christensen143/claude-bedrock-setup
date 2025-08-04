"""
claude-setup: CLI tool to configure Claude Desktop for AWS Bedrock.

This package provides a command-line interface for setting up Claude Desktop
to use AWS Bedrock as its AI provider, simplifying the configuration process
and making it easy to get started with Claude on AWS.
"""

__version__ = "0.1.0"
__author__ = "Chris Christensen"
__author_email__ = "chris@nexusweblabs.com"
__license__ = "MIT"
__description__ = "CLI tool to configure Claude Desktop for AWS Bedrock"
__url__ = "https://github.com/christensen143/claude-bedrock-setup"


# Lazy imports to avoid import issues during setup
def __getattr__(name):
    if name == "cli":
        from .cli import cli

        return cli
    elif name == "ConfigManager":
        from .config_manager import ConfigManager

        return ConfigManager
    elif name == "AuthChecker":
        from .auth_checker import AuthChecker

        return AuthChecker
    elif name == "AWSClient":
        from .aws_client import AWSClient

        return AWSClient
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    "__version__",
    "__author__",
    "__author_email__",
    "__license__",
    "__description__",
    "__url__",
    "cli",
    "ConfigManager",
    "AuthChecker",
    "AWSClient",
]
