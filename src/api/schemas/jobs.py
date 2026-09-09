from pydantic import BaseModel, Field
from typing import List

class JobCreateSchema(BaseModel):
    title: str = Field(..., min_length=2, max_length=255, examples=["Python Developer"])
    description: str = Field(..., min_length=10, examples=["We are looking for a Senior FastAPI engineer..."])
    company: str = Field(..., max_length=255, examples=["TechCorp"])
    tags: List[str] = Field(default=[], examples=[["python", "fastapi", "postgres"]])
    employer_id: int = Field(..., examples=[1])  # Пока хардкодим ID, так как авторизацию еще не делали

class JobResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    company: str
    tags: List[str]
    employer_id: int

    class Config:
        from_attributes = True  # Позволяет Pydantic читать данные из ORM-моделей SQLAlchemy