from pydantic import BaseModel
from typing import List


class AnswerRecord(BaseModel):
    question_id: str
    correct: bool
    difficulty: float
    topic: str


class UserSession(BaseModel):
    ability_score: float
    questions_answered: List[AnswerRecord]
    completed: bool