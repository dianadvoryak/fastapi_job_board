from pydantic import BaseModel
from typing import List

class JobNotificationEvent(BaseModel):
    job_id: int
    title: str
    company: str
    tags: List[str]
