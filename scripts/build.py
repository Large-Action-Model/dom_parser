#!/usr/bin/env python3
"""
Build script for DOM Parser package.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, check=True):
    """Run a command and handle errors."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=check)
    return result.returncode == 0

def clean():
    """Clean build artifacts."""
    print("Cleaning build artifacts...")
    
    # Remove build directories
    for path in ["build", "dist", "*.egg-info"]:
        run_command(f"rm -rf {path}", check=False)
    
    # Remove Python cache
    run_command("find . -name '__pycache__' -type d -exec rm -rf {} +", check=False)
    run_command("find . -name '*.pyc' -delete", check=False)

def format_code():
    """Format code with black."""
    print("Formatting code...")
    return run_command("black src/ tests/ examples/")

def lint():
    """Run linting."""
    print("Running linting...")
    success = True
    success &= run_command("flake8 src/ tests/ examples/")
    success &= run_command("mypy dom_parser/")
    return success

def test():
    """Run tests."""
    print("Running tests...")
    return run_command("pytest tests/")

def build():
    """Build the package."""
    print("Building package...")
    return run_command("python setup.py sdist bdist_wheel")

def install_dev():
    """Install package in development mode."""
    print("Installing in development mode...")
    return run_command("pip install -e .[dev]")

def main():
    """Main build script."""
    if len(sys.argv) < 2:
        print("Usage: python build.py [clean|format|lint|test|build|install-dev|all]")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "clean":
        clean()
    elif action == "format":
        format_code()
    elif action == "lint":
        if not lint():
            sys.exit(1)
    elif action == "test":
        if not test():
            sys.exit(1)
    elif action == "build":
        if not build():
            sys.exit(1)
    elif action == "install-dev":
        if not install_dev():
            sys.exit(1)
    elif action == "all":
        clean()
        if not format_code():
            sys.exit(1)
        if not lint():
            sys.exit(1)
        if not test():
            sys.exit(1)
        if not build():
            sys.exit(1)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
    
    print("Done!")

if __name__ == "__main__":
    main()