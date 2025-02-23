from .movie_controller import get_movies, get_movies_by_name
from .reporter_controller import get_reporters
from .document_controller import search_documents

__all__ = ["get_movies", "get_movies_by_name", "get_reporters", "search_documents"]