"""
claude-setup: CLI tool to configure Claude Desktop for AWS Bedrock.

This package provides a command-line interface for setting up Claude Desktop
to use AWS Bedrock as its AI provider, simplifying the configuration process
and making it easy to get started with Claude on AWS.
"""

from __future__ import annotations

from ._version import __version__

__author__ = "Chris Christensen"
__author_email__ = "chris@nexusweblabs.com"
__license__ = "MIT"
__description__ = "CLI tool to configure Claude Desktop for AWS Bedrock"
__url__ = "https://github.com/christensen143/claude-bedrock-setup"

# Module-level imports for __all__ exports
from .cli import cli
from .config_manager import ConfigManager
from .aws_client import BedrockClient


__all__ = [
    "__version__",
    "__author__",
    "__author_email__",
    "__license__",
    "__description__",
    "__url__",
    "cli",
    "ConfigManager",
    "BedrockClient",
]
