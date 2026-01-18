# 🚀 Getting Started with the Diabetes Prediction & Health Advice App

This Streamlit app lets you predict diabetes risk based on health parameters and get personalized health recommendations using AI. Follow these steps carefully to get the application running on your computer.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://diabetespredictionsystem-soyinkaenoch.streamlit.app/)


## Prerequisites

Before you begin, make sure you have:

- Python 3.9 or newer installed → Check with: `python --version` or `python3 --version`
- Git (optional – if you cloned the repository)
- A code editor (VS Code, PyCharm, etc. recommended)
- An internet connection (needed for installing packages)

## Step-by-Step Installation Guide

### 1. Clone or Download the Project

If you haven't already:

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo-name
```

Or simply download and extract the ZIP file.

### 2. Create and Activate a Virtual Environment

(Very important – prevents conflicts with other Python projects)

**Create virtual environment:**

```bash
python -m venv env
```

Or on some systems:

```bash
python3 -m venv env
```

**Then activate it:**

**Windows:**

```bash
env\Scripts\activate
```

**macOS / Linux / Unix:**

```bash
source env/bin/activate
```

After activation you should see `(env)` at the beginning of your terminal prompt.

### 3. Install All Required Packages

```bash
pip install --upgrade pip                    # Recommended: update pip first
pip install -r requirements.txt
```

This installs Streamlit, pandas, scikit-learn, and the AI libraries needed by the app.

**Tip:** If installation is very slow or fails, try:

```bash
pip install -r requirements.txt --timeout=100
```

### 4. Set Up Your API Key (Very Important!)

The app needs an API key to communicate with the AI model (Gemini).

1. Find the file called `.env.example` in the project folder
2. Make a copy and rename it to `.env` (just `.env` – no extension)
3. Open `.env` in a text editor
4. Add your Google API key like this:

```env
# .env file
GOOGLE_API_KEY=your-google-api-key-here
```

#### How to Get a Google API Key?

1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API key"
4. Copy the key and paste it carefully (no extra spaces!)

### 5. Run the Application

Make sure you're still in the activated virtual environment, then:

```bash
streamlit gpt_app.py
```
or 

```bash
streamlit run gemini_app.py
# streamlit run app.py
```

After a few seconds, your default web browser should automatically open with the app running at:

```
http://localhost:8501
```

---
