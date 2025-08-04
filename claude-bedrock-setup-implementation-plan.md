# Claude Bedrock Setup CLI Implementation Plan

## Executive Summary

This CLI tool streamlines the configuration of Claude to use AWS Bedrock as its backend provider. It automates the discovery of available Claude models, manages authentication, and persists settings in a local configuration file. The tool provides a user-friendly interface for developers to quickly set up and switch between different Claude models available through AWS Bedrock.

**Business Value:**
- Eliminates manual configuration errors
- Reduces setup time from minutes to seconds
- Provides consistent configuration across team members
- Enables easy model switching for different use cases

**Technical Approach:**
- Python CLI using Click framework for intuitive command structure
- boto3 for AWS Bedrock API interactions
- JSON-based configuration management
- Interactive prompts for user-friendly experience

**AWS Services:**
- AWS Bedrock (model discovery and inference)
- AWS STS (authentication verification)
- IAM (permission checking)

**Estimated Complexity:** Medium
**Timeline:** 2-3 days for full implementation

## Detailed Implementation Plan

### Phase 1: Foundation (Day 1 Morning)

#### 1.1 Project Structure Setup
```
claude-bedrock-setup/
├── setup.py
├── requirements.txt
├── .gitignore
├── README.md
├── claude_bedrock_setup/
│   ├── __init__.py
│   ├── cli.py
│   ├── aws_client.py
│   ├── config_manager.py
│   ├── auth_checker.py
│   └── utils.py
└── tests/
    ├── __init__.py
    ├── test_cli.py
    ├── test_aws_client.py
    └── test_config_manager.py
```

#### 1.2 Core Dependencies
```txt
# requirements.txt
click>=8.1.0
boto3>=1.28.0
rich>=13.0.0  # For enhanced CLI output
python-dotenv>=1.0.0
pytest>=7.0.0
pytest-mock>=3.0.0
```

#### 1.3 Basic CLI Framework
- Implement main CLI entry point with Click
- Set up command structure for `setup`, `configure`, and `status` commands
- Implement help text and version information
- Add basic error handling and logging setup

### Phase 2: Core Functionality (Day 1 Afternoon - Day 2 Morning)

#### 2.1 AWS Authentication Module (`auth_checker.py`)
```python
class AWSAuthChecker:
    def __init__(self):
        self.sts_client = None
        
    def check_authentication(self) -> tuple[bool, dict]:
        """
        Checks if AWS credentials are valid and accessible.
        Returns (is_authenticated, account_info)
        """
        
    def get_current_region(self) -> str:
        """
        Returns the current AWS region from environment or config.
        """
        
    def prompt_for_login(self) -> None:
        """
        Provides instructions for AWS authentication setup.
        """
```

#### 2.2 Bedrock Client Module (`aws_client.py`)
```python
class BedrockClient:
    def __init__(self, region: str = None):
        self.bedrock_client = None
        self.region = region or self._get_default_region()
        
    def list_available_models(self) -> list[dict]:
        """
        Retrieves available Claude models from Bedrock.
        Filters by "inference-profile/us.anthropic.claude-"
        """
        
    def validate_model_access(self, model_arn: str) -> bool:
        """
        Verifies user has access to the specified model.
        """
        
    def get_model_details(self, model_arn: str) -> dict:
        """
        Fetches detailed information about a specific model.
        """
```

#### 2.3 Configuration Manager (`config_manager.py`)
```python
class ConfigManager:
    DEFAULT_CONFIG = {
        "CLAUDE_CODE_USE_BEDROCK": "1",
        "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "4096",
        "MAX_THINKING_TOKENS": "1024"
    }
    
    def __init__(self, config_path: Path = None):
        self.config_path = config_path or Path.home() / ".claude" / "settings.local.json"
        
    def load_config(self) -> dict:
        """Loads existing configuration or returns defaults."""
        
    def save_config(self, config: dict) -> None:
        """Saves configuration to settings.local.json."""
        
    def update_gitignore(self) -> None:
        """Ensures .gitignore includes settings.local.json."""
        
    def merge_config(self, updates: dict) -> dict:
        """Merges new settings with existing configuration."""
```

#### 2.4 Main CLI Implementation (`cli.py`)
```python
@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Claude Bedrock Setup - Configure Claude to use AWS Bedrock."""
    pass

@cli.command()
@click.option('--region', help='AWS region to use')
@click.option('--profile', help='AWS profile to use')
def setup(region, profile):
    """Interactive setup wizard for Claude Bedrock configuration."""
    # 1. Check AWS authentication
    # 2. List available models
    # 3. Interactive model selection
    # 4. Save configuration
    # 5. Update .gitignore
    
@cli.command()
@click.option('--model', help='Model ARN to configure')
@click.option('--region', help='AWS region')
@click.option('--max-output-tokens', type=int, default=4096)
@click.option('--max-thinking-tokens', type=int, default=1024)
def configure(model, region, max_output_tokens, max_thinking_tokens):
    """Configure specific settings manually."""
    
@cli.command()
def status():
    """Display current configuration and authentication status."""
```

### Phase 3: Enhancement (Day 2 Afternoon - Day 3)

#### 3.1 Interactive Model Selection
```python
def interactive_model_selector(models: list[dict]) -> str:
    """
    Present models in a user-friendly table format:
    - Model ID
    - Model Name
    - Status
    - Region
    - Description
    
    Uses rich library for enhanced terminal output.
    """
```

#### 3.2 Advanced Error Handling
- AWS permission errors with helpful messages
- Network connectivity issues
- Invalid model selection
- Configuration file corruption
- Region-specific availability

#### 3.3 Testing Suite
```python
# test_cli.py
def test_setup_command_flow():
    """Test complete setup wizard flow."""
    
def test_configure_command():
    """Test manual configuration."""
    
def test_status_command():
    """Test status display."""

# test_aws_client.py
def test_model_listing():
    """Test Bedrock model discovery."""
    
def test_authentication_check():
    """Test AWS auth verification."""

# test_config_manager.py
def test_config_persistence():
    """Test configuration save/load."""
    
def test_gitignore_update():
    """Test .gitignore management."""
```

#### 3.4 Documentation and Distribution
- Comprehensive README with usage examples
- Inline code documentation
- Setup.py for pip installation
- GitHub Actions workflow for testing

## Technical Specifications

### CLI Structure

```bash
# Primary setup command (interactive)
claude-bedrock-setup setup

# Manual configuration
claude-bedrock-setup configure --model arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0 --region us-east-1

# Check current configuration
claude-bedrock-setup status

# Get help
claude-bedrock-setup --help
claude-bedrock-setup setup --help
```

### Configuration File Format

```json
{
  "CLAUDE_CODE_USE_BEDROCK": "1",
  "AWS_REGION": "us-east-1",
  "ANTHROPIC_MODEL": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0",
  "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "4096",
  "MAX_THINKING_TOKENS": "1024"
}
```

### User Experience Flow

1. **Initial Setup**
   ```
   $ claude-bedrock-setup setup
   
   🔍 Checking AWS authentication...
   ✅ Authenticated as: user@example.com (Account: 123456789012)
   
   🌎 Current region: us-east-1
   Use a different region? [y/N]: n
   
   📋 Available Claude models in us-east-1:
   
   1. Claude 3.5 Sonnet v2 (Latest)
      ARN: arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0
      
   2. Claude 3.5 Haiku
      ARN: arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-haiku-20241022-v1:0
      
   3. Claude 3 Opus
      ARN: arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-opus-20240307-v1:0
   
   Select a model [1-3]: 1
   
   ⚙️  Configuring Claude with:
   - Model: Claude 3.5 Sonnet v2
   - Region: us-east-1
   - Max Output Tokens: 4096
   - Max Thinking Tokens: 1024
   
   Proceed? [Y/n]: y
   
   ✅ Configuration saved to ~/.claude/settings.local.json
   ✅ Updated .gitignore to exclude settings file
   
   🎉 Setup complete! Claude is now configured to use AWS Bedrock.
   ```

2. **Authentication Required**
   ```
   $ claude-bedrock-setup setup
   
   🔍 Checking AWS authentication...
   ❌ AWS credentials not found or expired
   
   To authenticate with AWS, please run one of the following:
   
   1. Configure AWS CLI:
      $ aws configure
      
   2. Use AWS SSO:
      $ aws sso login --profile your-profile
      
   3. Set environment variables:
      export AWS_ACCESS_KEY_ID=your-key
      export AWS_SECRET_ACCESS_KEY=your-secret
      export AWS_REGION=us-east-1
   
   After authenticating, run this command again.
   ```

3. **Status Check**
   ```
   $ claude-bedrock-setup status
   
   Claude Bedrock Configuration Status
   ===================================
   
   ✅ AWS Authentication: Valid
      Account: 123456789012
      User: user@example.com
      
   ✅ Configuration File: ~/.claude/settings.local.json
   
   Current Settings:
   - CLAUDE_CODE_USE_BEDROCK: 1
   - AWS_REGION: us-east-1
   - ANTHROPIC_MODEL: Claude 3.5 Sonnet v2
   - CLAUDE_CODE_MAX_OUTPUT_TOKENS: 4096
   - MAX_THINKING_TOKENS: 1024
   
   ✅ Model Access: Verified
   ```

### Error Handling Examples

```python
# Permission Error
class BedrockPermissionError(Exception):
    def __init__(self, model_arn):
        super().__init__(
            f"Access denied to model: {model_arn}\n"
            f"Please ensure your AWS account has Bedrock model access enabled.\n"
            f"Visit: https://console.aws.amazon.com/bedrock/home#/modelaccess"
        )

# Region Error
class RegionNotSupportedError(Exception):
    def __init__(self, region):
        super().__init__(
            f"Region '{region}' does not support AWS Bedrock.\n"
            f"Supported regions: us-east-1, us-west-2, eu-west-1, ap-southeast-1"
        )
```

### Security Considerations

1. **Credential Management**
   - Never store AWS credentials in configuration files
   - Rely on AWS SDK credential chain
   - Validate permissions before saving configuration

2. **File Permissions**
   - Set appropriate permissions on settings.local.json (600)
   - Ensure .claude directory is user-readable only

3. **Input Validation**
   - Validate model ARNs match expected pattern
   - Sanitize all user inputs
   - Verify region codes against allowed list

### Testing Strategy

1. **Unit Tests**
   - Mock AWS API calls
   - Test configuration file operations
   - Validate error handling paths

2. **Integration Tests**
   - Test with real AWS credentials (optional)
   - Verify end-to-end setup flow
   - Test various authentication methods

3. **User Acceptance Tests**
   - Test on different operating systems
   - Verify with various AWS account configurations
   - Test error recovery scenarios

### Future Enhancements

1. **Model Comparison**
   - Display pricing information
   - Show performance characteristics
   - Compare feature availability

2. **Profile Management**
   - Support multiple configuration profiles
   - Quick switching between models
   - Team configuration sharing

3. **Advanced Features**
   - Model usage tracking
   - Cost estimation
   - Performance benchmarking
   - Auto-update notifications

## Implementation Timeline

**Day 1:**
- Morning: Project setup and basic CLI framework
- Afternoon: AWS authentication and Bedrock client implementation

**Day 2:**
- Morning: Configuration management and core setup flow
- Afternoon: Interactive features and error handling

**Day 3:**
- Morning: Testing suite implementation
- Afternoon: Documentation and packaging

## Success Criteria

1. **Functional Requirements**
   - ✓ Successful AWS authentication detection
   - ✓ Accurate model discovery from Bedrock
   - ✓ Reliable configuration persistence
   - ✓ Proper .gitignore management

2. **Non-Functional Requirements**
   - ✓ Setup completes in under 30 seconds
   - ✓ Clear error messages for all failure modes
   - ✓ Works on Python 3.8+
   - ✓ Cross-platform compatibility (Windows, macOS, Linux)

3. **User Experience**
   - ✓ Intuitive command structure
   - ✓ Helpful prompts and feedback
   - ✓ Graceful error recovery
   - ✓ Comprehensive help documentation