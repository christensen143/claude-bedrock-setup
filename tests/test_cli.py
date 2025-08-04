"""Tests for the CLI module."""

import json
from unittest.mock import patch, MagicMock

import pytest
from click.testing import CliRunner

from claude_setup.cli import cli, setup, status, reset
from claude_setup.config_manager import ConfigManager


class TestCLI:
    """Test cases for CLI commands."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_cli_version(self):
        """Test CLI version option."""
        result = self.runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert "claude-bedrock-setup, version 0.1.0" in result.output

    def test_cli_help(self):
        """Test CLI help."""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert "Claude Bedrock Setup CLI" in result.output
        assert "setup" in result.output
        assert "status" in result.output
        assert "reset" in result.output


class TestSetupCommand:
    """Test cases for setup command."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    @patch('claude_setup.cli.ensure_gitignore')
    @patch('claude_setup.cli.ConfigManager')
    @patch('claude_setup.cli.BedrockClient')
    @patch('claude_setup.cli.check_aws_auth')
    def test_setup_success_non_interactive(self, mock_auth, mock_client_class, mock_config_class, mock_gitignore, mock_claude_models):
        """Test successful setup in non-interactive mode."""
        # Arrange
        mock_auth.return_value = True
        mock_client = MagicMock()
        mock_client.list_claude_models.return_value = mock_claude_models
        mock_client_class.return_value = mock_client
        mock_config = MagicMock()
        mock_config_class.return_value = mock_config
        
        # Act
        result = self.runner.invoke(setup, ['--non-interactive'])
        
        # Assert
        assert result.exit_code == 0
        assert "AWS authentication verified" in result.output
        assert "Configuration saved successfully!" in result.output
        mock_auth.assert_called_once()
        mock_client_class.assert_called_once_with('us-west-2')
        mock_client.list_claude_models.assert_called_once()
        mock_config.save_settings.assert_called_once()
        mock_gitignore.assert_called_once()

    @patch('claude_setup.cli.ensure_gitignore')
    @patch('claude_setup.cli.ConfigManager')
    @patch('claude_setup.cli.BedrockClient')
    @patch('claude_setup.cli.check_aws_auth')
    def test_setup_success_interactive(self, mock_auth, mock_client_class, mock_config_class, mock_gitignore, mock_claude_models):
        """Test successful setup in interactive mode."""
        # Arrange
        mock_auth.return_value = True
        mock_client = MagicMock()
        mock_client.list_claude_models.return_value = mock_claude_models
        mock_client_class.return_value = mock_client
        mock_config = MagicMock()
        mock_config_class.return_value = mock_config
        
        # Act - simulate user selecting model 2
        result = self.runner.invoke(setup, input='2\n')
        
        # Assert
        assert result.exit_code == 0
        assert "Available Claude models:" in result.output
        assert "1. Claude 3 Sonnet" in result.output
        assert "2. Claude 3 Haiku" in result.output
        assert "Configuration saved successfully!" in result.output
        mock_auth.assert_called_once()
        mock_client.list_claude_models.assert_called_once()
        mock_config.save_settings.assert_called_once()
        mock_gitignore.assert_called_once()

    @patch('claude_setup.cli.check_aws_auth')
    def test_setup_auth_failure(self, mock_auth):
        """Test setup when AWS authentication fails."""
        # Arrange
        mock_auth.return_value = False
        
        # Act
        result = self.runner.invoke(setup)
        
        # Assert
        assert result.exit_code == 1
        assert "Not authenticated with AWS" in result.output
        assert "aws configure" in result.output
        mock_auth.assert_called_once()

    @patch('claude_setup.cli.BedrockClient')
    @patch('claude_setup.cli.check_aws_auth')
    def test_setup_no_models_found(self, mock_auth, mock_client_class):
        """Test setup when no Claude models are found."""
        # Arrange
        mock_auth.return_value = True
        mock_client = MagicMock()
        mock_client.list_claude_models.return_value = []
        mock_client_class.return_value = mock_client
        
        # Act
        result = self.runner.invoke(setup)
        
        # Assert
        assert result.exit_code == 1
        assert "No Claude models found" in result.output
        mock_auth.assert_called_once()
        mock_client.list_claude_models.assert_called_once()

    @patch('claude_setup.cli.ensure_gitignore')
    @patch('claude_setup.cli.ConfigManager')
    @patch('claude_setup.cli.BedrockClient')
    @patch('claude_setup.cli.check_aws_auth')
    def test_setup_custom_region(self, mock_auth, mock_client_class, mock_config_class, mock_gitignore, mock_claude_models):
        """Test setup with custom region."""
        # Arrange
        mock_auth.return_value = True
        mock_client = MagicMock()
        mock_client.list_claude_models.return_value = mock_claude_models
        mock_client_class.return_value = mock_client
        mock_config = MagicMock()
        mock_config_class.return_value = mock_config
        
        # Act
        result = self.runner.invoke(setup, ['--region', 'eu-west-1', '--non-interactive'])
        
        # Assert
        assert result.exit_code == 0
        mock_client_class.assert_called_once_with('eu-west-1')
        
        # Check that settings include custom region
        call_args = mock_config.save_settings.call_args[0][0]
        assert call_args['AWS_REGION'] == 'eu-west-1'

    @patch('claude_setup.cli.BedrockClient')
    @patch('claude_setup.cli.check_aws_auth')
    def test_setup_interactive_invalid_choice(self, mock_auth, mock_client_class, mock_claude_models):
        """Test interactive setup with invalid choice."""
        # Arrange
        mock_auth.return_value = True
        mock_client = MagicMock()
        mock_client.list_claude_models.return_value = mock_claude_models
        mock_client_class.return_value = mock_client
        
        # Act - simulate invalid choice then valid choice
        result = self.runner.invoke(setup, input='5\n2\n')
        
        # Assert
        assert result.exit_code == 0
        assert "Invalid choice. Please try again." in result.output

    @patch('claude_setup.cli.BedrockClient')
    @patch('claude_setup.cli.check_aws_auth')
    def test_setup_interactive_keyboard_interrupt(self, mock_auth, mock_client_class, mock_claude_models):
        """Test interactive setup with keyboard interrupt."""
        # Arrange
        mock_auth.return_value = True
        mock_client = MagicMock()
        mock_client.list_claude_models.return_value = mock_claude_models
        mock_client_class.return_value = mock_client
        
        # Act - simulate invalid input that causes ValueError, then abort
        # This simulates a user cancelling by giving invalid input then aborting
        result = self.runner.invoke(setup, input='invalid\ninvalid\n')
        
        # Assert - the setup should handle invalid input and show abort message
        assert "Error: 'invalid' is not a valid integer." in result.output and "Aborted!" in result.output

    @patch('claude_setup.cli.BedrockClient')
    @patch('claude_setup.cli.check_aws_auth')
    def test_setup_bedrock_client_exception(self, mock_auth, mock_client_class):
        """Test setup when BedrockClient raises exception."""
        # Arrange
        mock_auth.return_value = True
        mock_client = MagicMock()
        mock_client.list_claude_models.side_effect = Exception("AWS API Error")
        mock_client_class.return_value = mock_client
        
        # Act & Assert
        with pytest.raises(Exception, match="AWS API Error"):
            self.runner.invoke(setup, catch_exceptions=False)

    @patch('claude_setup.cli.ensure_gitignore')
    @patch('claude_setup.cli.ConfigManager')
    @patch('claude_setup.cli.BedrockClient')
    @patch('claude_setup.cli.check_aws_auth')
    def test_setup_config_manager_exception(self, mock_auth, mock_client_class, mock_config_class, mock_gitignore, mock_claude_models):
        """Test setup when ConfigManager raises exception."""
        # Arrange
        mock_auth.return_value = True
        mock_client = MagicMock()
        mock_client.list_claude_models.return_value = mock_claude_models
        mock_client_class.return_value = mock_client
        mock_config = MagicMock()
        mock_config.save_settings.side_effect = Exception("Config save error")
        mock_config_class.return_value = mock_config
        
        # Act & Assert
        with pytest.raises(Exception, match="Config save error"):
            self.runner.invoke(setup, ['--non-interactive'], catch_exceptions=False)

    @patch('claude_setup.cli.ensure_gitignore', side_effect=Exception("Gitignore error"))
    @patch('claude_setup.cli.ConfigManager')
    @patch('claude_setup.cli.BedrockClient')
    @patch('claude_setup.cli.check_aws_auth')
    def test_setup_gitignore_exception(self, mock_auth, mock_client_class, mock_config_class, mock_gitignore, mock_claude_models):
        """Test setup when ensure_gitignore raises exception."""
        # Arrange
        mock_auth.return_value = True
        mock_client = MagicMock()
        mock_client.list_claude_models.return_value = mock_claude_models
        mock_client_class.return_value = mock_client
        mock_config = MagicMock()
        mock_config_class.return_value = mock_config
        
        # Act & Assert
        with pytest.raises(Exception, match="Gitignore error"):
            self.runner.invoke(setup, ['--non-interactive'], catch_exceptions=False)


class TestStatusCommand:
    """Test cases for status command."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    @patch('claude_setup.cli.ConfigManager')
    def test_status_no_configuration(self, mock_config_class):
        """Test status when no configuration exists."""
        # Arrange
        mock_config = MagicMock()
        mock_config.load_settings.return_value = None
        mock_config_class.return_value = mock_config
        
        # Act
        result = self.runner.invoke(status)
        
        # Assert
        assert result.exit_code == 0
        assert "No configuration found." in result.output
        assert "Run 'claude-bedrock-setup setup'" in result.output
        mock_config.load_settings.assert_called_once()

    @patch('claude_setup.cli.ConfigManager')
    def test_status_with_configuration(self, mock_config_class, mock_settings):
        """Test status with existing configuration."""
        # Arrange
        mock_config = MagicMock()
        mock_config.load_settings.return_value = mock_settings
        mock_config.settings_path = "/test/.claude/settings.local.json"
        mock_config_class.return_value = mock_config
        
        # Act
        result = self.runner.invoke(status)
        
        # Assert
        assert result.exit_code == 0
        assert "Claude Bedrock Configuration" in result.output
        assert "Current settings:" in result.output
        assert "CLAUDE_CODE_USE_BEDROCK: 1" in result.output
        assert "AWS_REGION: us-west-2" in result.output
        assert "anthropic.claude-3-sonnet-20240229-v1:0" in result.output  # Extracted from ARN
        assert "Settings file: /test/.claude/settings.local.json" in result.output
        mock_config.load_settings.assert_called_once()

    @patch('claude_setup.cli.ConfigManager')
    def test_status_arn_extraction(self, mock_config_class):
        """Test status with ARN extraction for ANTHROPIC_MODEL."""
        # Arrange
        settings_with_arn = {
            "ANTHROPIC_MODEL": "arn:aws:bedrock:us-west-2:123456789012:inference-profile/anthropic.claude-3-haiku-20240307-v1:0"
        }
        mock_config = MagicMock()
        mock_config.load_settings.return_value = settings_with_arn
        mock_config_class.return_value = mock_config
        
        # Act
        result = self.runner.invoke(status)
        
        # Assert
        assert result.exit_code == 0
        assert "ANTHROPIC_MODEL: anthropic.claude-3-haiku-20240307-v1:0" in result.output

    @patch('claude_setup.cli.ConfigManager')
    def test_status_simple_model_id(self, mock_config_class):
        """Test status with simple model ID (no ARN)."""
        # Arrange
        settings_simple = {
            "ANTHROPIC_MODEL": "claude-3-sonnet"
        }
        mock_config = MagicMock()
        mock_config.load_settings.return_value = settings_simple
        mock_config_class.return_value = mock_config
        
        # Act
        result = self.runner.invoke(status)
        
        # Assert
        assert result.exit_code == 0
        assert "ANTHROPIC_MODEL: claude-3-sonnet" in result.output

    @patch('claude_setup.cli.ConfigManager')
    def test_status_config_manager_exception(self, mock_config_class):
        """Test status when ConfigManager raises exception."""
        # Arrange
        mock_config = MagicMock()
        mock_config.load_settings.side_effect = Exception("Config load error")
        mock_config_class.return_value = mock_config
        
        # Act & Assert
        with pytest.raises(Exception, match="Config load error"):
            self.runner.invoke(status, catch_exceptions=False)


class TestResetCommand:
    """Test cases for reset command."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    @patch('claude_setup.cli.ConfigManager')
    def test_reset_confirmed(self, mock_config_class):
        """Test reset when user confirms."""
        # Arrange
        mock_config = MagicMock()
        mock_config_class.return_value = mock_config
        
        # Act - simulate user confirming with 'y'
        result = self.runner.invoke(reset, input='y\n')
        
        # Assert
        assert result.exit_code == 0
        assert "Configuration reset successfully." in result.output
        mock_config.reset_settings.assert_called_once()

    @patch('claude_setup.cli.ConfigManager')
    def test_reset_cancelled(self, mock_config_class):
        """Test reset when user cancels."""
        # Arrange
        mock_config = MagicMock()
        mock_config_class.return_value = mock_config
        
        # Act - simulate user canceling with 'n'
        result = self.runner.invoke(reset, input='n\n')
        
        # Assert
        assert result.exit_code == 1  # Click confirmation returns 1 when cancelled
        mock_config.reset_settings.assert_not_called()

    @patch('claude_setup.cli.ConfigManager')
    def test_reset_config_manager_exception(self, mock_config_class):
        """Test reset when ConfigManager raises exception."""
        # Arrange
        mock_config = MagicMock()
        mock_config.reset_settings.side_effect = Exception("Reset error")
        mock_config_class.return_value = mock_config
        
        # Act & Assert
        with pytest.raises(Exception, match="Reset error"):
            self.runner.invoke(reset, input='y\n', catch_exceptions=False)

    def test_reset_help(self):
        """Test reset command help."""
        result = self.runner.invoke(reset, ['--help'])
        assert result.exit_code == 0
        assert "Reset Claude Bedrock configuration" in result.output

    @patch('claude_setup.cli.ConfigManager')
    def test_reset_keyboard_interrupt(self, mock_config_class):
        """Test reset with keyboard interrupt during confirmation."""
        # Arrange
        mock_config = MagicMock()
        mock_config_class.return_value = mock_config
        
        # Act - simulate user aborting by not providing input
        result = self.runner.invoke(reset, input='')
        
        # Assert - should abort when no input is provided
        assert result.exit_code == 1  # Aborted
        mock_config.reset_settings.assert_not_called()


class TestCLIIntegration:
    """Integration tests for the CLI."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_cli_help_shows_all_commands(self):
        """Test that CLI help shows all available commands."""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert "setup" in result.output
        assert "status" in result.output
        assert "reset" in result.output

    def test_individual_command_help(self):
        """Test help for individual commands."""
        # Test setup help
        result = self.runner.invoke(setup, ['--help'])
        assert result.exit_code == 0
        assert "Set up Claude to use AWS Bedrock" in result.output
        assert "--region" in result.output
        assert "--non-interactive" in result.output

        # Test status help
        result = self.runner.invoke(status, ['--help'])
        assert result.exit_code == 0
        assert "Show current Claude Bedrock configuration" in result.output

        # Test reset help
        result = self.runner.invoke(reset, ['--help'])
        assert result.exit_code == 0
        assert "Reset Claude Bedrock configuration" in result.output

    def test_invalid_command(self):
        """Test CLI with invalid command."""
        result = self.runner.invoke(cli, ['invalid-command'])
        assert result.exit_code != 0
        assert "No such command" in result.output