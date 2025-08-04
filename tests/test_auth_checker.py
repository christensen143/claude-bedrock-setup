"""Tests for the auth_checker module."""

import subprocess
from unittest.mock import patch, MagicMock

from claude_setup.auth_checker import check_aws_auth


class TestCheckAWSAuth:
    """Test cases for check_aws_auth function."""

    @patch("claude_setup.auth_checker.subprocess.run")
    def test_check_aws_auth_success(self, mock_run):
        """Test successful AWS authentication check."""
        # Arrange
        mock_run.return_value = MagicMock(returncode=0)

        # Act
        result = check_aws_auth()

        # Assert
        assert result is True
        mock_run.assert_called_once_with(
            ["aws", "sts", "get-caller-identity"],
            capture_output=True,
            text=True,
            check=True,
        )

    @patch("claude_setup.auth_checker.subprocess.run")
    def test_check_aws_auth_called_process_error(self, mock_run):
        """Test AWS authentication check with CalledProcessError."""
        # Arrange
        mock_run.side_effect = subprocess.CalledProcessError(1, "aws")

        # Act
        result = check_aws_auth()

        # Assert
        assert result is False
        mock_run.assert_called_once_with(
            ["aws", "sts", "get-caller-identity"],
            capture_output=True,
            text=True,
            check=True,
        )

    @patch("claude_setup.auth_checker.subprocess.run")
    def test_check_aws_auth_file_not_found_error(self, mock_run):
        """Test AWS authentication check when AWS CLI is not installed."""
        # Arrange
        mock_run.side_effect = FileNotFoundError("aws command not found")

        # Act
        result = check_aws_auth()

        # Assert
        assert result is False
        mock_run.assert_called_once_with(
            ["aws", "sts", "get-caller-identity"],
            capture_output=True,
            text=True,
            check=True,
        )

    @patch("claude_setup.auth_checker.subprocess.run")
    def test_check_aws_auth_unexpected_exception(self, mock_run):
        """Test AWS authentication check with unexpected exception."""
        # Arrange
        mock_run.side_effect = RuntimeError("Unexpected error")

        # Act
        result = check_aws_auth()

        # Assert
        assert result is False
        mock_run.assert_called_once_with(
            ["aws", "sts", "get-caller-identity"],
            capture_output=True,
            text=True,
            check=True,
        )

    @patch("claude_setup.auth_checker.subprocess.run")
    def test_check_aws_auth_permission_error(self, mock_run):
        """Test AWS authentication check with permission error."""
        # Arrange
        mock_run.side_effect = PermissionError("Permission denied")

        # Act
        result = check_aws_auth()

        # Assert
        assert result is False
        mock_run.assert_called_once_with(
            ["aws", "sts", "get-caller-identity"],
            capture_output=True,
            text=True,
            check=True,
        )

    @patch("claude_setup.auth_checker.subprocess.run")
    def test_check_aws_auth_timeout_error(self, mock_run):
        """Test AWS authentication check with timeout error."""
        # Arrange
        mock_run.side_effect = subprocess.TimeoutExpired("aws", 30)

        # Act
        result = check_aws_auth()

        # Assert
        assert result is False
        mock_run.assert_called_once_with(
            ["aws", "sts", "get-caller-identity"],
            capture_output=True,
            text=True,
            check=True,
        )
