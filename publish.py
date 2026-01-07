#!/usr/bin/env python3
"""
Helper script for publishing pyhscodes to PyPI.

Usage:
    python publish.py test    # Build and upload to TestPyPI
    python publish.py prod    # Build and upload to PyPI
"""

import shutil
import subprocess
import sys
import os


def run_command(cmd, description, show_output=False):
    """Run a command and handle errors."""
    print(f"\n📦 {description}...")
    try:
        result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {description} completed successfully")
        if show_output and result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False


def get_version():
    """Extract version from pyproject.toml."""
    try:
        with open("pyproject.toml", "r") as f:
            for line in f:
                if line.strip().startswith("version"):
                    return line.split("=")[1].strip().strip('"')
    except Exception:
        pass
    return "unknown"


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["test", "prod"]:
        print("Usage: python publish.py [test|prod]")
        print("  test - Build and upload to TestPyPI")
        print("  prod - Build and upload to PyPI")
        sys.exit(1)

    target = sys.argv[1]
    version = get_version()

    print("🚀 pyhscodes Publishing Script")
    print("=" * 40)
    print(f"📋 Version: {version}")
    print(f"🎯 Target: {'TestPyPI' if target == 'test' else 'PyPI'}")

    # Clean old dist directory
    if os.path.exists("dist"):
        print("\n🧹 Cleaning old dist directory...")
        shutil.rmtree("dist")
        print("✅ Old dist directory removed")

    # Build the package
    if not run_command("python -m build", "Building distribution"):
        print("❌ Build failed. Make sure 'build' is installed: pip install build")
        sys.exit(1)

    # Check if twine is installed
    if not run_command(
        "twine --version", "Checking twine installation", show_output=True
    ):
        print("❌ Please install twine: pip install twine")
        sys.exit(1)

    # Validate distribution files
    if not run_command("twine check dist/*", "Validating distribution files"):
        sys.exit(1)

    # Upload to appropriate repository
    if target == "test":
        print("\n🧪 Uploading to TestPyPI...")
        print("When prompted, use:")
        print("  Username: __token__")
        print("  Password: your-testpypi-api-token")
        cmd = "twine upload --repository testpypi dist/*"
    else:
        print("\n🌟 Uploading to PyPI...")
        print("When prompted, use:")
        print("  Username: __token__")
        print("  Password: your-pypi-api-token")
        cmd = "twine upload dist/*"

    if run_command(cmd, f"Uploading to {'TestPyPI' if target == 'test' else 'PyPI'}"):
        if target == "test":
            print("\n✅ Upload to TestPyPI successful!")
            print("Test installation with:")
            print("  pip install --index-url https://test.pypi.org/simple/ pyhscodes")
        else:
            print("\n🎉 Upload to PyPI successful!")
            print(
                "Your package is now available at: https://pypi.org/project/pyhscodes/"
            )
            print("Install with: pip install pyhscodes")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
