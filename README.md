# CodeExplain: Plain-English Code Tutor

CodeExplain is a beginner-friendly code explanation tool that helps students understand code snippets in plain English. It provides a line-by-line breakdown, complexity analysis, suggested improvements, and comprehension quizzes.

## Features

- **Multi-Model Support**: Use Gemini API, Ollama (local), or LM Studio (local) as the underlying LLM.
- **Structured Explanation**: Provides summary, plain English explanation, line-by-line breakdown, time/space complexity, improvements, and quizzes in clearly separated sections.
- **Language Support**: Supports explaining code in English or Hinglish (and potentially other languages).
- **No Complex Setup**: A simple Streamlit interface that just works.

## Installation

1. Clone the repository.
2. Install the requirements:
   ```bash
   python -m venv venv
   .\venv\Scripts\pip install -r requirements.txt
   ```
3. Set up your environment variables by editing the `.env` file (see example structure below):
   ```
   GEMINI_API_KEY=your_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   OLLAMA_MODEL=llama3
   LMSTUDIO_MODEL=gemma4-e4b
   LMSTUDIO_URL=http://localhost:1234/v1
   OLLAMA_URL=http://localhost:11434
   ```

## Usage

Run the Streamlit application:

```bash
.\venv\Scripts\streamlit run app.py
```

1. Open the application in your browser (usually http://localhost:8501).
2. Select your Model Provider from the sidebar.
3. Choose the target language for the explanation.
4. Select the code language of the snippet you're pasting.
5. Paste your code snippet and click **Explain Code**.

## How to Select Your Own Models

You can easily swap out the AI model powering your code explanations via the `.env` file configuration:

### 1. Google Gemini
By default, the app is configured to use `gemini-2.5-flash`. If you want to use a different Gemini model (like `gemini-2.5-pro`):
1. Open your `.env` file.
2. Edit the `GEMINI_MODEL` line:
   ```
   GEMINI_MODEL=gemini-2.5-pro
   ```
3. Ensure your `GEMINI_API_KEY` is set correctly.

### 2. Ollama (Local)
Ollama lets you run models completely offline on your own computer.
1. Make sure you have pulled your desired model locally (e.g., `ollama run llama3.2`).
2. Open your `.env` file.
3. Edit the `OLLAMA_MODEL` line to match:
   ```
   OLLAMA_MODEL=llama3.2
   ```
4. Select **Ollama** from the sidebar dropdown in the Streamlit app.

### 3. LM Studio (Local)
LM Studio is another local AI manager with a graphical interface.
1. Open LM Studio, search for a model (like `gemma4-e4b`), download it, and load it.
2. Go to the **Local Server** tab in LM Studio and click **Start Server**.
3. Edit the `LMSTUDIO_MODEL` line in `.env` to match the exact name of the loaded model:
   ```
   LMSTUDIO_MODEL=gemma4-e4b
   ```
4. Select **LM Studio** from the sidebar dropdown in the Streamlit app.

---

> [!IMPORTANT]
> **Remember to restart your Streamlit server** (press `Ctrl+C` in the terminal and run `streamlit run app.py` again) whenever you make changes to your `.env` file so the app loads the new settings!

## Known Limitations

- The application heavily relies on the LLM's ability to return valid JSON. If the model fails to return properly formatted JSON, the parsing will fail. Using capable models like `gemini-2.5-flash` or `qwen2.5-coder` locally is recommended.
- Code execution is not supported.
