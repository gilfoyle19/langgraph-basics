from typing import List

from pydantic import BaseModel, Field

class Reflection(BaseModel):
    missing: str = Field(description="What information is missing that would help the agent make a better decision?")
    superfluous: str = Field(description="What information is unnecessary and could be removed to make the agent's decision more efficient?")

class AnswerQuestion(BaseModel):
    answer: str = Field(description="~250 word detailed answer to the question.")
    reflection: Reflection = Field(description="your reflection on the initial answer.")
    search_queries: List[str] = Field(description="a list of 1-3 search queries to research information and improve your answer.")

class ReviseAnswer(AnswerQuestion):
    """Revise your original answer to your question."""

    references: List[str] = Field(
        description="Citations motivating your updated answer."
    )