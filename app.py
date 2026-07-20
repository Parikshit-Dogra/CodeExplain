# pyrefly: ignore [missing-import]
import streamlit as st
from services.code_explainer import CodeExplainerService
import traceback

st.set_page_config(page_title="CodeExplain - Code in Laymen Tutor", layout="wide")

st.title("CodeExplain")

# --- Left Panel ---
st.sidebar.title("Settings")

provider = st.sidebar.selectbox(
    "Model Provider",
    ["Select Provider...", "Gemini", "Ollama", "LM Studio"]
)

language = st.sidebar.selectbox(
    "Explanation Language",
    [
        "English", "Hinglish", "Hindi", "Spanish", "French", "German", 
        "Chinese", "Japanese", "Korean", "Russian", "Portuguese", 
        "Italian", "Arabic", "Bengali", "Urdu", "Tamil", "Telugu"
    ]
)

quiz_difficulty = st.sidebar.selectbox(
    "Quiz Difficulty",
    ["Easy", "Medium", "Hard"]
)

# --- Main Area ---
code_language = "Auto-detect"

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
                    st.session_state.explanation = explanation
                        
            except ValueError as ve:
                st.error(f"Error: {ve}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                st.error("Please check the terminal logs for details.")
                print(traceback.format_exc())

if "explanation" in st.session_state:
    explanation = st.session_state.explanation
    st.success("Explanation generated successfully!")
    
    st.info(f"**Detected Language:** {explanation.detected_language}")
    
    st.markdown("---")
    st.header("Summary")
    st.write(explanation.summary)
    
    st.markdown("---")
    st.header("Layman Explanation")
    st.write(getattr(explanation, "layman_explanation", getattr(explanation, "plain_english", "Please re-generate the explanation.")))
    
    if explanation.translation and language != "English":
        st.markdown("---")
        st.header(f"Translation ({language})")
        st.write(explanation.translation)
    
    st.markdown("---")
    st.header("Line-by-line")
    for line_data in explanation.line_by_line:
        st.markdown(f"**Line {line_data.line_number}**: `{line_data.code}`")
        st.markdown(f"> {line_data.explanation}")
    
    st.markdown("---")
    st.header("Complexity")
    st.subheader("Time Complexity")
    st.write(explanation.time_complexity)
    st.subheader("Space Complexity")
    st.write(explanation.space_complexity)
    
    st.markdown("---")
    st.header("Suggested Improvements")
    for imp in explanation.improvements:
        st.markdown(f"- {imp}")

st.markdown("---")
st.header("Interactive Quiz")
if st.button("Generate Quiz"):
    if provider == "Select Provider...":
        st.warning("Please select a model provider from the settings (Left Panel).")
    elif not code_input.strip():
        st.warning("Please paste some code.")
    else:
        with st.spinner(f"Generating quiz using {provider}..."):
            try:
                explainer = CodeExplainerService(provider_name=provider)
                quiz = explainer.generate_quiz(
                    code=code_input,
                    difficulty=quiz_difficulty
                )
                
                if quiz:
                    st.session_state.current_quiz = quiz
                    st.session_state.quiz_answers = {}
                    st.rerun()
            except ValueError as ve:
                st.error(f"Error: {ve}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                print(traceback.format_exc())

if "current_quiz" in st.session_state:
    quiz = st.session_state.current_quiz
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
        
    for i, q in enumerate(quiz.questions):
        st.subheader(f"Q{i+1}: {q.question}")
        
        if i in st.session_state.quiz_answers:
            selected_idx = st.session_state.quiz_answers[i]
            selected_option = q.options[selected_idx]
            
            st.write(f"**Your Answer:** {selected_option.text}")
            if selected_option.is_correct:
                st.success("Correct!")
            else:
                st.error("Incorrect.")
            
            st.info(f"**Explanation:** {selected_option.explanation}")
        else:
            for opt_idx, opt in enumerate(q.options):
                if st.button(opt.text, key=f"q_{i}_opt_{opt_idx}"):
                    st.session_state.quiz_answers[i] = opt_idx
                    st.rerun()
