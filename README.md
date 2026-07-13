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
   pip install -r requirements.txt
   ```
3. Set up your environment variables by copying `.env.example` to `.env` (or just editing the `.env` file):
   ```
   GEMINI_API_KEY=your_api_key_here
   MODEL_PROVIDER=gemini  # gemini, ollama, or lmstudio
   LOCAL_MODEL=qwen3:4b
   LMSTUDIO_URL=http://localhost:1234/v1
   OLLAMA_URL=http://localhost:11434
   ```

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

1. Open the application in your browser (usually http://localhost:8501).
2. Select your Model Provider from the sidebar.
3. Choose the target language for the explanation.
4. Select the code language of the snippet you're pasting.
5. Paste your code snippet and click **Explain Code**.

## Supported Models

- **Gemini**: Requires a Google GenAI API key in the `.env` file.
- **Ollama**: Requires Ollama running locally (default: `http://localhost:11434`).
- **LM Studio**: Requires LM Studio running with a local server (default: `http://localhost:1234/v1`).

## Known Limitations

- The application heavily relies on the LLM's ability to return valid JSON. If the model fails to return properly formatted JSON, the parsing will fail. Using capable models like `gemini-2.5-flash` or `qwen2.5-coder` locally is recommended.
- Code execution is not supported.
