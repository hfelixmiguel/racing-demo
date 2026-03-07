"""
Vercel Build Script for Racing Demo

This script handles the build process for deploying the racing demo
application to Vercel. It sets up the virtual environment, installs
dependencies, and prepares the application for deployment.
"""

import os
import subprocess
import sys
from pathlib import Path


def setup_python_environment():
    """Set up Python virtual environment."""
    venv_path = Path('.venv')
    
    # Check if venv already exists
    if venv_path.exists():
        print('Virtual environment already exists. Updating...')
        subprocess.run([sys.executable, 'ensurepip', '--upgrade'], check=True)
        subprocess.run([str(venv_path / 'bin' / 'python'), '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
    else:
        print('Creating virtual environment...')
        subprocess.run([sys.executable, '-m', 'venv', str(venv_path)], check=True)
    
    # Get venv Python executable
    if os.name == 'nt':  # Windows
        python_exec = str(venv_path / 'Scripts' / 'python')
        pip_exec = str(venv_path / 'Scripts' / 'pip')
    else:  # Linux/Mac
        python_exec = str(venv_path / 'bin' / 'python')
        pip_exec = str(venv_path / 'bin' / 'pip')
    
    return python_exec, pip_exec


def install_dependencies(pip_exec):
    """Install Python dependencies from requirements.txt."""
    print('Installing dependencies...')
    result = subprocess.run(
        [pip_exec, 'install', '-r', 'requirements.txt'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print('Error installing dependencies:')
        print(result.stderr)
        raise RuntimeError(f'Failed to install dependencies: {result.stderr}')
    
    print('Dependencies installed successfully.')
    return True


def verify_installation(python_exec):
    """Verify that key dependencies are installed."""
    import sys
    
    # Test imports
    try:
        import arcade
        print(f'✓ Arcade version {arcade.__version__}')
    except ImportError as e:
        raise RuntimeError(f'Arcade not installed: {e}')
    
    try:
        import flask
        print(f'✓ Flask version {flask.__version__}')
    except ImportError as e:
        raise RuntimeError(f'Flask not installed: {e}')
    
    try:
        import numpy
        print(f'✓ NumPy version {numpy.__version__}')
    except ImportError as e:
        raise RuntimeError(f'NumPy not installed: {e}')
    
    return True


def main():
    """Main build function."""
    print('=' * 60)
    print('Vercel Build Script for Racing Demo')
    print('=' * 60)
    
    try:
        # Setup environment
        python_exec, pip_exec = setup_python_environment()
        
        # Install dependencies
        install_dependencies(pip_exec)
        
        # Verify installation
        verify_installation(python_exec)
        
        print('=' * 60)
        print('Build completed successfully!')
        print('=' * 60)
        
    except Exception as e:
        print(f'Build failed: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
