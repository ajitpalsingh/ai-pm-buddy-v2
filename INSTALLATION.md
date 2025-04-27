# AI PM Buddy v1.0 - Installation Guide

This guide will walk you through setting up and running the AI PM Buddy application on your local machine.

## Prerequisites

1. **Python 3.8+**: Make sure you have Python 3.8 or newer installed. You can download it from [python.org](https://www.python.org/downloads/).

2. **Graphviz**: The application requires Graphviz for some visualizations.
   - **Windows**: Download from [Graphviz website](https://graphviz.org/download/) and add the bin directory to your PATH
   - **macOS**: `brew install graphviz`
   - **Linux**: `sudo apt-get install graphviz graphviz-dev pkg-config`

3. **OpenAI API Key**: You'll need an API key from OpenAI for the AI features to work. You can obtain one from [OpenAI's platform](https://platform.openai.com/account/api-keys).

## Installation Steps

### Step 1: Extract the ZIP file

Extract the `ai_pm_buddy_v1.0.zip` file to a directory of your choice.

### Step 2: Create a Virtual Environment (Recommended)

Open a terminal or command prompt in the extracted directory and run:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Packages

Install all the required Python packages:

```bash
pip install -r package-requirements.txt
```

This will install:
- streamlit
- openai
- pandas
- numpy
- matplotlib
- plotly
- networkx
- wordcloud
- pygraphviz
- python-dotenv

### Step 4: Set Up Your OpenAI API Key

Create a `.env` file in the main directory by copying the `.env.example` file:

```bash
# On Windows
copy .env.example .env

# On macOS/Linux
cp .env.example .env
```

Edit the `.env` file and replace `your_api_key_here` with your actual OpenAI API key.

### Step 5: Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at http://localhost:8501 in your web browser.

## Usage Tips

1. When you first run the application, a sample project will be created automatically.
2. Use the sidebar to navigate between different project management modules.
3. Your API key can also be updated through the application's sidebar (under "API Key Settings").
4. The application will save your project data in session state. For a production environment, you would want to connect to a database.

## Troubleshooting

1. **ImportError for pygraphviz**: Make sure Graphviz is properly installed and added to your PATH. On Windows, you may need to restart your computer after installation.

2. **OpenAI API Key issues**: If you see errors related to the OpenAI API, verify that your API key is correct and has sufficient credits/permissions.

3. **Port in use**: If port 8501 is already in use, Streamlit will automatically try to use the next available port. Check your terminal output for the correct URL.

4. **Package installation issues**: Try installing packages one by one if you encounter any issues with the bulk installation.

## Additional Configuration

The application's appearance and server settings can be customized in the `.streamlit/config.toml` file. The current configuration sets:

- Server port: 8501
- Primary color: Green (#4CAF50)
- Light background theme

You can modify these settings to match your preferences.