# Windows Deployment Guide for XP3 Viewer and Converter v1.0.2

## Prerequisites for Windows Deployment

### Required Software:
1. **Python 3.7+** - Download from https://python.org/downloads/
2. **Git for Windows** - Download from https://git-scm.com/download/win
3. **Inno Setup** - Download from https://jrsoftware.org/isinfo.php

## Step-by-Step Windows Deployment

### Step 1: Clone Repository on Windows
```cmd
git clone https://github.com/DarrylClay2005/XP3-Viewer-and-Converter.git
cd XP3-Viewer-and-Converter
```

### Step 2: Setup Python Environment
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller pillow>=10.0.0
```

### Step 3: Test Application
```cmd
python xp3_viewer_enhanced.py
```

### Step 4: Build Windows Executable
```cmd
pyinstaller --clean xp3_viewer.spec
```

### Step 5: Verify Executable
```cmd
dir dist\
dist\XP3_Viewer_Converter.exe
```

### Step 6: Create Windows Installer
1. Open Inno Setup
2. Open `installer_script.iss`
3. Click **Build** → **Compile**
4. Installer will be created in `installer\` directory

### Step 7: Test Installation
1. Run the created installer
2. Test the installed application
3. Verify all features work correctly

## Automated Windows Build Script

Save as `build_windows.bat` and run on Windows:

```batch
@echo off
echo XP3 Viewer and Converter - Windows Build Script
echo ================================================

echo Setting up Python environment...
python -m venv venv
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller pillow>=10.0.0

echo Creating icons...
python create_icon.py

echo Building Windows executable...
pyinstaller --clean xp3_viewer.spec

echo Checking if executable was created...
if exist "dist\XP3_Viewer_Converter.exe" (
    echo ✓ Windows executable created successfully!
    echo File location: dist\XP3_Viewer_Converter.exe
    
    echo Creating portable package...
    if not exist "XP3_Viewer_Converter_v1.0.2_Windows" mkdir XP3_Viewer_Converter_v1.0.2_Windows
    copy "dist\XP3_Viewer_Converter.exe" "XP3_Viewer_Converter_v1.0.2_Windows\"
    copy "README.md" "XP3_Viewer_Converter_v1.0.2_Windows\"
    copy "LICENSE" "XP3_Viewer_Converter_v1.0.2_Windows\"
    copy "USAGE_EXAMPLES.md" "XP3_Viewer_Converter_v1.0.2_Windows\"
    copy "xp3_icon.ico" "XP3_Viewer_Converter_v1.0.2_Windows\"
    
    echo @echo off > "XP3_Viewer_Converter_v1.0.2_Windows\Run_XP3_Viewer.bat"
    echo title XP3 Viewer and Converter >> "XP3_Viewer_Converter_v1.0.2_Windows\Run_XP3_Viewer.bat"
    echo echo Starting XP3 Viewer and Converter... >> "XP3_Viewer_Converter_v1.0.2_Windows\Run_XP3_Viewer.bat"
    echo XP3_Viewer_Converter.exe >> "XP3_Viewer_Converter_v1.0.2_Windows\Run_XP3_Viewer.bat"
    echo pause >> "XP3_Viewer_Converter_v1.0.2_Windows\Run_XP3_Viewer.bat"
    
    echo ✓ Portable package created: XP3_Viewer_Converter_v1.0.2_Windows
    echo.
    echo Next steps:
    echo 1. Test the executable: dist\XP3_Viewer_Converter.exe
    echo 2. Create installer using Inno Setup with installer_script.iss
    echo 3. Upload to GitHub releases
    
) else (
    echo ✗ Failed to create Windows executable
    echo Check the build output above for errors
)

pause
```

## Expected Output Structure

After successful Windows build:
```
dist/
└── XP3_Viewer_Converter.exe    (Windows executable)

XP3_Viewer_Converter_v1.0.2_Windows/
├── XP3_Viewer_Converter.exe
├── README.md
├── LICENSE
├── USAGE_EXAMPLES.md
├── xp3_icon.ico
└── Run_XP3_Viewer.bat

installer/
└── XP3_Viewer_Converter_v1.0.2_Setup.exe
```

## Troubleshooting

### Common Issues:

1. **Python not found**: Install Python and add to PATH
2. **PyInstaller fails**: Ensure all dependencies are installed
3. **Missing DLL**: Install Visual C++ Redistributable
4. **Antivirus blocking**: Add exception for PyInstaller output

### Solutions:

```cmd
# If Python not in PATH
set PATH=%PATH%;C:\Python39;C:\Python39\Scripts

# If missing Visual C++
# Download and install: https://aka.ms/vs/17/release/vc_redist.x64.exe

# If PyInstaller issues
pip install --upgrade pyinstaller
```

## Final Deployment Checklist

- [ ] Python environment setup
- [ ] Dependencies installed
- [ ] Icons created
- [ ] Windows executable built
- [ ] Executable tested
- [ ] Installer created with Inno Setup
- [ ] Installer tested
- [ ] Files uploaded to GitHub release
- [ ] Release notes published

## GitHub Release Upload

1. Go to: https://github.com/DarrylClay2005/XP3-Viewer-and-Converter/releases
2. Click "Create a new release"
3. Tag: `v1.0.2`
4. Title: `XP3 Viewer and Converter v1.0.2 - First Iteration`
5. Upload files:
   - `XP3_Viewer_Converter.exe`
   - `XP3_Viewer_Converter_v1.0.2_Setup.exe`
   - `XP3_Viewer_Converter_v1.0.2_Windows.zip`

## Success Criteria

✅ Windows executable runs without dependencies
✅ Loading screen shows "Welcome to the first Iteration of XP3 Viewer/Converter"
✅ Attribution "Made by Darryl Clay" visible in UI
✅ Windows XP styling applied throughout
✅ All original XP3 functionality works
✅ Professional installer created
✅ GitHub release published

---

**Made by Darryl Clay - First Iteration of XP3 Viewer/Converter**
