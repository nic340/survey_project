from typing import Optional
from sqlmodel import Field, SQLModel

class Survey(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: str
    rating: int
    feedback: Optional[str] = None