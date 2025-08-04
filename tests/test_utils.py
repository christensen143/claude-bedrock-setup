"""Test utilities and helper functions for claude-setup tests."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock


def create_temp_settings_file(settings_dict, temp_dir):
    """Create a temporary settings file for testing.
    
    Args:
        settings_dict: Dictionary of settings to write
        temp_dir: Temporary directory path
        
    Returns:
        Path to the created settings file
    """
    claude_dir = temp_dir / ".claude"
    claude_dir.mkdir(exist_ok=True)
    
    settings_file = claude_dir / "settings.local.json"
    with open(settings_file, 'w') as f:
        json.dump(settings_dict, f, indent=2)
    
    return settings_file


def create_temp_gitignore(content, temp_dir):
    """Create a temporary .gitignore file for testing.
    
    Args:
        content: Content to write to .gitignore
        temp_dir: Temporary directory path
        
    Returns:
        Path to the created .gitignore file
    """
    gitignore_file = temp_dir / ".gitignore"
    with open(gitignore_file, 'w') as f:
        f.write(content)
    
    return gitignore_file


def mock_subprocess_success(stdout_data="", stderr_data=""):
    """Create a mock subprocess.run for successful execution.
    
    Args:
        stdout_data: Data to return as stdout
        stderr_data: Data to return as stderr
        
    Returns:
        Mock object configured for successful subprocess execution
    """
    mock = MagicMock()
    mock.returncode = 0
    mock.stdout = stdout_data
    mock.stderr = stderr_data
    return mock


def mock_subprocess_failure(returncode=1, stdout_data="", stderr_data=""):
    """Create a mock subprocess.run for failed execution.
    
    Args:
        returncode: Return code for the failed process
        stdout_data: Data to return as stdout
        stderr_data: Data to return as stderr
        
    Returns:
        Mock object configured for failed subprocess execution
    """
    mock = MagicMock()
    mock.returncode = returncode
    mock.stdout = stdout_data
    mock.stderr = stderr_data
    return mock


class MockPath:
    """Mock Path object for testing file system operations."""
    
    def __init__(self, path_str, exists=True):
        self.path_str = path_str
        self._exists = exists
        self.mkdir_called = False
        self.unlink_called = False
    
    def __str__(self):
        return self.path_str
    
    def __truediv__(self, other):
        return MockPath(f"{self.path_str}/{other}", self._exists)
    
    def exists(self):
        return self._exists
    
    def mkdir(self, exist_ok=False):
        self.mkdir_called = True
        if not exist_ok and self._exists:
            raise FileExistsError("Directory already exists")
    
    def unlink(self):
        if not self._exists:
            raise FileNotFoundError("File does not exist")
        self.unlink_called = True


def assert_subprocess_called_with(mock_run, expected_cmd, expected_kwargs=None):
    """Assert that subprocess.run was called with expected arguments.
    
    Args:
        mock_run: Mock subprocess.run object
        expected_cmd: Expected command list
        expected_kwargs: Expected keyword arguments
    """
    mock_run.assert_called_once()
    call_args, call_kwargs = mock_run.call_args
    
    assert call_args[0] == expected_cmd
    
    if expected_kwargs:
        for key, value in expected_kwargs.items():
            assert call_kwargs.get(key) == value


def create_mock_aws_response(models_data):
    """Create a mock AWS list-inference-profiles response.
    
    Args:
        models_data: List of model dictionaries with keys: id, name, arn, status
        
    Returns:
        Dictionary in AWS response format
    """
    summaries = []
    for model in models_data:
        summary = {
            'inferenceProfileId': model['id'],
            'inferenceProfileName': model.get('name', model['id']),
            'inferenceProfileArn': model.get('arn', ''),
            'status': model.get('status', 'ACTIVE')
        }
        summaries.append(summary)
    
    return {'inferenceProfileSummaries': summaries}


class CLITestHelper:
    """Helper class for CLI testing."""
    
    @staticmethod
    def run_cli_command(runner, command, args=None, input_data=None, catch_exceptions=True):
        """Run a CLI command with standard error handling.
        
        Args:
            runner: Click test runner
            command: CLI command to run
            args: Command arguments list
            input_data: Input to provide to command
            catch_exceptions: Whether to catch exceptions
            
        Returns:
            Click Result object
        """
        cmd_args = args or []
        return runner.invoke(
            command, 
            cmd_args, 
            input=input_data, 
            catch_exceptions=catch_exceptions
        )
    
    @staticmethod
    def assert_success(result, expected_output=None):
        """Assert that CLI command succeeded.
        
        Args:
            result: Click Result object
            expected_output: Expected output string (optional)
        """
        assert result.exit_code == 0, f"Command failed with output: {result.output}"
        if expected_output:
            assert expected_output in result.output
    
    @staticmethod
    def assert_failure(result, expected_exit_code=1, expected_output=None):
        """Assert that CLI command failed.
        
        Args:
            result: Click Result object
            expected_exit_code: Expected exit code
            expected_output: Expected output string (optional)
        """
        assert result.exit_code == expected_exit_code, f"Expected exit code {expected_exit_code}, got {result.exit_code}"
        if expected_output:
            assert expected_output in result.output