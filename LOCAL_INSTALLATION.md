# AI PM Buddy v2.0 - Local Installation Guide for Windows 11

This guide provides instructions for installing and running AI PM Buddy v2.0 on a Windows 11 machine.

## System Requirements

- Windows 11
- Python 3.11 or higher
- OpenAI API Key
- Graphviz (optional, for network diagrams)

## Quick Installation

1. Copy all files to `C:\Users\A726951\python_trial\pm_buddy2`
2. Double-click `install.bat` to set up the virtual environment and install dependencies
3. Edit the `.env` file and add your OpenAI API key
4. Double-click `run.bat` to start the application
5. Open your browser and navigate to `http://localhost:8502/`

## Manual Installation

If you prefer to install manually or if the batch script doesn't work, follow these steps:

1. Open Windows Terminal or Command Prompt
2. Navigate to the installation directory:
   ```
   cd C:\Users\A726951\python_trial\pm_buddy2
   ```
3. Create a virtual environment:
   ```
   python -m venv venv
   ```
4. Activate the virtual environment:
   ```
   venv\Scripts\activate
   ```
5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
6. Edit the `.env` file and add your OpenAI API key
7. Run the application:
   ```
   streamlit run app_v2.py --server.port 8502
   ```
8. Open your browser and navigate to `http://localhost:8502/`

## Troubleshooting

### Python Not Found

Ensure Python 3.11+ is installed and added to your PATH environment variable.

### Package Installation Errors

If you encounter issues installing `pygraphviz`, you can:

1. Install Visual Studio Build Tools and Graphviz, then try:
   ```
   pip install --global-option=build_ext --global-option="-IC:\Program Files\Graphviz\include" --global-option="-LC:\Program Files\Graphviz\lib" pygraphviz
   ```

2. Or download a pre-built wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygraphviz and install it:
   ```
   pip install [path_to_downloaded_wheel]
   ```

### Port Already in Use

If port 8502 is already in use:

1. Find the process using the port:
   ```
   netstat -ano | findstr :8502
   ```
2. Kill the process (replace PID with the process ID from the previous command):
   ```
   taskkill /F /PID PID
   ```

3. Or change the port number in the `run.bat` file and in `.streamlit/config.toml`

## Files and Directory Structure

- `app_v2.py`: Main application file
- `modules/`: Application modules
- `utils/`: Utility functions
- `data/`: Data files
- `.env`: Environment variables configuration
- `.streamlit/`: Streamlit configuration

## Support and Additional Information

For more information about AI PM Buddy v2.0, refer to the `README.md` file.

For detailed installation troubleshooting, see the `INSTALLATION.md` file.