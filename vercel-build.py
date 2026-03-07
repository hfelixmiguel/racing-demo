"""
Vercel Build Script for Racing Demo

This script prepares the Flask application for deployment on Vercel.
It installs dependencies and sets up the environment properly.
"""

import subprocess
import sys
from pathlib import Path


def install_dependencies():
    """Install Python dependencies from requirements.txt."""
    print("📦 Installing dependencies...")
    
    try:
        # Install Flask and other dependencies
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def verify_flask():
    """Verify Flask is installed correctly."""
    print("🔍 Verifying Flask installation...")
    
    try:
        import flask
        print(f"✅ Flask version: {flask.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Failed to import Flask: {e}")
        return False


def create_wsgi_entry():
    """Create WSGI entry point if it doesn't exist."""
    print("📝 Checking WSGI entry point...")
    
    wsgi_path = Path("wsgi.py")
    
    if not wsgi_path.exists():
        print("⚠️  Creating wsgi.py entry point...")
        
        wsgi_content = '''"""
WSGI Entry Point for Vercel Deployment

This module provides the WSGI application callable that Vercel uses
to deploy Flask applications. It's required for Vercel to recognize
the Flask app as the entrypoint.
"""

from app import app as flask_app


def application(environ, start_response):
    """
    WSGI Application Callable
    
    This is the entry point that Vercel uses to run the Flask application.
    
    Args:
        environ: WSGI environment dictionary
        start_response: Callable that takes status code and headers
        
    Returns:
        Iterable of response bodies
    """
    return flask_app.wsgi_app(environ, start_response)
'''
        
        wsgi_path.write_text(wsgi_content)
        print("✅ Created wsgi.py")
    else:
        print("✅ wsgi.py already exists")


def main():
    """Main build function."""
    print("=" * 60)
    print("🚀 Racing Demo - Vercel Build")
    print("=" * 60)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Build failed: Dependencies installation error")
        return False
    
    # Verify Flask
    if not verify_flask():
        print("\n❌ Build failed: Flask verification error")
        return False
    
    # Create WSGI entry point
    create_wsgi_entry()
    
    print("\n" + "=" * 60)
    print("✅ Vercel build completed successfully!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)