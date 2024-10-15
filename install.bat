@echo off

:: Check if Chocolatey is installed (for Windows package management)
choco -v >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Chocolatey...
    @powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
) else (
    echo Chocolatey is already installed.
)

:: Install Tesseract OCR
choco install tesseract -y

:: Install ChromeDriver
choco install chromedriver -y

:: Install Python packages
echo Installing Python packages...
pip install -r requirements.txt