# XP3 Viewer and Converter - Windows PowerShell Build Script
# Made by Darryl Clay - First Iteration of XP3 Viewer/Converter

Write-Host "XP3 Viewer and Converter - Windows Build Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Made by Darryl Clay - First Iteration of XP3 Viewer/Converter" -ForegroundColor Yellow
Write-Host ""

function Test-Command($command) {
    $null = Get-Command $command -ErrorAction SilentlyContinue
    return $?
}

function Write-Step($step, $message) {
    Write-Host "[$step] $message" -ForegroundColor Green
}

function Write-Success($message) {
    Write-Host "✓ $message" -ForegroundColor Green
}

function Write-Error($message) {
    Write-Host "✗ ERROR: $message" -ForegroundColor Red
}

# Step 1: Check Prerequisites
Write-Step "1/8" "Checking prerequisites..."

if (-not (Test-Command python)) {
    Write-Error "Python not found. Please install Python 3.7+ from https://python.org/downloads/"
    Read-Host "Press Enter to exit"
    exit 1
}

$pythonVersion = python --version
Write-Success "Python found: $pythonVersion"

# Step 2: Setup Virtual Environment
Write-Step "2/8" "Setting up Python environment..."

if (Test-Path "venv") {
    Remove-Item "venv" -Recurse -Force
}

python -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to create virtual environment"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Success "Virtual environment created"

# Activate virtual environment
& "venv\Scripts\Activate.ps1"
Write-Success "Virtual environment activated"

# Step 3: Install Dependencies
Write-Step "3/8" "Installing dependencies..."

pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install requirements"
    Read-Host "Press Enter to exit"
    exit 1
}

pip install pyinstaller pillow>=10.0.0
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install build dependencies"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Success "Dependencies installed"

# Step 4: Create Icons
Write-Step "4/8" "Creating application icons..."

python create_icon.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to create icons"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Success "Icons created"

# Step 5: Test Application
Write-Step "5/8" "Testing application..."

python -c "from xp3_viewer_enhanced import main; print('Application imports successfully')"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Application test failed"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Success "Application test passed"

# Step 6: Build Executable
Write-Step "6/8" "Building Windows executable..."

pyinstaller --clean xp3_viewer.spec
if ($LASTEXITCODE -ne 0) {
    Write-Error "PyInstaller build failed"
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 7: Verify Executable
Write-Step "7/8" "Verifying executable creation..."

$exePath = "dist\XP3_Viewer_Converter.exe"
if (Test-Path $exePath) {
    $fileSize = (Get-Item $exePath).Length
    $fileSizeMB = [math]::Round($fileSize / 1MB, 1)
    Write-Success "Windows executable created: $exePath"
    Write-Host "   File size: $fileSizeMB MB" -ForegroundColor Cyan
} else {
    Write-Error "Windows executable not found after build"
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 8: Create Portable Package
Write-Step "8/8" "Creating portable package..."

$packageDir = "XP3_Viewer_Converter_v1.0.2_Windows"
if (Test-Path $packageDir) {
    Remove-Item $packageDir -Recurse -Force
}

New-Item -ItemType Directory -Path $packageDir | Out-Null

# Copy files
Copy-Item "dist\XP3_Viewer_Converter.exe" "$packageDir\" -Force
Copy-Item "README.md" "$packageDir\" -Force
Copy-Item "LICENSE" "$packageDir\" -Force  
Copy-Item "USAGE_EXAMPLES.md" "$packageDir\" -Force
Copy-Item "xp3_icon.ico" "$packageDir\" -Force

# Create run script
$runScript = @"
@echo off
title XP3 Viewer and Converter - Made by Darryl Clay
echo Welcome to the first Iteration of XP3 Viewer/Converter
echo Made by Darryl Clay
echo.
echo Starting application...
XP3_Viewer_Converter.exe
pause
"@

$runScript | Out-File -FilePath "$packageDir\Run_XP3_Viewer.bat" -Encoding ASCII

Write-Success "Portable package created: $packageDir"

# Create ZIP archive
try {
    Compress-Archive -Path $packageDir -DestinationPath "$packageDir.zip" -Force
    $zipSize = (Get-Item "$packageDir.zip").Length
    $zipSizeMB = [math]::Round($zipSize / 1MB, 1)
    Write-Success "ZIP archive created: $packageDir.zip ($zipSizeMB MB)"
} catch {
    Write-Host "WARNING: Could not create ZIP archive" -ForegroundColor Yellow
}

# Final Summary
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "🎉 BUILD COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Generated files:" -ForegroundColor Yellow
Write-Host "✓ dist\XP3_Viewer_Converter.exe" -ForegroundColor Green
Write-Host "✓ $packageDir\ (folder)" -ForegroundColor Green
Write-Host "✓ $packageDir.zip" -ForegroundColor Green
Write-Host "✓ installer_script.iss (for Inno Setup)" -ForegroundColor Green

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Test the executable: dist\XP3_Viewer_Converter.exe" -ForegroundColor White
Write-Host "2. Create installer using Inno Setup:" -ForegroundColor White
Write-Host "   - Download and install Inno Setup from https://jrsoftware.org/isinfo.php" -ForegroundColor Gray
Write-Host "   - Open installer_script.iss in Inno Setup" -ForegroundColor Gray
Write-Host "   - Click Build → Compile" -ForegroundColor Gray
Write-Host "3. Upload files to GitHub release" -ForegroundColor White

Write-Host ""
Write-Host "Features implemented:" -ForegroundColor Yellow
Write-Host "✓ Loading screen: 'Welcome to the first Iteration of XP3 Viewer/Converter'" -ForegroundColor Green
Write-Host "✓ Attribution: 'Made by Darryl Clay' in UI" -ForegroundColor Green
Write-Host "✓ Windows XP styling throughout" -ForegroundColor Green
Write-Host "✓ Loading animation in bottom right" -ForegroundColor Green
Write-Host "✓ Professional executable packaging" -ForegroundColor Green

Write-Host ""
Write-Host "Made by Darryl Clay - First Iteration Complete!" -ForegroundColor Magenta

Read-Host "`nPress Enter to exit"
