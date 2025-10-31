#!/usr/bin/env python3
"""
Test runner script for alg-snake project.
Provides convenient ways to run different test suites.
"""

import subprocess
import sys
import os


def run_command(command):
    """Run a command and return the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False


def check_requirements():
    """Check if required packages are available."""
    try:
        import pygame
        import pytest

        return True
    except ImportError as e:
        print(f"Missing required packages: {e}")
        print("\nPlease install requirements:")
        print("  pip install -r requirements.txt")
        print("\nOr run:")
        print("  python tests/check_requirements.py")
        return False


def main():
    """Main test runner function."""
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py [unit|integration|all|coverage]")
        print("  unit        - Run unit tests only")
        print("  integration - Run integration tests only")
        print("  all         - Run all tests")
        print("  coverage    - Run all tests with coverage report")
        sys.exit(1)

    # Check requirements first
    if not check_requirements():
        sys.exit(1)

    test_type = sys.argv[1].lower()

    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    if test_type == "unit":
        print("Running unit tests...")
        success = run_command("pytest tests/unit/ -m unit -v")
    elif test_type == "integration":
        print("Running integration tests...")
        success = run_command("pytest tests/integration/ -m integration -v")
    elif test_type == "all":
        print("Running all tests...")
        success = run_command("pytest tests/ -v")
    elif test_type == "coverage":
        print("Running tests with coverage...")
        success = run_command("pytest tests/ --cov=. --cov-report=html --cov-report=term")
        if success:
            print("\nCoverage report generated in htmlcov/index.html")
    else:
        print(f"Unknown test type: {test_type}")
        sys.exit(1)

    if success:
        print("\n✓ Tests completed successfully!")
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
