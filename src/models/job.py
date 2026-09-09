from sqlalchemy import String, Text, ForeignKey, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import BaseModel

class Job(BaseModel):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False)

    # Массив тегов/навыков (например: ['fastapi', 'postgres', 'redis'])
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)

    employer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    employer: Mapped["User"] = relationship("User", back_populates="jobs")
