#!/usr/bin/env python3
"""
Check and install requirements for testing.
"""

import subprocess
import sys
import os


def check_and_install_requirements():
    """Check if requirements are installed and install if missing."""
    requirements_file = os.path.join(os.path.dirname(__file__), "..", "requirements.txt")

    try:
        # Try to import pygame to see if it's available
        import pygame

        print("✓ pygame is available")
    except ImportError:
        print("✗ pygame not found, installing requirements...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
            print("✓ Requirements installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install requirements: {e}")
            sys.exit(1)

    try:
        import pytest

        print("✓ pytest is available")
    except ImportError:
        print("✗ pytest not found, installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest", "pytest-cov"])
            print("✓ pytest installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install pytest: {e}")
            sys.exit(1)


if __name__ == "__main__":
    check_and_install_requirements()
