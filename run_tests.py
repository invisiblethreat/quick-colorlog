#!/usr/bin/env python3
"""
Test runner script for quick-colorlog.

This script provides an easy way to run all tests and generate coverage reports.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print("=" * 60)

    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        print("Make sure pytest is installed: pip install pytest")
        return False


def main():
    """Main test runner function."""
    project_root = Path(__file__).parent

    print("🧪 Quick-ColorLog Test Runner")
    print(f"Project root: {project_root}")

    # Change to project directory
    import os

    os.chdir(project_root)

    # Test commands to run
    test_commands = [
        # Basic test run
        {
            "cmd": ["python", "-m", "pytest", "tests/", "-v"],
            "description": "Running all tests with verbose output",
        },
        # Test with coverage
        {
            "cmd": [
                "python",
                "-m",
                "pytest",
                "tests/",
                "--cov=quick_colorlog",
                "--cov-report=term-missing",
            ],
            "description": "Running tests with coverage report",
        },
        # Regression tests specifically
        {
            "cmd": [
                "python",
                "-m",
                "pytest",
                "tests/test_regression.py",
                "-v",
                "-m",
                "regression",
            ],
            "description": "Running regression tests specifically",
        },
        # Double logging tests
        {
            "cmd": ["python", "-m", "pytest", "tests/test_double_logging.py", "-v"],
            "description": "Running double logging prevention tests",
        },
    ]

    success_count = 0
    total_count = len(test_commands)

    for test_config in test_commands:
        if run_command(test_config["cmd"], test_config["description"]):
            success_count += 1
        else:
            print(f"\n⚠️  Test command failed, but continuing with remaining tests...")

    # Summary
    print(f"\n{'='*60}")
    print("📊 Test Summary")
    print("=" * 60)
    print(f"Successful test runs: {success_count}/{total_count}")

    if success_count == total_count:
        print("🎉 All test commands completed successfully!")
        sys.exit(0)
    else:
        print("⚠️  Some test commands failed. Check the output above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
