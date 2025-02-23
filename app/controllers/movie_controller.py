from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.movie_service import MovieCrawlerService
from app.schemas.movie_schema import MovieResponse, ErrorResponse
from app.models.movie import Movie

router = APIRouter()
movie_service = MovieCrawlerService()

@router.get("/", response_model=MovieResponse)
async def get_movies(
    page: int = Query(1, ge=1),
    res_per_page: int = Query(30, ge=1),
):
    try:
        print("Fetching movies...")
        movies = movie_service.crawl_movies()

        start_index = (page - 1) * res_per_page
        paginated_movies = movies[start_index : start_index + res_per_page]

        return {
            "success": True,
            "count": len(paginated_movies),
            "total": len(movies),
            "page": page,
            "res_per_page": res_per_page,
            "total_pages": (len(movies) + res_per_page - 1) // res_per_page,
            "data": paginated_movies,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch movies: {str(e)}")

@router.get("/movies/searchByName", response_model=MovieResponse)
async def get_movies_by_name(
    name: Optional[str] = Query(None, description="Name of the movie to search for"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    res_per_page: int = Query(30, ge=1, description="Number of results per page"),
):
    try:
        # Validate the 'name' parameter
        if not name:
            raise HTTPException(
                status_code=400,
                detail="Missing or invalid 'name' query parameter",
            )

        # Call the service to search for movies
        result = movie_service.search_movies_by_name(name, page, res_per_page)

        # Prepare the response
        return {
            "success": True,
            "count": len(result["movies"]),
            "total": result["total"],
            "page": page,
            "res_per_page": res_per_page,
            "total_pages": (result["total"] + res_per_page - 1) // res_per_page,
            "data": result["movies"],
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search movies: {str(e)}",
        )