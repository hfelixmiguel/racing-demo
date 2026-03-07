"""
Vercel Build Script for Racing Demo

This script handles the installation of dependencies in a Vercel-compatible way,
resolving PEP 668 externally-managed-environment errors.
"""

import subprocess
import sys
import os


def install_dependencies():
    """Install Python dependencies using uv or pip with appropriate flags."""
    
    # Check if uv is available (preferred for modern Python environments)
    try:
        result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("Using uv for dependency installation...")
            # Create virtual environment and install dependencies
            subprocess.run([
                "uv", "pip", "install", 
                "-r", "requirements.txt"
            ], check=True)
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Fallback to pip with --break-system-packages flag
    print("Using pip with --break-system-packages...")
    subprocess.run([
        sys.executable, "-m", "pip", "install", 
        "--break-system-packages",
        "-r", "requirements.txt"
    ], check=True)
    return True


def main():
    """Main entry point for the build script."""
    print("=" * 60)
    print("Racing Demo - Vercel Build Script")
    print("=" * 60)
    
    try:
        install_dependencies()
        print("\n✅ Dependencies installed successfully!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error installing dependencies: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
