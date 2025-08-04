from setuptools import setup, find_packages

setup(
    name="claude-setup",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.1.0",
        "boto3>=1.34.0",
        "rich>=13.7.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "claude-setup=claude_setup.cli:cli",
        ],
    },
    author="Your Name",
    description="CLI tool to configure Claude for AWS Bedrock",
    python_requires=">=3.7",
)