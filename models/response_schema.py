from typing import List
from pydantic import BaseModel, Field

class LineExplanation(BaseModel):
    line_number: int
    code: str
    explanation: str

class ResponseSchema(BaseModel):
    detected_language: str = Field(description="The programming language of the code, auto-detected if not specified.")
    summary: str = Field(description="A brief summary of what the code does.")
    layman_explanation: str = Field(description="A layman explanation of the code for beginners.")
    line_by_line: List[LineExplanation] = Field(description="Line-by-line breakdown of the code.")
    time_complexity: str = Field(description="Time complexity analysis (Best, Average, Worst).")
    space_complexity: str = Field(description="Space complexity analysis.")
    improvements: List[str] = Field(description="Maximum 5 meaningful suggestions for improvement.")
    translation: str = Field(description="Translation of the explanation into the selected language (if requested).")

class QuizOption(BaseModel):
    text: str = Field(description="The text of the option.")
    is_correct: bool = Field(description="Whether this option is the correct answer.")
    explanation: str = Field(description="A layman explanation of why this option is correct or incorrect.")

class QuizQuestion(BaseModel):
    question: str = Field(description="The comprehension question related to the code snippet.")
    options: List[QuizOption] = Field(description="4 clickable options for this question.")

class QuizSchema(BaseModel):
    questions: List[QuizQuestion] = Field(description="Exactly 3 comprehension questions.")
