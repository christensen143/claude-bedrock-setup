"""Tests for the gitignore_manager module."""

from pathlib import Path
from unittest.mock import patch, mock_open

import pytest

from claude_setup.gitignore_manager import ensure_gitignore


class TestEnsureGitignore:
    """Test cases for ensure_gitignore function."""

    @patch("builtins.open", new_callable=mock_open, read_data="")
    @patch("claude_setup.gitignore_manager.Path.exists")
    def test_ensure_gitignore_empty_file(self, mock_exists, mock_file):
        """Test adding pattern to empty .gitignore file."""
        # Arrange
        mock_exists.return_value = True

        # Act
        ensure_gitignore()

        # Assert
        mock_exists.assert_called_once()
        # Check that file was opened twice: once for read, once for write
        assert mock_file.call_count == 2
        mock_file.assert_any_call(Path(".gitignore"), "r")
        mock_file.assert_any_call(Path(".gitignore"), "w")

        # Check the written content
        write_call = [
            call for call in mock_file.return_value.write.call_args_list if call[0][0]
        ][-1]
        written_content = write_call[0][0]
        assert ".claude/settings.local.json\n" == written_content

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="node_modules/\n*.log\n",
    )
    @patch("claude_setup.gitignore_manager.Path.exists")
    def test_ensure_gitignore_existing_content(self, mock_exists, mock_file):
        """Test adding pattern to .gitignore with existing content."""
        # Arrange
        mock_exists.return_value = True

        # Act
        ensure_gitignore()

        # Assert
        mock_exists.assert_called_once()
        assert mock_file.call_count == 2
        mock_file.assert_any_call(Path(".gitignore"), "r")
        mock_file.assert_any_call(Path(".gitignore"), "w")

        # Check the written content includes existing and new patterns
        write_call = [
            call for call in mock_file.return_value.write.call_args_list if call[0][0]
        ][-1]
        written_content = write_call[0][0]
        assert "node_modules/\n*.log\n.claude/settings.local.json\n" == written_content

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="node_modules/\n.claude/settings.local.json\n*.log\n",
    )
    @patch("claude_setup.gitignore_manager.Path.exists")
    def test_ensure_gitignore_pattern_already_exists(self, mock_exists, mock_file):
        """Test that pattern is not added if it already exists."""
        # Arrange
        mock_exists.return_value = True

        # Act
        ensure_gitignore()

        # Assert
        mock_exists.assert_called_once()
        # Should only read the file, not write
        mock_file.assert_called_once_with(Path(".gitignore"), "r")

    @patch("builtins.open", new_callable=mock_open)
    @patch("claude_setup.gitignore_manager.Path.exists")
    def test_ensure_gitignore_file_not_exists(self, mock_exists, mock_file):
        """Test creating .gitignore when file doesn't exist."""
        # Arrange
        mock_exists.return_value = False

        # Act
        ensure_gitignore()

        # Assert
        mock_exists.assert_called_once()
        # Should only write (create) the file
        mock_file.assert_called_once_with(Path(".gitignore"), "w")

        # Check the written content
        write_call = mock_file.return_value.write.call_args_list[0]
        written_content = write_call[0][0]
        assert ".claude/settings.local.json\n" == written_content

    @patch("builtins.open", new_callable=mock_open, read_data="   \n\n   \n")
    @patch("claude_setup.gitignore_manager.Path.exists")
    def test_ensure_gitignore_whitespace_only_file(self, mock_exists, mock_file):
        """Test handling .gitignore with only whitespace."""
        # Arrange
        mock_exists.return_value = True

        # Act
        ensure_gitignore()

        # Assert
        mock_exists.assert_called_once()
        assert mock_file.call_count == 2
        mock_file.assert_any_call(Path(".gitignore"), "r")
        mock_file.assert_any_call(Path(".gitignore"), "w")

        # Check the written content
        write_call = [
            call for call in mock_file.return_value.write.call_args_list if call[0][0]
        ][-1]
        written_content = write_call[0][0]
        assert ".claude/settings.local.json\n" == written_content

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="node_modules/\n# Comment\n\n*.log\n",
    )
    @patch("claude_setup.gitignore_manager.Path.exists")
    def test_ensure_gitignore_with_comments_and_empty_lines(
        self, mock_exists, mock_file
    ):
        """Test handling .gitignore with comments and empty lines."""
        # Arrange
        mock_exists.return_value = True

        # Act
        ensure_gitignore()

        # Assert
        mock_exists.assert_called_once()
        assert mock_file.call_count == 2

        # Check the written content preserves structure
        write_call = [
            call for call in mock_file.return_value.write.call_args_list if call[0][0]
        ][-1]
        written_content = write_call[0][0]
        expected = "node_modules/\n# Comment\n\n*.log\n.claude/settings.local.json\n"
        assert expected == written_content

    @patch("builtins.open", side_effect=PermissionError("Permission denied"))
    @patch("claude_setup.gitignore_manager.Path.exists")
    def test_ensure_gitignore_read_permission_error(self, mock_exists, mock_file):
        """Test handling permission error when reading .gitignore."""
        # Arrange
        mock_exists.return_value = True

        # Act & Assert
        with pytest.raises(PermissionError, match="Permission denied"):
            ensure_gitignore()

        mock_exists.assert_called_once()
        mock_file.assert_called_once_with(Path(".gitignore"), "r")

    @patch("builtins.open")
    @patch("claude_setup.gitignore_manager.Path.exists")
    def test_ensure_gitignore_write_permission_error(self, mock_exists, mock_file):
        """Test handling permission error when writing .gitignore."""
        # Arrange
        mock_exists.return_value = True
        mock_file.side_effect = [
            mock_open(read_data="node_modules/\n").return_value,  # Read succeeds
            PermissionError("Permission denied"),  # Write fails
        ]

        # Act & Assert
        with pytest.raises(PermissionError, match="Permission denied"):
            ensure_gitignore()

        mock_exists.assert_called_once()
        assert mock_file.call_count == 2

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=("node_modules/\n.claude/settings.local.json\n" "similar-pattern\n"),
    )
    @patch("claude_setup.gitignore_manager.Path.exists")
    def test_ensure_gitignore_similar_pattern_exists(self, mock_exists, mock_file):
        """Test that exact pattern match is required."""
        # Arrange
        mock_exists.return_value = True

        # Act
        ensure_gitignore()

        # Assert
        mock_exists.assert_called_once()
        # Should only read the file since exact pattern exists
        mock_file.assert_called_once_with(Path(".gitignore"), "r")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="node_modules/\n.claude/settings.local.json  \n*.log\n",
    )
    @patch("claude_setup.gitignore_manager.Path.exists")
    def test_ensure_gitignore_pattern_with_trailing_spaces(
        self, mock_exists, mock_file
    ):
        """Test that trailing spaces in existing pattern don't match."""
        # Arrange
        mock_exists.return_value = True

        # Act
        ensure_gitignore()

        # Assert
        mock_exists.assert_called_once()
        assert mock_file.call_count == 2  # Read and write
        mock_file.assert_any_call(Path(".gitignore"), "r")
        mock_file.assert_any_call(Path(".gitignore"), "w")

        # Check that the pattern was added despite similar line
        # with trailing spaces
        write_call = [
            call for call in mock_file.return_value.write.call_args_list if call[0][0]
        ][-1]
        written_content = write_call[0][0]
        assert ".claude/settings.local.json" in written_content
        # Should have both the original line with spaces and the new clean line
        lines = written_content.strip().split("\n")
        assert ".claude/settings.local.json  " in lines
        assert ".claude/settings.local.json" in lines

    @patch("builtins.open", side_effect=IOError("Disk full"))
    @patch("claude_setup.gitignore_manager.Path.exists")
    def test_ensure_gitignore_io_error(self, mock_exists, mock_file):
        """Test handling IO error when accessing .gitignore."""
        # Arrange
        mock_exists.return_value = True

        # Act & Assert
        with pytest.raises(IOError, match="Disk full"):
            ensure_gitignore()

        mock_exists.assert_called_once()
        mock_file.assert_called_once_with(Path(".gitignore"), "r")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="line1\nline2\nline3",
    )
    @patch("claude_setup.gitignore_manager.Path.exists")
    def test_ensure_gitignore_no_trailing_newline(self, mock_exists, mock_file):
        """Test handling .gitignore without trailing newline."""
        # Arrange
        mock_exists.return_value = True

        # Act
        ensure_gitignore()

        # Assert
        mock_exists.assert_called_once()
        assert mock_file.call_count == 2

        # Check the written content adds pattern properly
        write_call = [
            call for call in mock_file.return_value.write.call_args_list if call[0][0]
        ][-1]
        written_content = write_call[0][0]
        assert "line1\nline2\nline3\n.claude/settings.local.json\n" == written_content
