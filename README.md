# 🚀 Getting Started

To run this app, follow these steps:

1. **Set up your virtual environment:**

    ```bash
    python3 -m venv env
    ```

2. **Activate the environment:**

    - On Unix or MacOS:
      ```bash
      source env/bin/activate
      ```
    - On Windows:
      ```bash
      source env/Scripts/activate
      ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Prepare your environment variables:**

    - Rename `.env.example` to `.env`.
    - Add your OpenAI API key in the format:
      ```plaintext
      OPENAI_API_KEY=your_api_key_here
      ```

5. **Run the app:**

    ```bash
    streamlit run app.py
    ```

Happy coding! 🎉