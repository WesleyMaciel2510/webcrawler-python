from pydantic import BaseModel
from typing import List
from app.models.movie import Movie # type: ignore

class MovieResponse(BaseModel):
    success: bool
    count: int
    total: int
    page: int
    res_per_page: int
    total_pages: int
    data: List[Movie]

class ErrorResponse(BaseModel):
    success: bool
    error: str