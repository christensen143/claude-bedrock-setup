"""Integration tests for the claude-bedrock-setup application."""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from click.testing import CliRunner

from claude_setup.cli import cli
from claude_setup.config_manager import ConfigManager
from claude_setup.gitignore_manager import ensure_gitignore


class TestEndToEndWorkflow:
    """End-to-end integration tests."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner(env={"NO_COLOR": "1"})

    @patch("claude_setup.cli.ensure_gitignore")
    @patch("claude_setup.cli.check_aws_auth")
    @patch("claude_setup.aws_client.subprocess.run")
    def test_complete_setup_workflow(
        self, mock_subprocess, mock_auth, mock_gitignore, mock_aws_response
    ):
        """Test complete setup workflow from start to finish."""
        # Arrange
        mock_auth.return_value = True
        mock_subprocess.return_value = MagicMock(
            returncode=0, stdout=json.dumps(mock_aws_response)
        )

        with self.runner.isolated_filesystem():
            # Act - Run setup
            result = self.runner.invoke(cli, ["setup", "--non-interactive"])

            # Assert setup succeeded
            assert result.exit_code == 0
            assert "Configuration saved successfully!" in result.output

            # Verify configuration file was created
            config_manager = ConfigManager()
            settings = config_manager.load_settings()
            assert settings is not None
            assert settings["CLAUDE_CODE_USE_BEDROCK"] == "1"
            assert settings["AWS_REGION"] == "us-west-2"
            assert "ANTHROPIC_MODEL" in settings

            # Test status command
            status_result = self.runner.invoke(cli, ["status"])
            assert status_result.exit_code == 0
            assert "Claude Bedrock Configuration" in status_result.output
            assert "CLAUDE_CODE_USE_BEDROCK: 1" in status_result.output

            # Test reset command
            reset_result = self.runner.invoke(cli, ["reset"], input="y\n")
            assert reset_result.exit_code == 0
            assert "Configuration reset successfully" in reset_result.output

            # Verify configuration was reset
            settings_after_reset = config_manager.load_settings()
            assert settings_after_reset is None

            # Test status after reset
            status_after_reset = self.runner.invoke(cli, ["status"])
            assert status_after_reset.exit_code == 0
            assert "No configuration found" in status_after_reset.output

    @patch("claude_setup.cli.check_aws_auth")
    @patch("claude_setup.aws_client.subprocess.run")
    def test_setup_with_different_regions(
        self, mock_subprocess, mock_auth, mock_aws_response
    ):
        """Test setup workflow with different AWS regions."""
        # Arrange
        mock_auth.return_value = True
        mock_subprocess.return_value = MagicMock(
            returncode=0, stdout=json.dumps(mock_aws_response)
        )

        regions = ["us-east-1", "eu-west-1", "ap-southeast-1"]

        for region in regions:
            with self.runner.isolated_filesystem():
                # Act
                result = self.runner.invoke(
                    cli, ["setup", "--region", region, "--non-interactive"]
                )

                # Assert
                assert result.exit_code == 0
                assert (
                    f"Fetching available Claude models from {region}" in result.output
                )

                # Verify region in configuration
                config_manager = ConfigManager()
                settings = config_manager.load_settings()
                assert settings["AWS_REGION"] == region

                # Verify AWS CLI was called with correct region
                mock_subprocess.assert_called_with(
                    [
                        "aws",
                        "bedrock",
                        "list-inference-profiles",
                        "--region",
                        region,
                    ],
                    capture_output=True,
                    text=True,
                    check=True,
                )

    def test_gitignore_integration(self):
        """Test gitignore functionality integration."""
        original_dir = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            try:
                os.chdir(temp_path)

                # Test with no existing .gitignore
                ensure_gitignore()
                gitignore_path = temp_path / ".gitignore"
                assert gitignore_path.exists()
                with open(gitignore_path) as f:
                    content = f.read()
                assert ".claude/settings.local.json" in content

                # Test with existing .gitignore
                existing_content = "node_modules/\n*.log\n"
                with open(gitignore_path, "w") as f:
                    f.write(existing_content)

                ensure_gitignore()
                with open(gitignore_path) as f:
                    updated_content = f.read()
                assert existing_content.strip() in updated_content
                assert ".claude/settings.local.json" in updated_content

                # Test idempotent behavior
                ensure_gitignore()
                with open(gitignore_path) as f:
                    final_content = f.read()
                # Should only have one instance of the pattern
                assert final_content.count(".claude/settings.local.json") == 1

            finally:
                os.chdir(original_dir)

    def test_config_manager_integration(self):
        """Test config manager functionality integration."""
        original_dir = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            try:
                os.chdir(temp_path)

                config_manager = ConfigManager()

                # Test saving new settings
                initial_settings = {
                    "CLAUDE_CODE_USE_BEDROCK": "1",
                    "AWS_REGION": "us-west-2",
                }
                config_manager.save_settings(initial_settings)

                # Verify directory and file creation
                assert config_manager.claude_dir.exists()
                assert config_manager.settings_path.exists()

                # Test loading settings
                loaded_settings = config_manager.load_settings()
                assert loaded_settings == initial_settings

                # Test updating settings
                additional_settings = {
                    "ANTHROPIC_MODEL": "claude-3-sonnet",
                    "MAX_THINKING_TOKENS": "2048",
                }
                config_manager.save_settings(additional_settings)

                # Verify merge behavior
                updated_settings = config_manager.load_settings()
                expected_settings = {**initial_settings, **additional_settings}
                assert updated_settings == expected_settings

                # Test reset
                config_manager.reset_settings()
                assert not config_manager.settings_path.exists()
                assert config_manager.load_settings() is None

            finally:
                os.chdir(original_dir)


class TestErrorHandlingIntegration:
    """Integration tests for error handling scenarios."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner(env={"NO_COLOR": "1"})

    @patch("claude_setup.cli.check_aws_auth")
    def test_auth_failure_workflow(self, mock_auth):
        """Test workflow when AWS authentication fails."""
        # Arrange
        mock_auth.return_value = False

        original_dir = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            try:
                os.chdir(temp_path)

                # Act
                result = self.runner.invoke(cli, ["setup"])

                # Assert
                assert result.exit_code == 1
                assert "Not authenticated with AWS" in result.output
                assert "aws configure" in result.output

                # Verify no configuration was created
                config_manager = ConfigManager()
                assert config_manager.load_settings() is None

            finally:
                os.chdir(original_dir)

    @patch("claude_setup.cli.check_aws_auth")
    @patch("claude_setup.aws_client.subprocess.run")
    def test_bedrock_api_error_workflow(self, mock_subprocess, mock_auth):
        """Test workflow when Bedrock API returns error."""
        # Arrange
        mock_auth.return_value = True
        mock_subprocess.side_effect = Exception("AccessDeniedException: Not authorized")

        original_dir = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            try:
                os.chdir(temp_path)

                # Act & Assert
                with pytest.raises(Exception, match="AccessDeniedException"):
                    self.runner.invoke(
                        cli, ["setup", "--non-interactive"], catch_exceptions=False
                    )

                # Verify no configuration was created
                config_manager = ConfigManager()
                assert config_manager.load_settings() is None

            finally:
                os.chdir(original_dir)

    def test_permission_error_workflow(self):
        """Test workflow when permission errors occur."""
        original_dir = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            try:
                os.chdir(temp_path)

                # Create a read-only directory to simulate permission error
                claude_dir = temp_path / ".claude"
                claude_dir.mkdir()
                os.chmod(claude_dir, 0o444)  # Read-only

                try:
                    config_manager = ConfigManager()
                    settings = {"test": "value"}

                    # This should raise a permission error
                    with pytest.raises((PermissionError, OSError)):
                        config_manager.save_settings(settings)

                finally:
                    # Restore permissions for cleanup
                    os.chmod(claude_dir, 0o755)

            finally:
                os.chdir(original_dir)

    def test_corrupted_config_recovery(self):
        """Test recovery from corrupted configuration file."""
        original_dir = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            try:
                os.chdir(temp_path)

                config_manager = ConfigManager()
                config_manager.ensure_claude_directory()

                # Create corrupted JSON file
                with open(config_manager.settings_path, "w") as f:
                    f.write("invalid json content {")

                # Should handle corrupted file gracefully
                result = config_manager.load_settings()
                assert result is None

                # Should be able to save new settings over corrupted file
                new_settings = {"CLAUDE_CODE_USE_BEDROCK": "1"}
                config_manager.save_settings(new_settings)

                # Verify recovery
                loaded_settings = config_manager.load_settings()
                assert loaded_settings == new_settings

            finally:
                os.chdir(original_dir)


class TestConcurrencyAndFileSystemEdgeCases:
    """Test edge cases related to file system operations."""

    def test_concurrent_gitignore_updates(self):
        """Test handling concurrent .gitignore updates."""
        original_dir = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            try:
                os.chdir(temp_path)

                # Create initial .gitignore
                gitignore_path = temp_path / ".gitignore"
                with open(gitignore_path, "w") as f:
                    f.write("initial_content\n")

                # Simulate concurrent modification by changing file
                # between read and write
                # original_ensure = ensure_gitignore  # noqa: F841

                def mock_ensure_with_race_condition():
                    # Read the file
                    with open(gitignore_path, "r") as f:
                        content = f.read()
                        lines = content.strip().split("\n") if content.strip() else []

                    # Simulate another process modifying the file
                    with open(gitignore_path, "w") as f:
                        f.write("initial_content\nconcurrent_addition\n")

                    # Continue with original logic
                    claude_settings_pattern = ".claude/settings.local.json"
                    if claude_settings_pattern not in lines:
                        lines.append(claude_settings_pattern)
                        with open(gitignore_path, "w") as f:
                            f.write("\n".join(lines) + "\n")

                # Run the modified function
                mock_ensure_with_race_condition()

                # Verify the result handles the race condition appropriately
                with open(gitignore_path) as f:
                    final_content = f.read()

                # The exact result may vary, but it should contain our pattern
                assert ".claude/settings.local.json" in final_content

            finally:
                os.chdir(original_dir)

    def test_symlink_handling(self):
        """Test handling of symlinks in configuration paths."""
        original_dir = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            try:
                os.chdir(temp_path)

                # Create actual claude directory
                real_claude_dir = temp_path / "real_claude"
                real_claude_dir.mkdir()

                # Create symlink
                symlink_path = temp_path / ".claude"
                symlink_path.symlink_to(real_claude_dir)

                # Test that config manager works with symlinked directory
                config_manager = ConfigManager()
                settings = {"test": "value"}
                config_manager.save_settings(settings)

                # Verify file was created in real directory
                real_settings_path = real_claude_dir / "settings.local.json"
                assert real_settings_path.exists()

                # Verify loading works through symlink
                loaded_settings = config_manager.load_settings()
                assert loaded_settings == settings

            finally:
                os.chdir(original_dir)

    def test_special_characters_in_paths(self):
        """Test handling paths with special characters."""
        # This test would need to be adapted based on the operating system
        # For now, we'll test basic functionality
        original_dir = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            # Create directory with spaces
            special_dir = temp_path / "dir with spaces"
            special_dir.mkdir()
            try:
                os.chdir(special_dir)

                config_manager = ConfigManager()
                settings = {"test": "value with spaces and unicode: 你好"}
                config_manager.save_settings(settings)

                loaded_settings = config_manager.load_settings()
                assert loaded_settings == settings

            finally:
                os.chdir(original_dir)
