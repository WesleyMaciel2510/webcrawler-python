from pydantic import BaseModel
from typing import Optional

class Movie(BaseModel):
    title: str
    release_date: str
    url: Optional[str] = None