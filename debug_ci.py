#!/usr/bin/env python3
"""Debug script for CI import issues."""
import sys
import os
import subprocess

print("=== CI Debug Information ===")
print(f"Python: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")
print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")
print()

print("=== Python Path ===")
for i, path in enumerate(sys.path):
    print(f"{i}: {path}")
print()

print("=== pip list ===")
subprocess.run([sys.executable, "-m", "pip", "list"], check=True)
print()

print("=== Package installation check ===")
result = subprocess.run(
    [sys.executable, "-m", "pip", "show", "claude-bedrock-setup"],
    capture_output=True,
    text=True
)
if result.returncode == 0:
    print(result.stdout)
else:
    print("claude-bedrock-setup not found via pip show")
    print(result.stderr)
print()

print("=== Direct import test ===")
try:
    import claude_setup
    print(f"✓ import claude_setup succeeded")
    print(f"  Version: {claude_setup.__version__}")
    print(f"  Location: {claude_setup.__file__}")
except Exception as e:
    print(f"✗ import claude_setup failed: {e}")
    import traceback
    traceback.print_exc()
print()

print("=== Click import test ===")
try:
    from claude_setup import cli
    print(f"✓ from claude_setup import cli succeeded")
    print(f"  CLI object: {cli}")
except Exception as e:
    print(f"✗ from claude_setup import cli failed: {e}")
    import traceback
    traceback.print_exc()