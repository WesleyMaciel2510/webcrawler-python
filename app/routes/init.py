from .movie_routes import router as movie_router
from .reporter_routes import router as reporter_router
from .document_routes import router as document_router

__all__ = ["movie_router", "reporter_router", "document_router"]