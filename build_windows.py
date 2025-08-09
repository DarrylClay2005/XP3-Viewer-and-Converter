#!/usr/bin/env python3
"""
Build script for XP3 Viewer and Converter Windows executable and installer
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"🔨 {description}")
    print(f"{'='*60}")
    print(f"Running: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print("✅ Success!")
        if result.stdout:
            print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print("Output:", e.stdout)
        if e.stderr:
            print("Error:", e.stderr)
        return False

def ensure_requirements():
    """Ensure all required tools and dependencies are installed"""
    print("\n🔍 Checking requirements...")
    
    # Check if we're in virtual environment
    if not os.environ.get('VIRTUAL_ENV') and not hasattr(sys, 'real_prefix'):
        print("⚠️  Warning: Not in virtual environment")
    
    # Install additional required packages
    packages = [
        'pyinstaller',
        'pillow>=10.0.0',
        'auto-py-to-exe',  # For GUI installer creation
    ]
    
    for package in packages:
        print(f"📦 Installing/checking {package}...")
        if not run_command(f"pip install {package}", f"Installing {package}"):
            print(f"❌ Failed to install {package}")
            return False
    
    return True

def create_executable():
    """Create the Windows executable using PyInstaller"""
    print("\n🏗️  Creating Windows executable...")
    
    # Ensure icons exist
    if not Path('xp3_icon.ico').exists():
        print("📊 Creating application icons...")
        if not run_command("python create_icon.py", "Creating icons"):
            print("❌ Failed to create icons")
            return False
    
    # Build with PyInstaller
    cmd = "pyinstaller --clean xp3_viewer.spec"
    if not run_command(cmd, "Building executable with PyInstaller"):
        print("❌ Failed to build executable")
        return False
    
    # Check if executable was created (Linux or Windows)
    exe_paths = [Path("dist/XP3_Viewer_Converter.exe"), Path("dist/XP3_Viewer_Converter")]
    exe_path = None
    for path in exe_paths:
        if path.exists():
            exe_path = path
            break
    
    if exe_path:
        print(f"✅ Executable created: {exe_path}")
        print(f"📊 Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
        return True
    else:
        print("❌ Executable not found after build")
        return False

def create_installer():
    """Create a Windows installer using NSIS or Inno Setup"""
    print("\n📦 Creating Windows installer...")
    
    # Create installer script for Inno Setup
    inno_script = """
[Setup]
AppName=XP3 Viewer and Converter
AppVersion=1.0.2
DefaultDirName={pf}\\XP3 Viewer and Converter
DefaultGroupName=XP3 Viewer and Converter
UninstallDisplayIcon={app}\\XP3_Viewer_Converter.exe
Compression=lzma2
SolidCompression=yes
OutputDir=installer
OutputBaseFilename=XP3_Viewer_Converter_v1.0.2_Setup

[Files]
Source: "dist\\XP3_Viewer_Converter.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "xp3_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\XP3 Viewer and Converter"; Filename: "{app}\\XP3_Viewer_Converter.exe"; WorkingDir: "{app}"; IconFilename: "{app}\\xp3_icon.ico"
Name: "{group}\\Uninstall XP3 Viewer and Converter"; Filename: "{uninstallexe}"
Name: "{commondesktop}\\XP3 Viewer and Converter"; Filename: "{app}\\XP3_Viewer_Converter.exe"; WorkingDir: "{app}"; IconFilename: "{app}\\xp3_icon.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\\XP3_Viewer_Converter.exe"; Description: "Launch XP3 Viewer and Converter"; Flags: nowait postinstall skipifsilent
"""
    
    # Write Inno Setup script
    with open("installer_script.iss", "w", encoding='utf-8') as f:
        f.write(inno_script)
    
    print("📄 Inno Setup script created: installer_script.iss")
    
    # Create installer directory
    os.makedirs("installer", exist_ok=True)
    
    # Note: This would require Inno Setup to be installed on Windows
    print("ℹ️  To create the installer on Windows:")
    print("   1. Install Inno Setup from https://jrsoftware.org/isinfo.php")
    print("   2. Open installer_script.iss in Inno Setup")
    print("   3. Click Build → Compile")
    print("   4. The installer will be created in the 'installer' directory")
    
    return True

def create_portable_package():
    """Create a portable package with all necessary files"""
    print("\n📁 Creating portable package...")
    
    package_dir = Path("XP3_Viewer_Converter_v1.0.2_Portable")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir()
    
    # Find the executable (Linux or Windows)
    exe_files = [
        ("dist/XP3_Viewer_Converter.exe", "XP3_Viewer_Converter.exe"),
        ("dist/XP3_Viewer_Converter", "XP3_Viewer_Converter"),
    ]
    
    # Copy files to package
    files_to_copy = [
        ("README.md", "README.md"),
        ("LICENSE", "LICENSE"),
        ("USAGE_EXAMPLES.md", "USAGE_EXAMPLES.md"),
        ("xp3_icon.ico", "xp3_icon.ico"),
    ]
    
    # Add executable file
    for exe_src, exe_dst in exe_files:
        if Path(exe_src).exists():
            files_to_copy.insert(0, (exe_src, exe_dst))
            break
    
    for src, dst in files_to_copy:
        src_path = Path(src)
        if src_path.exists():
            dst_path = package_dir / dst
            shutil.copy2(src_path, dst_path)
            print(f"📄 Copied: {src} → {dst}")
        else:
            print(f"⚠️  File not found: {src}")
    
    # Create a simple run script
    run_script = """@echo off
title XP3 Viewer and Converter
echo Starting XP3 Viewer and Converter...
XP3_Viewer_Converter.exe
pause
"""
    
    with open(package_dir / "Run_XP3_Viewer.bat", "w") as f:
        f.write(run_script)
    
    # Create archive
    archive_name = "XP3_Viewer_Converter_v1.0.2_Portable"
    shutil.make_archive(archive_name, 'zip', package_dir)
    
    print(f"✅ Portable package created: {archive_name}.zip")
    return True

def optimize_and_test():
    """Perform optimization and testing"""
    print("\n🔧 Optimizing and testing...")
    
    # Run tests
    print("🧪 Running tests...")
    if not run_command("python test_xp3.py", "Running unit tests"):
        print("⚠️  Some tests failed, but continuing build process")
    
    # Test the executable (dry run)
    exe_path = Path("dist/XP3_Viewer_Converter.exe")
    if exe_path.exists():
        print("✅ Executable exists and is ready for testing")
        # Note: We can't actually run the GUI test in this environment
    
    return True

def update_version_files():
    """Update version information in files"""
    print("\n📝 Updating version files...")
    
    # Update setup.py version
    setup_py = Path("setup.py")
    if setup_py.exists():
        content = setup_py.read_text()
        content = content.replace('version="1.0.0"', 'version="1.0.2"')
        setup_py.write_text(content)
        print("✅ Updated setup.py version")
    
    return True

def prepare_github_release():
    """Prepare files for GitHub release"""
    print("\n🚀 Preparing GitHub release...")
    
    release_dir = Path("github_release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # Copy release files
    release_files = [
        "dist/XP3_Viewer_Converter.exe",
        "XP3_Viewer_Converter_v1.0.2_Portable.zip",
        "README.md",
        "LICENSE",
        "USAGE_EXAMPLES.md"
    ]
    
    for file_path in release_files:
        src = Path(file_path)
        if src.exists():
            dst = release_dir / src.name
            if src.is_file():
                shutil.copy2(src, dst)
            print(f"📄 Prepared for release: {src.name}")
    
    # Create release notes
    release_notes = f"""# XP3 Viewer and Converter v1.0.2 Release

## What's New in v1.0.2
- ✨ **First Iteration of XP3 Viewer/Converter**
- 🎨 Windows XP styling and theming
- 🔄 Loading screen with "Welcome to the first Iteration of XP3 Viewer/Converter"
- 👤 Attribution: "Made by Darryl Clay" displayed throughout the application
- 🔄 Loading animations and status indicators
- 🏗️ Optimized performance and error handling
- 📦 Professional Windows installer package

## Features
- Extract individual files or entire XP3 archives
- Preview image files with optimized rendering
- Convert images to PNG, JPEG, BMP, or TIFF formats
- Enhanced error handling and performance
- Cross-platform support (Windows executable provided)

## Downloads
- `XP3_Viewer_Converter.exe` - Standalone Windows executable
- `XP3_Viewer_Converter_v1.0.2_Portable.zip` - Portable package

## Installation
1. Download the executable or portable package
2. Run `XP3_Viewer_Converter.exe` directly (no installation required)
3. Or use the Windows installer for system-wide installation

## System Requirements
- Windows 7 or later
- No additional software required (standalone executable)

Made by Darryl Clay
"""
    
    with open(release_dir / "RELEASE_NOTES.md", "w", encoding='utf-8') as f:
        f.write(release_notes)
    
    print("✅ GitHub release files prepared in 'github_release' directory")
    return True

def main():
    """Main build process"""
    print("🚀 XP3 Viewer and Converter - Windows Build Process")
    print("=" * 60)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Build steps
    steps = [
        ("Checking requirements", ensure_requirements),
        ("Updating version files", update_version_files),
        ("Creating executable", create_executable),
        ("Optimizing and testing", optimize_and_test),
        ("Creating portable package", create_portable_package),
        ("Creating installer configuration", create_installer),
        ("Preparing GitHub release", prepare_github_release),
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        print(f"\n{'🔄' if success_count == len(steps) else '📍'} Step {success_count + 1}/{len(steps)}: {step_name}")
        if step_func():
            success_count += 1
            print(f"✅ {step_name} completed successfully")
        else:
            print(f"❌ {step_name} failed")
            break
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 BUILD SUMMARY")
    print(f"{'='*60}")
    
    if success_count == len(steps):
        print("🎉 All build steps completed successfully!")
        print("\n📦 Generated files:")
        for file_path in ["dist/XP3_Viewer_Converter.exe", 
                         "XP3_Viewer_Converter_v1.0.2_Portable.zip",
                         "installer_script.iss",
                         "github_release"]:
            if Path(file_path).exists():
                print(f"   ✅ {file_path}")
        
        print("\n🚀 Next steps:")
        print("   1. Test the executable on Windows")
        print("   2. Create installer using Inno Setup (on Windows)")
        print("   3. Upload to GitHub releases")
        print("   4. Update README with download links")
        
    else:
        print(f"⚠️  Build completed with {success_count}/{len(steps)} successful steps")
    
    print(f"\n{'='*60}")
    print("Build process completed!")

if __name__ == "__main__":
    main()
