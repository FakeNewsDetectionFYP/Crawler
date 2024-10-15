#!/bin/bash

# Check if Homebrew is installed
if ! command -v brew &>/dev/null
then
    echo "Homebrew not found, installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew is already installed."
fi

# Install Tesseract OCR
if ! command -v tesseract &>/dev/null
then
    echo "Installing Tesseract OCR..."
    brew install tesseract
else
    echo "Tesseract is already installed."
fi

# Install ChromeDriver (for Selenium)
if ! command -v chromedriver &>/dev/null
then
    echo "Installing ChromeDriver..."
    brew install chromedriver
else
    echo "ChromeDriver is already installed."
fi

# Install Python packages
echo "Installing Python packages from requirements.txt..."
pip install -r requirements.txt