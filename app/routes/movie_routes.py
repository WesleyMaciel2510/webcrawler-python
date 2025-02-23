from fastapi import APIRouter
from app.controllers.movie_controller import get_movies, get_movies_by_name

router = APIRouter()

# Movie-related routes
router.get("/", summary="Get top movies")(get_movies)
router.get("/searchByName", summary="Search movies by name")(get_movies_by_name)