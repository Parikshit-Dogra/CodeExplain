from typing import List
from pydantic import BaseModel, Field

class LineExplanation(BaseModel):
    line_number: int
    code: str
    explanation: str

class ResponseSchema(BaseModel):
    detected_language: str = Field(description="The programming language of the code, auto-detected if not specified.")
    summary: str = Field(description="A brief summary of what the code does.")
    plain_english: str = Field(description="A plain-English explanation of the code for beginners.")
    line_by_line: List[LineExplanation] = Field(description="Line-by-line breakdown of the code.")
    time_complexity: str = Field(description="Time complexity analysis (Best, Average, Worst).")
    space_complexity: str = Field(description="Space complexity analysis.")
    improvements: List[str] = Field(description="Maximum 5 meaningful suggestions for improvement.")
    translation: str = Field(description="Translation of the explanation into the selected language (if requested).")
    quiz: List[str] = Field(description="5 comprehension questions to test understanding.")
