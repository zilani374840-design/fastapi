# ==========================================
# schema.py  ->  Rules for the data coming in / going out of the API (Pydantic)
# ==========================================
from typing import Optional
from pydantic import BaseModel, Field


# Data needed to add a new student
class StudentCreate(BaseModel):
    name: str
    age: int = Field(ge=18, le=30)               # age must be 18 to 30
    email: str
    roll: int
    session: str
    english_score: int = Field(default=0, ge=0, le=100)   # marks must be 0 to 100
    math_score: int = Field(default=0, ge=0, le=100)
    history_score: int = Field(default=0, ge=0, le=100)


# For update every field is optional -> only the fields you send are changed
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    english_score: Optional[int] = Field(default=None, ge=0, le=100)
    math_score: Optional[int] = Field(default=None, ge=0, le=100)
    history_score: Optional[int] = Field(default=None, ge=0, le=100)


# Data sent from the API to the frontend
class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    email: str
    roll: int
    session: str
    english_score: int
    math_score: int
    history_score: int
    average: float
    comment: str
