#!/usr/bin/env python3
"""Test runner script for claude-setup CLI application."""

import subprocess
import sys
from pathlib import Path


def run_tests():
    """Run the test suite with coverage reporting."""
    print("Running claude-setup test suite...")
    print("=" * 60)

    # Change to project directory
    project_dir = Path(__file__).parent

    try:
        # Run tests with coverage
        cmd = [
            "pipenv",
            "run",
            "pytest",
            "tests/",
            "-v",
            "--cov=src/claude_setup",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov",
            "--cov-fail-under=95",
        ]

        result = subprocess.run(cmd, cwd=project_dir, check=False)

        if result.returncode == 0:
            print("\n" + "=" * 60)
            print("✅ All tests passed! Coverage target met.")
            print("📊 HTML coverage report generated in htmlcov/")
        else:
            print("\n" + "=" * 60)
            print("❌ Some tests failed or coverage target not met.")
            sys.exit(1)

    except FileNotFoundError:
        print("❌ Error: pipenv not found. Please install pipenv first.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
