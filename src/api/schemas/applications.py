from pydantic import BaseModel, Field

class ApplyJobSchema(BaseModel):
    user_id: int = Field(..., examples=[1])  # Пока передаем руками, так как токенов еще нет
    cover_letter: str = Field(..., min_length=10, examples=["Привет! Я идеальный Python разработчик для вашей команды."])

class ApplicationResponseSchema(BaseModel):
    id: int
    job_id: int
    user_id: int
    cover_letter: str

    class Config:
        from_attributes = True
        