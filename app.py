# pyrefly: ignore [missing-import]
import streamlit as st
from services.code_explainer import CodeExplainerService
import traceback

st.set_page_config(page_title="CodeExplain - Plain-English Code Tutor", layout="wide")

st.title("👨‍🏫 CodeExplain: Plain-English Code Tutor")

# --- Left Panel ---
st.sidebar.title("Settings")

provider = st.sidebar.selectbox(
    "Model Provider",
    ["Select Provider...", "Gemini", "Ollama", "LM Studio"]
)

language = st.sidebar.selectbox(
    "Explanation Language",
    ["English", "Hinglish"]
)

quiz_difficulty = st.sidebar.selectbox(
    "Quiz Difficulty",
    ["Easy", "Medium", "Hard"]
)

# --- Main Area ---
code_language = st.selectbox(
    "Code Language",
    ["Python", "C++", "Java", "JavaScript", "C", "Go"]
)

code_input = st.text_area("Paste your code here", height=300)

if st.button("Explain Code"):
    if provider == "Select Provider...":
        st.warning("Please select a model provider from the settings (Left Panel).")
    elif not code_input.strip():
        st.warning("Please paste some code.")
    else:
        with st.spinner(f"Generating explanation using {provider}..."):
            try:
                # Initialize service
                explainer = CodeExplainerService(provider_name=provider)
                
                # Fetch explanation
                explanation = explainer.explain_code(
                    code=code_input,
                    language=language,
                    difficulty=quiz_difficulty,
                    code_language=code_language
                )
                
                if explanation:
                    st.success("Explanation generated successfully!")
                    
                    st.markdown("---")
                    st.header("📝 Summary")
                    st.write(explanation.summary)
                    
                    st.markdown("---")
                    st.header("📖 Plain English")
                    st.write(explanation.plain_english)
                    
                    if explanation.translation and language != "English":
                        st.markdown("---")
                        st.header(f"🌐 Translation ({language})")
                        st.write(explanation.translation)
                    
                    st.markdown("---")
                    st.header("🔍 Line-by-line")
                    for line_data in explanation.line_by_line:
                        st.markdown(f"**Line {line_data.line_number}**: `{line_data.code}`")
                        st.markdown(f"> {line_data.explanation}")
                    
                    st.markdown("---")
                    st.header("⏱️ Complexity")
                    st.subheader("Time Complexity")
                    st.write(explanation.time_complexity)
                    st.subheader("Space Complexity")
                    st.write(explanation.space_complexity)
                    
                    st.markdown("---")
                    st.header("💡 Suggested Improvements")
                    for imp in explanation.improvements:
                        st.markdown(f"- {imp}")
                    
                    st.markdown("---")
                    st.header("🧠 Quiz")
                    for q in explanation.quiz:
                        st.markdown(f"- {q}")
                        
            except ValueError as ve:
                st.error(f"Error: {ve}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                st.error("Please check the terminal logs for details.")
                print(traceback.format_exc())
