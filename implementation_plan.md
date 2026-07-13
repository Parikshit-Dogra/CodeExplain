# CodeExplain Implementation Plan

This plan outlines the steps to build the CodeExplain plain-English code tutor based on the requirements in `prompt.txt`.

## User Review Required

> [!IMPORTANT]
> Please review the proposed folder structure, the abstraction design, and the sequence of phases. Once approved, I will proceed to execute the plan and create the files.

## Open Questions

> [!TIP]
> 1. Which model provider should be the default when starting the app? (Assuming `gemini` based on `.env` example).
> 2. What `google-genai` or `google-generativeai` package version should be used for Gemini? I'll use the latest available.

## Proposed Changes

We will build the application iteratively across the following components:

### 1. Project Setup
- Establish the `requirements.txt` with dependencies: `streamlit`, `python-dotenv`, `requests`, `google-genai`, `openai`, `pydantic`.
- Create a `.env` template file containing placeholders for `GEMINI_API_KEY`, `MODEL_PROVIDER`, `LOCAL_MODEL`, `LMSTUDIO_URL`, and `OLLAMA_URL`.

### 2. LLM Abstraction Layer (`llm/`)
- **`llm/base_llm.py`**: Define a base interface `BaseLLM` with a `generate(prompt: str) -> str` method.
- **`llm/gemini_provider.py`**: Implement the `GeminiProvider` class using the Gemini API.
- **`llm/ollama_provider.py`**: Implement the `OllamaProvider` class using requests to Ollama's local endpoint.
- **`llm/lmstudio_provider.py`**: Implement the `LMStudioProvider` class using the OpenAI compatible endpoint for LM Studio.
- **`llm/llm_factory.py`**: A factory function to instantiate the correct provider based on `MODEL_PROVIDER` setting.

### 3. Models and Prompts (`models/` and `config/`)
- **`models/response_schema.py`**: Pydantic models to structure the JSON output (Summary, Plain English, Line-by-line, Time Complexity, Space Complexity, Improvements, Quiz).
- **`config/prompts.py`**: The central prompt template that instructs the LLM to output the specific JSON structure.
- **`config/settings.py`**: Load and validate environment variables.

### 4. Core Services (`services/`)
- **`services/code_explainer.py`**: The central service that takes code, language, and quiz difficulty, constructs the prompt, calls the LLM factory, parses the JSON response, and returns a structured object.

### 5. Streamlit Application (`app.py`)
- **Left Panel**: Settings for Model Provider, Language, and Quiz Difficulty.
- **Main Area**: Code text area, target language selector, and an "Explain Code" button.
- **Results Rendering**: Logic to display the parsed JSON response in clearly separated, readable sections as requested.

### 6. Documentation
- **`README.md`**: Update with project overview, setup instructions, usage, and supported models.

## Verification Plan

### Automated Tests
- For this initial implementation, no automated test suite is explicitly requested in the prompt, but we will ensure syntax correctness and clean module imports.

### Manual Verification
- Run `streamlit run app.py` and verify the UI matches the design.
- Test explanation generation with mock LLM responses or actual endpoints if configured, verifying that the output JSON is parsed and displayed correctly in all sections.
