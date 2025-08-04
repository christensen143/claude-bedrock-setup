"""setup.py - Setup script for the Claude Bedrock Setup CLI tool."""

import os
import re
from setuptools import setup, find_packages


def get_version():
    """Extract version from src/claude_setup/_version.py."""
    version_file = os.path.join("src", "claude_setup", "_version.py")
    with open(version_file, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', content, re.MULTILINE)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find __version__ in _version.py")


# Read long description from README.md
def get_long_description():
    """Read the long description from README.md."""
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return (
            "A command-line tool to configure Claude Desktop to use "
            "AWS Bedrock as its AI provider."
        )


setup(
    name="claude-bedrock-setup",
    version=get_version(),
    author="Chris Christensen",
    author_email="chris.christensen@nexusweblabs.com",
    description="CLI tool to configure Claude Desktop for AWS Bedrock",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/christensen143/claude-bedrock-setup",
    project_urls={
        "Bug Tracker": (
            "https://github.com/christensen143/" "claude-bedrock-setup/issues"
        ),
        "Documentation": (
            "https://github.com/christensen143/" "claude-bedrock-setup#readme"
        ),
        "Source Code": ("https://github.com/christensen143/" "claude-bedrock-setup"),
        "Changelog": (
            "https://github.com/christensen143/"
            "claude-bedrock-setup/blob/main/CHANGELOG.md"
        ),
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Installation/Setup",
        "Topic :: Utilities",
        "Environment :: Console",
        "Typing :: Typed",
    ],
    keywords=[
        "claude",
        "anthropic",
        "aws",
        "bedrock",
        "cli",
        "configuration",
        "setup",
        "ai",
        "llm",
        "chatbot",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.1.0",
        "boto3>=1.34.0",
        "rich>=13.7.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
            "pre-commit>=3.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "moto[bedrock]>=4.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "claude-bedrock-setup=claude_setup.cli:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
