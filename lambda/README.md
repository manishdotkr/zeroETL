
---

### ZeroEtl Setup Script

This script automates the setup process for the ZeroEtl project by downloading dependencies and packaging them into a zip file.

### Prerequisites
- **Python:** Ensure Python is installed on your system.
- **pip or pip3:** Make sure either pip or pip3 is installed. The script checks for their presence.
- **pipenv:** If not already installed, the script will install pipenv to manage dependencies.
- **zip:** Ensure zip is installed on your system for packaging the files.

### Instructions

1. **Download Script:**
    - Clone or download the repository.

2. **Run the Script:**
    - Open a terminal and navigate to the directory containing the setup.sh script.
    - Run the script by executing the following command:
        ```
        ./setup.sh
        ```

3. **Follow Prompts:**
    - The script will first check if zeroEtl.zip already exists in the directory. If so, it will be deleted.
    - It then checks for the presence of pip or pip3. If neither is found, it prompts to install either of them.
    - If pipenv is not installed, it will be installed automatically.
    - Dependencies will be installed from Pipfile.lock using pipenv.
    - If pipenv fails to install or execute, the script will terminate.
    - Finally, all files in the directory will be zipped into zeroEtl.zip.

4. **Completion:**
    - Upon successful execution, the script will display "Files zipped successfully."

### Notes
- **Pipfile.lock:** Ensure Pipfile.lock is present in the project directory to correctly install dependencies.
- **Customization:** Modify the script according to your project's specific requirements, such as changing the name of the zip file or adding additional steps.

### Troubleshooting
- If you encounter any issues during the setup process, ensure that all prerequisites are met and check for any error messages displayed during script execution.

### Contact
For any further assistance or inquiries, feel free to contact the project maintainer at [officialmanishkr98@gmail.com](mailto:officialmanishkr98@gmail.com).