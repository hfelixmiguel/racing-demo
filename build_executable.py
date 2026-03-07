#!/usr/bin/env python3
"""
PyInstaller Build Script for Racing Game Demo

This script builds a standalone executable using PyInstaller.
Output: dist/racing_demo/racing_demo.exe (Windows) or racing_demo (Linux/Mac)
"""

import os
import sys
from pathlib import Path


def build_executable():
    """Build the racing game executable."""
    
    # Get current directory
    cwd = Path(__file__).parent.absolute()
    
    # Define paths
    dist_dir = cwd / "dist" / "racing_demo"
    spec_file = cwd / "racing_demo.spec"
    
    print("=" * 60)
    print("Racing Game Demo - PyInstaller Build")
    print("=" * 60)
    print(f"Working directory: {cwd}")
    print(f"Output directory: {dist_dir}")
    print()
    
    # Check if pyinstaller is installed
    try:
        import pyinstaller.__main__ as pyi_main
        print("✓ PyInstaller found")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        os.system(f"pip install pyinstaller")
    
    # Clean previous builds
    print("\nCleaning previous builds...")
    if dist_dir.exists():
        import shutil
        shutil.rmtree(dist_dir)
        print(f"  Removed: {dist_dir}")
    
    # Create spec file for PyInstaller
    print("\nCreating PyInstaller spec file...")
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['{cwd / "main.py"}'],
    pathex=[],
    binaries=[],
    datas=[
        ('{cwd / "tracks"}', 'tracks'),
    ],
    hiddenimports=[
        'arcade',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='racing_demo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open(spec_file, 'w') as f:
        f.write(spec_content)
    print(f"  Created: {spec_file}")
    
    # Run PyInstaller
    print("\nRunning PyInstaller...")
    print("-" * 60)
    
    try:
        import pyinstaller.__main__ as pyi_main
        
        # Build with specified options
        result = pyi_main.run(
            '--name=racing_demo',
            '--onefile',
            '--windowed',
            '--noconsole',
            f'--distpath={dist_dir}',
            f'--workpath={cwd / ".pyinstaller_cache"}',
            f'--specpath={cwd}',
            f'--specfile={spec_file}',
            str(cwd / "main.py"),
        )
        
        if result == 0:
            print("-" * 60)
            print("✓ Build successful!")
            
            # Find the executable
            exe_path = dist_dir / "racing_demo.exe" if os.name == 'nt' else dist_dir / "racing_demo"
            
            if exe_path.exists():
                print(f"\nExecutable created: {exe_path}")
                print(f"Size: {exe_path.stat().st_size / (1024*1024):.2f} MB")
                
                # Test run (optional)
                test_run = input("\nTest run the executable? (y/n): ").lower()
                if test_run == 'y':
                    print(f"Running: {exe_path}")
                    os.startfile(exe_path) if os.name == 'nt' else os.system(f"{exe_path} &")
            else:
                print(f"\n⚠ Warning: Executable not found at expected location")
                print(f"  Looking for: {exe_path}")
                print(f"  Contents of dist/racing_demo/:")
                if dist_dir.exists():
                    for item in dist_dir.iterdir():
                        print(f"    - {item.name} ({item.stat().st_size / 1024:.1f} KB)")
        else:
            print("-" * 60)
            print("✗ Build failed with exit code:", result)
            
    except Exception as e:
        print("-" * 60)
        print(f"✗ Build error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Build complete!")
    print("=" * 60)


if __name__ == "__main__":
    build_executable()
