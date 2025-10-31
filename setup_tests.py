#!/usr/bin/env python3
"""
Setup script for alg-snake testing environment.
Run this once to install all dependencies needed for testing.
"""

import subprocess
import sys
import os


def main():
    """Setup testing environment."""
    print("Setting up alg-snake testing environment...")
    print("=" * 50)

    # Get project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_file = os.path.join(project_dir, "requirements.txt")

    if not os.path.exists(requirements_file):
        print("❌ requirements.txt not found!")
        print(f"Expected at: {requirements_file}")
        sys.exit(1)

    print("📦 Installing requirements from requirements.txt...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", requirements_file], capture_output=True, text=True
        )

        if result.returncode == 0:
            print("✅ Requirements installed successfully!")
        else:
            print("❌ Failed to install requirements:")
            print(result.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error installing requirements: {e}")
        sys.exit(1)

    # Verify installations
    print("\n🔍 Verifying installations...")

    try:
        import pygame

        print(f"✅ pygame {pygame.version.ver} - OK")
    except ImportError:
        print("❌ pygame - FAILED")

    try:
        import pytest

        print(f"✅ pytest - OK")
    except ImportError:
        print("❌ pytest - FAILED")

    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\nNow you can run tests with:")
    print("  python run_tests.py all")
    print("  pytest tests/ -v")
    print("\nOr run individual test categories:")
    print("  python run_tests.py unit")
    print("  python run_tests.py integration")
    print("  python run_tests.py coverage")


if __name__ == "__main__":
    main()
