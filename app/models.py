from typing import Optional
from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str
    student_id: str
    course: Optional[str] = None
    subject: Optional[str] = None
    difficulty: Optional[str] = "medium"
    concept: Optional[str] = None

class QueryResponse(BaseModel):
    response: str
    resources: Optional[list[str]] = []
    visuals: Optional[list[str]] = []
    subject: Optional[str] = None
    concept: Optional[str] = None

class RecommendRequest(BaseModel):
    course: str
    struggled_topic: str

class RecommendResponse(BaseModel):
    recommendations: list[str]

class PracticeRequest(BaseModel):
    subject: str
    course: str
    concept: str
    difficulty: Optional[str] = "medium"
    question: Optional[str] = None

class PracticeResponse(BaseModel):
    practice_question: str
