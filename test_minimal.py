"""Minimal test to debug CI failures."""
import sys
print(f"Python: {sys.version}")
print(f"Path: {sys.path[:3]}")

try:
    # Test 1: Basic import
    import claude_setup
    print("✓ import claude_setup")
    
    # Test 2: Check version
    print(f"✓ version: {claude_setup.__version__}")
    
    # Test 3: Import from package
    from claude_setup import cli
    print("✓ from claude_setup import cli")
    
    # Test 4: Direct module import
    from claude_setup.cli import cli as cli2
    print("✓ from claude_setup.cli import cli")
    
    # Test 5: Run basic CLI command
    from click.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    print(f"✓ CLI output: {result.output.strip()}")
    print(f"✓ Exit code: {result.exit_code}")
    
except Exception as e:
    import traceback
    print(f"\n✗ ERROR: {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\nAll tests passed!")