#!/bin/bash

# Check if zeroEtl.zip exists, if yes, delete it
if [ -f zeroEtl.zip ]; then
    echo "The file zeroEtl.zip already exists. Deleting..."
    rm zeroEtl.zip
    echo "Deleted zeroEtl.zip"
fi

# Check if pip3 is installed
if command -v pip &> /dev/null; then
    pipCommand="pip"
# Check if pip is installed only if pip3 is not found
elif command -v pip3 &> /dev/null; then
    pipCommand="pip3"
else
    echo "Neither pip nor pip3 is installed. Please install either of them to proceed."
    exit 1
fi

# Check if pipenv is installed, if not, install it
if ! command -v pipenv &> /dev/null; then
    echo "pipenv is not installed. Installing it now..."
    $pipCommand install pipenv
fi

# Install dependencies from Pipfile.lock using pipenv if available, else use pip in the current directory
if command -v pipenv &> /dev/null; then
    echo "Installing dependencies from Pipfile.lock using pipenv..."
    pipenv install
    pipenv run $pipCommand install -r <(pipenv requirements) --target ./
else
    echo "pipenv failed to install. Please make sure it is installed and properly configured."
    exit 1
fi

# Check if zip is installed
if ! command -v zip &> /dev/null; then
    echo "zip is not installed. Please install zip to proceed with zipping files."
    exit 1
fi

# Zip all files in the present working directory with the name "zeroEtl.py"
zip -r zeroEtl.zip ./*

echo "Files zipped successfully."
