"""Pytest configuration and shared fixtures for claude-bedrock-setup tests."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_settings():
    """Sample configuration settings for testing."""
    return {
        "CLAUDE_CODE_USE_BEDROCK": "1",
        "AWS_REGION": "us-west-2",
        "ANTHROPIC_MODEL": "arn:aws:bedrock:us-west-2:123456789012:inference-profile/anthropic.claude-3-sonnet-20240229-v1:0",
        "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "4096",
        "MAX_THINKING_TOKENS": "1024"
    }


@pytest.fixture
def mock_claude_models():
    """Sample Claude models response for testing."""
    return [
        {
            'id': 'anthropic.claude-3-sonnet-20240229-v1:0',
            'name': 'Claude 3 Sonnet',
            'arn': 'arn:aws:bedrock:us-west-2:123456789012:inference-profile/anthropic.claude-3-sonnet-20240229-v1:0',
            'status': 'ACTIVE'
        },
        {
            'id': 'anthropic.claude-3-haiku-20240307-v1:0',
            'name': 'Claude 3 Haiku',
            'arn': 'arn:aws:bedrock:us-west-2:123456789012:inference-profile/anthropic.claude-3-haiku-20240307-v1:0',
            'status': 'ACTIVE'
        },
        {
            'id': 'anthropic.claude-3-opus-20240229-v1:0',
            'name': 'Claude 3 Opus',
            'arn': 'arn:aws:bedrock:us-west-2:123456789012:inference-profile/anthropic.claude-3-opus-20240229-v1:0',
            'status': 'ACTIVE'
        }
    ]


@pytest.fixture
def mock_aws_response():
    """Mock AWS CLI response for list-inference-profiles."""
    return {
        'inferenceProfileSummaries': [
            {
                'inferenceProfileId': 'anthropic.claude-3-sonnet-20240229-v1:0',
                'inferenceProfileName': 'Claude 3 Sonnet',
                'inferenceProfileArn': 'arn:aws:bedrock:us-west-2:123456789012:inference-profile/anthropic.claude-3-sonnet-20240229-v1:0',
                'status': 'ACTIVE'
            },
            {
                'inferenceProfileId': 'anthropic.claude-3-haiku-20240307-v1:0',
                'inferenceProfileName': 'Claude 3 Haiku',
                'inferenceProfileArn': 'arn:aws:bedrock:us-west-2:123456789012:inference-profile/anthropic.claude-3-haiku-20240307-v1:0',
                'status': 'ACTIVE'
            },
            {
                'inferenceProfileId': 'anthropic.claude-3-opus-20240229-v1:0',
                'inferenceProfileName': 'Claude 3 Opus',
                'inferenceProfileArn': 'arn:aws:bedrock:us-west-2:123456789012:inference-profile/anthropic.claude-3-opus-20240229-v1:0',
                'status': 'ACTIVE'
            },
            {
                'inferenceProfileId': 'meta.llama3-8b-instruct-v1:0',
                'inferenceProfileName': 'Llama 3 8B',
                'inferenceProfileArn': 'arn:aws:bedrock:us-west-2:123456789012:inference-profile/meta.llama3-8b-instruct-v1:0',
                'status': 'ACTIVE'
            }
        ]
    }


@pytest.fixture
def mock_subprocess_run():
    """Create a mock subprocess.run with configurable behavior."""
    def _mock_run(returncode=0, stdout="", stderr="", side_effect=None):
        mock = MagicMock()
        mock.returncode = returncode
        mock.stdout = stdout
        mock.stderr = stderr
        if side_effect:
            mock.side_effect = side_effect
        return mock
    return _mock_run