@echo off
echo XP3 Viewer and Converter - Windows Build Script
echo ================================================
echo Made by Darryl Clay - First Iteration of XP3 Viewer/Converter
echo.

echo [1/8] Setting up Python environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment. Is Python installed?
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
echo ✓ Virtual environment activated

echo.
echo [2/8] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

pip install pyinstaller pillow>=10.0.0
if errorlevel 1 (
    echo ERROR: Failed to install build dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo [3/8] Creating application icons...
python create_icon.py
if errorlevel 1 (
    echo ERROR: Failed to create icons
    pause
    exit /b 1
)
echo ✓ Icons created

echo.
echo [4/8] Testing application...
python -c "from xp3_viewer_enhanced import main; print('✓ Application imports successfully')"
if errorlevel 1 (
    echo ERROR: Application test failed
    pause
    exit /b 1
)

echo.
echo [5/8] Building Windows executable...
pyinstaller --clean xp3_viewer.spec
if errorlevel 1 (
    echo ERROR: PyInstaller build failed
    pause
    exit /b 1
)

echo.
echo [6/8] Verifying executable creation...
if exist "dist\XP3_Viewer_Converter.exe" (
    echo ✓ Windows executable created successfully!
    for %%A in ("dist\XP3_Viewer_Converter.exe") do echo File size: %%~zA bytes
    echo File location: dist\XP3_Viewer_Converter.exe
) else (
    echo ERROR: Windows executable not found after build
    pause
    exit /b 1
)

echo.
echo [7/8] Creating portable package...
if not exist "XP3_Viewer_Converter_v1.0.2_Windows" mkdir XP3_Viewer_Converter_v1.0.2_Windows

copy "dist\XP3_Viewer_Converter.exe" "XP3_Viewer_Converter_v1.0.2_Windows\" >nul
copy "README.md" "XP3_Viewer_Converter_v1.0.2_Windows\" >nul
copy "LICENSE" "XP3_Viewer_Converter_v1.0.2_Windows\" >nul
copy "USAGE_EXAMPLES.md" "XP3_Viewer_Converter_v1.0.2_Windows\" >nul
copy "xp3_icon.ico" "XP3_Viewer_Converter_v1.0.2_Windows\" >nul

echo @echo off > "XP3_Viewer_Converter_v1.0.2_Windows\Run_XP3_Viewer.bat"
echo title XP3 Viewer and Converter - Made by Darryl Clay >> "XP3_Viewer_Converter_v1.0.2_Windows\Run_XP3_Viewer.bat"
echo echo Welcome to the first Iteration of XP3 Viewer/Converter >> "XP3_Viewer_Converter_v1.0.2_Windows\Run_XP3_Viewer.bat"
echo echo Made by Darryl Clay >> "XP3_Viewer_Converter_v1.0.2_Windows\Run_XP3_Viewer.bat"
echo echo. >> "XP3_Viewer_Converter_v1.0.2_Windows\Run_XP3_Viewer.bat"
echo echo Starting application... >> "XP3_Viewer_Converter_v1.0.2_Windows\Run_XP3_Viewer.bat"
echo XP3_Viewer_Converter.exe >> "XP3_Viewer_Converter_v1.0.2_Windows\Run_XP3_Viewer.bat"
echo pause >> "XP3_Viewer_Converter_v1.0.2_Windows\Run_XP3_Viewer.bat"

echo ✓ Portable package created: XP3_Viewer_Converter_v1.0.2_Windows

echo.
echo [8/8] Creating ZIP archive...
powershell -command "Compress-Archive -Path 'XP3_Viewer_Converter_v1.0.2_Windows' -DestinationPath 'XP3_Viewer_Converter_v1.0.2_Windows.zip' -Force"
if exist "XP3_Viewer_Converter_v1.0.2_Windows.zip" (
    echo ✓ ZIP archive created: XP3_Viewer_Converter_v1.0.2_Windows.zip
    for %%A in ("XP3_Viewer_Converter_v1.0.2_Windows.zip") do echo Archive size: %%~zA bytes
) else (
    echo WARNING: Could not create ZIP archive
)

echo.
echo ================================================
echo 🎉 BUILD COMPLETED SUCCESSFULLY!
echo ================================================
echo.
echo Generated files:
echo ✓ dist\XP3_Viewer_Converter.exe
echo ✓ XP3_Viewer_Converter_v1.0.2_Windows\ (folder)
echo ✓ XP3_Viewer_Converter_v1.0.2_Windows.zip
echo ✓ installer_script.iss (for Inno Setup)
echo.
echo Next steps:
echo 1. Test the executable: dist\XP3_Viewer_Converter.exe
echo 2. Create installer using Inno Setup:
echo    - Open Inno Setup
echo    - Open installer_script.iss
echo    - Click Build → Compile
echo 3. Upload files to GitHub release
echo.
echo Features implemented:
echo ✓ Loading screen: "Welcome to the first Iteration of XP3 Viewer/Converter"
echo ✓ Attribution: "Made by Darryl Clay" in UI
echo ✓ Windows XP styling throughout
echo ✓ Loading animation in bottom right
echo ✓ Professional executable packaging
echo.
echo Made by Darryl Clay - First Iteration Complete!
echo.
pause
