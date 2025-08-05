"""Tests for the config_manager module."""

from pathlib import Path
from unittest.mock import patch, mock_open

import pytest

from claude_setup.config_manager import ConfigManager


class TestConfigManager:
    """Test cases for ConfigManager class."""

    def test_init(self):
        """Test ConfigManager initialization."""
        config_manager = ConfigManager()

        assert config_manager.claude_dir == Path(".claude")
        assert config_manager.settings_file == "settings.local.json"
        assert config_manager.settings_path == Path(".claude/settings.local.json")

    @patch("claude_setup.config_manager.Path.mkdir")
    def test_ensure_claude_directory(self, mock_mkdir):
        """Test ensuring .claude directory exists."""
        # Arrange
        config_manager = ConfigManager()

        # Act
        config_manager.ensure_claude_directory()

        # Assert
        mock_mkdir.assert_called_once_with(exist_ok=True)

    @patch("claude_setup.config_manager.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_settings_new_file(self, mock_file, mock_mkdir):
        """Test saving settings to a new file."""
        # Arrange
        config_manager = ConfigManager()
        settings = {"CLAUDE_CODE_USE_BEDROCK": "1", "AWS_REGION": "us-west-2"}

        # Act
        config_manager.save_settings(settings)

        # Assert
        mock_mkdir.assert_called_once_with(exist_ok=True)
        mock_file.assert_called_once_with(config_manager.settings_path, "w")

        # Check that json.dump was called - the actual data is written
        # by json.dump
        # json.dump calls write multiple times, so we just verify
        # write was called
        assert mock_file().write.called

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    @patch("claude_setup.config_manager.Path.exists")
    def test_load_settings_legacy_format(self, mock_exists, mock_file):
        """Test successfully loading settings in legacy format."""
        # Arrange
        config_manager = ConfigManager()
        mock_exists.return_value = True

        # Act
        result = config_manager.load_settings()

        # Assert
        assert result == {"key": "value"}
        mock_exists.assert_called_once()
        mock_file.assert_called_once_with(config_manager.settings_path, "r")

    @patch(
        "builtins.open", new_callable=mock_open, read_data='{"env": {"key": "value"}}'
    )
    @patch("claude_setup.config_manager.Path.exists")
    def test_load_settings_new_format(self, mock_exists, mock_file):
        """Test successfully loading settings in new env wrapper format."""
        # Arrange
        config_manager = ConfigManager()
        mock_exists.return_value = True

        # Act
        result = config_manager.load_settings()

        # Assert
        assert result == {"key": "value"}
        mock_exists.assert_called_once()
        mock_file.assert_called_once_with(config_manager.settings_path, "r")

    @patch("claude_setup.config_manager.Path.exists")
    def test_load_settings_file_not_exists(self, mock_exists):
        """Test loading settings when file doesn't exist."""
        # Arrange
        config_manager = ConfigManager()
        mock_exists.return_value = False

        # Act
        result = config_manager.load_settings()

        # Assert
        assert result is None
        mock_exists.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    @patch("claude_setup.config_manager.Path.exists")
    def test_load_settings_json_decode_error(self, mock_exists, mock_file):
        """Test loading settings with invalid JSON."""
        # Arrange
        config_manager = ConfigManager()
        mock_exists.return_value = True

        # Act
        result = config_manager.load_settings()

        # Assert
        assert result is None
        mock_exists.assert_called_once()
        mock_file.assert_called_once_with(config_manager.settings_path, "r")

    @patch("builtins.open", side_effect=IOError("Permission denied"))
    @patch("claude_setup.config_manager.Path.exists")
    def test_load_settings_io_error(self, mock_exists, mock_file):
        """Test loading settings with IO error."""
        # Arrange
        config_manager = ConfigManager()
        mock_exists.return_value = True

        # Act
        result = config_manager.load_settings()

        # Assert
        assert result is None
        mock_exists.assert_called_once()
        mock_file.assert_called_once_with(config_manager.settings_path, "r")

    @patch("claude_setup.config_manager.Path.unlink")
    @patch("claude_setup.config_manager.Path.exists")
    def test_reset_settings_file_exists(self, mock_exists, mock_unlink):
        """Test resetting settings when file exists."""
        # Arrange
        config_manager = ConfigManager()
        mock_exists.return_value = True

        # Act
        config_manager.reset_settings()

        # Assert
        mock_exists.assert_called_once()
        mock_unlink.assert_called_once()

    @patch("claude_setup.config_manager.Path.unlink")
    @patch("claude_setup.config_manager.Path.exists")
    def test_reset_settings_file_not_exists(self, mock_exists, mock_unlink):
        """Test resetting settings when file doesn't exist."""
        # Arrange
        config_manager = ConfigManager()
        mock_exists.return_value = False

        # Act
        config_manager.reset_settings()

        # Assert
        mock_exists.assert_called_once()
        mock_unlink.assert_not_called()

    @patch("claude_setup.config_manager.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_settings_empty_dict(self, mock_file, mock_mkdir):
        """Test saving empty settings dictionary."""
        # Arrange
        config_manager = ConfigManager()
        settings = {}

        # Act
        config_manager.save_settings(settings)

        # Assert
        mock_mkdir.assert_called_once_with(exist_ok=True)
        mock_file.assert_called_once_with(config_manager.settings_path, "w")

        # Check that write was called for empty dict
        assert mock_file().write.called

    @patch("claude_setup.config_manager.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_settings_special_characters(self, mock_file, mock_mkdir):
        """Test saving settings with special characters."""
        # Arrange
        config_manager = ConfigManager()
        settings = {
            "SPECIAL_CHARS": "!@#$%^&*()_+-=[]{}|;':\",./<>?",
            "UNICODE": "héllo wørld 你好",
        }

        # Act
        config_manager.save_settings(settings)

        # Assert
        mock_mkdir.assert_called_once_with(exist_ok=True)
        mock_file.assert_called_once_with(config_manager.settings_path, "w")
        assert mock_file().write.called

    @patch("builtins.open", new_callable=mock_open, read_data="{}")
    @patch("claude_setup.config_manager.Path.exists")
    def test_load_settings_empty_file(self, mock_exists, mock_file):
        """Test loading settings from empty JSON file."""
        # Arrange
        config_manager = ConfigManager()
        mock_exists.return_value = True

        # Act
        result = config_manager.load_settings()

        # Assert
        assert result == {}
        mock_exists.assert_called_once()
        mock_file.assert_called_once_with(config_manager.settings_path, "r")

    @patch("builtins.open", new_callable=mock_open, read_data='{"env": {}}')
    @patch("claude_setup.config_manager.Path.exists")
    def test_load_settings_empty_env(self, mock_exists, mock_file):
        """Test loading settings from empty env wrapper."""
        # Arrange
        config_manager = ConfigManager()
        mock_exists.return_value = True

        # Act
        result = config_manager.load_settings()

        # Assert
        assert result == {}
        mock_exists.assert_called_once()
        mock_file.assert_called_once_with(config_manager.settings_path, "r")

    @patch(
        "claude_setup.config_manager.Path.mkdir",
        side_effect=PermissionError("Permission denied"),
    )
    def test_save_settings_mkdir_permission_error(self, mock_mkdir):
        """Test saving settings when mkdir raises PermissionError."""
        # Arrange
        config_manager = ConfigManager()
        settings = {"key": "value"}

        # Act & Assert
        with pytest.raises(PermissionError, match="Permission denied"):
            config_manager.save_settings(settings)

        mock_mkdir.assert_called_once_with(exist_ok=True)

    @patch("claude_setup.config_manager.Path.mkdir")
    @patch("builtins.open", side_effect=PermissionError("Permission denied"))
    def test_save_settings_file_permission_error(self, mock_file, mock_mkdir):
        """Test saving settings when file write raises PermissionError."""
        # Arrange
        config_manager = ConfigManager()
        settings = {"key": "value"}

        # Act & Assert
        with pytest.raises(PermissionError, match="Permission denied"):
            config_manager.save_settings(settings)

        mock_mkdir.assert_called_once_with(exist_ok=True)
        mock_file.assert_called_once_with(config_manager.settings_path, "w")

    @patch(
        "claude_setup.config_manager.Path.unlink",
        side_effect=PermissionError("Permission denied"),
    )
    @patch("claude_setup.config_manager.Path.exists")
    def test_reset_settings_permission_error(self, mock_exists, mock_unlink):
        """Test resetting settings when unlink raises PermissionError."""
        # Arrange
        config_manager = ConfigManager()
        mock_exists.return_value = True

        # Act & Assert
        with pytest.raises(PermissionError, match="Permission denied"):
            config_manager.reset_settings()

        mock_exists.assert_called_once()
        mock_unlink.assert_called_once()
