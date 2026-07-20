"""
This is the main entry point for the CodeExplain Streamlit application.
It handles the user interface (UI) rendering, captures user inputs, 
interacts with the backend services (CodeExplainerService), 
and displays the generated explanations and quizzes.
"""

# pyrefly: ignore [missing-import]
import streamlit as st
from services.code_explainer import CodeExplainerService
import traceback

# 1. Page Configuration
# Set up the basic properties of the Streamlit web page, like the title and layout style.
st.set_page_config(page_title="CodeExplain - Code in Laymen Tutor", layout="wide")

st.title("CodeExplain")

# 2. Sidebar (Left Panel) Setup
# The sidebar contains all the configuration settings for the user to customize their experience.
st.sidebar.title("Settings")

# Dropdown to select which LLM backend to use
provider = st.sidebar.selectbox(
    "Model Provider",
    ["Select Provider...", "Gemini", "Ollama", "LM Studio"]
)

# Dropdown to select the target language for the explanation translation
language = st.sidebar.selectbox(
    "Explanation Language",
    [
        "English", "Hinglish", "Hindi", "Spanish", "French", "German", 
        "Chinese", "Japanese", "Korean", "Russian", "Portuguese", 
        "Italian", "Arabic", "Bengali", "Urdu", "Tamil", "Telugu"
    ]
)

# Dropdown to set the difficulty level for the generated quiz questions
quiz_difficulty = st.sidebar.selectbox(
    "Quiz Difficulty",
    ["Easy", "Medium", "Hard"]
)

# 3. Main Area Setup
code_language = "Auto-detect"

# Text area where the user pastes the code they want explained
code_input = st.text_area("Paste your code here", height=300)

# 4. Code Explanation Logic
# Trigger the explanation generation when the button is clicked
if st.button("Explain Code"):
    # Validation: Ensure a provider is selected and code is provided
    if provider == "Select Provider...":
        st.warning("Please select a model provider from the settings (Left Panel).")
    elif not code_input.strip():
        st.warning("Please paste some code.")
    else:
        # Show a loading spinner while the backend processes the request
        with st.spinner(f"Generating explanation using {provider}..."):
            try:
                # Initialize the core service with the selected provider
                explainer = CodeExplainerService(provider_name=provider)
                
                # Fetch the structured explanation from the LLM
                explanation = explainer.explain_code(
                    code=code_input,
                    language=language,
                    difficulty=quiz_difficulty,
                    code_language=code_language
                )
                
                # If successful, store the result in Streamlit's session state 
                # so it persists across UI reruns.
                if explanation:
                    st.session_state.explanation = explanation
                        
            except ValueError as ve:
                # Catch specific parsing errors and show to the user
                st.error(f"Error: {ve}")
            except Exception as e:
                # Catch unexpected errors, log them, and show a generic message
                st.error(f"An unexpected error occurred: {e}")
                st.error("Please check the terminal logs for details.")
                print(traceback.format_exc())

# 5. Render the Code Explanation Results
# If an explanation exists in the session state, render its components
if "explanation" in st.session_state:
    explanation = st.session_state.explanation
    st.success("Explanation generated successfully!")
    
    # Display the auto-detected language
    st.info(f"**Detected Language:** {explanation.detected_language}")
    
    # Display the high-level summary
    st.markdown("---")
    st.header("Summary")
    st.write(explanation.summary)
    
    # Display the beginner-friendly "layman" explanation
    st.markdown("---")
    st.header("Layman Explanation")
    st.write(getattr(explanation, "layman_explanation", getattr(explanation, "plain_english", "Please re-generate the explanation.")))
    
    # Display the translated explanation if a non-English language was selected
    if explanation.translation and language != "English":
        st.markdown("---")
        st.header(f"Translation ({language})")
        st.write(explanation.translation)
    
    # Display the detailed line-by-line breakdown
    st.markdown("---")
    st.header("Line-by-line")
    for line_data in explanation.line_by_line:
        st.markdown(f"**Line {line_data.line_number}**: `{line_data.code}`")
        st.markdown(f"> {line_data.explanation}")
    
    # Display the algorithm complexity analysis
    st.markdown("---")
    st.header("Complexity")
    st.subheader("Time Complexity")
    st.write(explanation.time_complexity)
    st.subheader("Space Complexity")
    st.write(explanation.space_complexity)
    
    # Display actionable improvement suggestions
    st.markdown("---")
    st.header("Suggested Improvements")
    for imp in explanation.improvements:
        st.markdown(f"- {imp}")

# 6. Interactive Quiz Section
st.markdown("---")
st.header("Interactive Quiz")

# Trigger quiz generation when the button is clicked
if st.button("Generate Quiz"):
    if provider == "Select Provider...":
        st.warning("Please select a model provider from the settings (Left Panel).")
    elif not code_input.strip():
        st.warning("Please paste some code.")
    else:
        with st.spinner(f"Generating quiz using {provider}..."):
            try:
                # Initialize service and request the quiz
                explainer = CodeExplainerService(provider_name=provider)
                quiz = explainer.generate_quiz(
                    code=code_input,
                    difficulty=quiz_difficulty
                )
                
                # Store the quiz data and initialize an empty dictionary 
                # to track user answers in the session state.
                if quiz:
                    st.session_state.current_quiz = quiz
                    st.session_state.quiz_answers = {}
                    st.rerun() # Force UI refresh to display the quiz
            except ValueError as ve:
                st.error(f"Error: {ve}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                print(traceback.format_exc())

# 7. Render the Interactive Quiz UI
# If a quiz exists in the session state, render its questions
if "current_quiz" in st.session_state:
    quiz = st.session_state.current_quiz
    # Ensure answer tracking dictionary exists
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
        
    # Iterate through all generated questions
    for i, q in enumerate(quiz.questions):
        st.subheader(f"Q{i+1}: {q.question}")
        
        # If the user has already answered this question, show the result
        if i in st.session_state.quiz_answers:
            selected_idx = st.session_state.quiz_answers[i]
            selected_option = q.options[selected_idx]
            
            st.write(f"**Your Answer:** {selected_option.text}")
            if selected_option.is_correct:
                st.success("Correct!")
            else:
                st.error("Incorrect.")
            
            # Show the explanation regardless of whether they were right or wrong
            st.info(f"**Explanation:** {selected_option.explanation}")
        else:
            # If the user hasn't answered yet, display the clickable options
            for opt_idx, opt in enumerate(q.options):
                # When an option button is clicked, record the answer and refresh
                if st.button(opt.text, key=f"q_{i}_opt_{opt_idx}"):
                    st.session_state.quiz_answers[i] = opt_idx
                    st.rerun()
