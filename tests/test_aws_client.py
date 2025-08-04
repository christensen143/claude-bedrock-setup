"""Tests for the aws_client module."""

import json
import subprocess
from unittest.mock import patch, MagicMock

import pytest

from claude_setup.aws_client import BedrockClient


class TestBedrockClient:
    """Test cases for BedrockClient class."""

    def test_init_default_region(self):
        """Test BedrockClient initialization with default region."""
        client = BedrockClient()
        assert client.region == 'us-west-2'

    def test_init_custom_region(self):
        """Test BedrockClient initialization with custom region."""
        region = 'us-east-1'
        client = BedrockClient(region)
        assert client.region == region

    @patch('claude_setup.aws_client.subprocess.run')
    def test_list_claude_models_success(self, mock_run, mock_aws_response):
        """Test successful listing of Claude models."""
        # Arrange
        client = BedrockClient('us-west-2')
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps(mock_aws_response)
        )
        
        # Act
        result = client.list_claude_models()
        
        # Assert
        assert len(result) == 3  # Only Claude models, not Llama
        assert all('anthropic.claude' in model['id'] for model in result)
        
        # Check first model details
        assert result[0]['id'] == 'anthropic.claude-3-haiku-20240307-v1:0'
        assert result[0]['name'] == 'Claude 3 Haiku'
        assert result[0]['arn'] == 'arn:aws:bedrock:us-west-2:123456789012:inference-profile/anthropic.claude-3-haiku-20240307-v1:0'
        assert result[0]['status'] == 'ACTIVE'
        
        # Verify models are sorted by name
        model_names = [model['name'] for model in result]
        assert model_names == sorted(model_names)
        
        mock_run.assert_called_once_with(
            ['aws', 'bedrock', 'list-inference-profiles', '--region', 'us-west-2'],
            capture_output=True,
            text=True,
            check=True
        )

    @patch('claude_setup.aws_client.subprocess.run')
    def test_list_claude_models_empty_response(self, mock_run):
        """Test listing Claude models with empty response."""
        # Arrange
        client = BedrockClient()
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps({'inferenceProfileSummaries': []})
        )
        
        # Act
        result = client.list_claude_models()
        
        # Assert
        assert result == []
        mock_run.assert_called_once()

    @patch('claude_setup.aws_client.subprocess.run')
    def test_list_claude_models_no_claude_models(self, mock_run):
        """Test listing when no Claude models are available."""
        # Arrange
        client = BedrockClient()
        non_claude_response = {
            'inferenceProfileSummaries': [
                {
                    'inferenceProfileId': 'meta.llama3-8b-instruct-v1:0',
                    'inferenceProfileName': 'Llama 3 8B',
                    'inferenceProfileArn': 'arn:aws:bedrock:us-west-2:123456789012:inference-profile/meta.llama3-8b-instruct-v1:0',
                    'status': 'ACTIVE'
                }
            ]
        }
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps(non_claude_response)
        )
        
        # Act
        result = client.list_claude_models()
        
        # Assert
        assert result == []
        mock_run.assert_called_once()

    @patch('claude_setup.aws_client.subprocess.run')
    def test_list_claude_models_missing_profile_name(self, mock_run):
        """Test listing Claude models when profile name is missing."""
        # Arrange
        client = BedrockClient()
        response_without_name = {
            'inferenceProfileSummaries': [
                {
                    'inferenceProfileId': 'anthropic.claude-3-sonnet-20240229-v1:0',
                    'inferenceProfileArn': 'arn:aws:bedrock:us-west-2:123456789012:inference-profile/anthropic.claude-3-sonnet-20240229-v1:0',
                    'status': 'ACTIVE'
                }
            ]
        }
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps(response_without_name)
        )
        
        # Act
        result = client.list_claude_models()
        
        # Assert
        assert len(result) == 1
        # Should use the last part of profile ID as name
        assert result[0]['name'] == 'anthropic.claude-3-sonnet-20240229-v1:0'
        mock_run.assert_called_once()

    @patch('claude_setup.aws_client.subprocess.run')
    def test_list_claude_models_access_denied_error(self, mock_run):
        """Test listing Claude models with AccessDeniedException."""
        # Arrange
        client = BedrockClient()
        error = subprocess.CalledProcessError(
            1, 'aws', stderr='AccessDeniedException: User not authorized'
        )
        mock_run.side_effect = error
        
        # Act & Assert
        with pytest.raises(Exception, match="Access denied. Please check your AWS permissions for Amazon Bedrock."):
            client.list_claude_models()
        
        mock_run.assert_called_once()

    @patch('claude_setup.aws_client.subprocess.run')
    def test_list_claude_models_not_authorized_error(self, mock_run):
        """Test listing Claude models with authentication error."""
        # Arrange
        client = BedrockClient()
        error = subprocess.CalledProcessError(
            1, 'aws', stderr='The security token included in the request is invalid. not authorized'
        )
        mock_run.side_effect = error
        
        # Act & Assert
        with pytest.raises(Exception, match="Not authenticated with AWS. Please run 'aws configure' or set up your AWS credentials."):
            client.list_claude_models()
        
        mock_run.assert_called_once()

    @patch('claude_setup.aws_client.subprocess.run')
    def test_list_claude_models_generic_called_process_error(self, mock_run):
        """Test listing Claude models with generic CalledProcessError."""
        # Arrange
        client = BedrockClient()
        error_message = "Some other AWS CLI error"
        error = subprocess.CalledProcessError(1, 'aws', stderr=error_message)
        mock_run.side_effect = error
        
        # Act & Assert
        with pytest.raises(Exception, match=f"Error listing models: {error_message}"):
            client.list_claude_models()
        
        mock_run.assert_called_once()

    @patch('claude_setup.aws_client.subprocess.run')
    def test_list_claude_models_json_decode_error(self, mock_run):
        """Test listing Claude models with invalid JSON response."""
        # Arrange
        client = BedrockClient()
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="invalid json"
        )
        
        # Act & Assert
        with pytest.raises(Exception, match="Unexpected error:"):
            client.list_claude_models()
        
        mock_run.assert_called_once()

    @patch('claude_setup.aws_client.subprocess.run')
    def test_list_claude_models_unexpected_error(self, mock_run):
        """Test listing Claude models with unexpected error."""
        # Arrange
        client = BedrockClient()
        mock_run.side_effect = RuntimeError("Unexpected runtime error")
        
        # Act & Assert
        with pytest.raises(Exception, match="Unexpected error: Unexpected runtime error"):
            client.list_claude_models()
        
        mock_run.assert_called_once()

    @patch('claude_setup.aws_client.subprocess.run')
    def test_list_claude_models_custom_region(self, mock_run, mock_aws_response):
        """Test listing Claude models with custom region."""
        # Arrange
        custom_region = 'eu-west-1'
        client = BedrockClient(custom_region)
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps(mock_aws_response)
        )
        
        # Act
        result = client.list_claude_models()
        
        # Assert
        assert len(result) == 3
        mock_run.assert_called_once_with(
            ['aws', 'bedrock', 'list-inference-profiles', '--region', custom_region],
            capture_output=True,
            text=True,
            check=True
        )

    @patch('claude_setup.aws_client.subprocess.run')
    def test_list_claude_models_partial_data(self, mock_run):
        """Test listing Claude models with partial data in response."""
        # Arrange
        client = BedrockClient()
        partial_response = {
            'inferenceProfileSummaries': [
                {
                    'inferenceProfileId': 'anthropic.claude-3-sonnet-20240229-v1:0',
                    # Missing other fields
                }
            ]
        }
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps(partial_response)
        )
        
        # Act
        result = client.list_claude_models()
        
        # Assert
        assert len(result) == 1
        assert result[0]['id'] == 'anthropic.claude-3-sonnet-20240229-v1:0'
        assert result[0]['name'] == 'anthropic.claude-3-sonnet-20240229-v1:0'
        assert result[0]['arn'] == ''
        assert result[0]['status'] == 'ACTIVE'  # Default value
        mock_run.assert_called_once()

    @patch('claude_setup.aws_client.subprocess.run')
    def test_list_claude_models_file_not_found_error(self, mock_run):
        """Test listing Claude models when AWS CLI is not installed."""
        # Arrange
        client = BedrockClient()
        mock_run.side_effect = FileNotFoundError("aws command not found")
        
        # Act & Assert
        with pytest.raises(Exception, match="Unexpected error: aws command not found"):
            client.list_claude_models()
        
        mock_run.assert_called_once()