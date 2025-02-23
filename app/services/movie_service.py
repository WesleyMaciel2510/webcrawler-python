import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin
from app.models.movie import Movie

class MovieCrawlerService:
    def __init__(self):
        self.base_url = "https://www.rottentomatoes.com/browse/movies_at_home"

    def format_date(self, date_string: str) -> str:
        try:
            # Parse the date string (e.g., "Opened Feb 19, 2025") and format it as ISO 8601
            date_str = date_string.replace("Opened ", "").strip()
            date = datetime.strptime(date_str, "%b %d, %Y")
            return date.isoformat()
        except Exception as e:
            print(f"Error formatting date '{date_string}': {e}")
            return datetime.now().isoformat()  # Fallback to current date

    def crawl_movies(self) -> List[Movie]:
        try:
            print("Fetching movies from:", self.base_url)

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            }

            response = requests.get(self.base_url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            print("Response received, parsing HTML...")

            soup = BeautifulSoup(response.text, "html.parser")
            movies: List[Movie] = []

            # Find all movie tiles
            movie_tiles = soup.select(".discovery-tiles__wrap .js-tile-link")

            for tile in movie_tiles[:10]:  # Limit to 10 movies
                try:
                    # Extract title
                    title_element = tile.select_one(".p--small")
                    title = title_element.text.strip() if title_element else "Unknown Title"

                    # Extract release date
                    release_date_element = tile.select_one(".smaller")
                    release_date_text = release_date_element.text.strip() if release_date_element else None
                    formatted_date = self.format_date(release_date_text) if release_date_text else "N/A"

                    # Extract relative URL
                    relative_url = tile.get("href")
                    full_url = urljoin(self.base_url, relative_url) if relative_url else None

                    # Only add the movie if the title is valid
                    if title != "Unknown Title":
                        movies.append(Movie(
                            title=title,
                            release_date=formatted_date,
                            url=full_url
                        ))

                except Exception as e:
                    print(f"Error parsing movie tile: {e}")

            if not movies:
                raise ValueError("No movies found on the page")

            print(f"Successfully parsed {len(movies)} movies")
            return movies

        except requests.RequestException as e:
            print(f"Network error: {e}")
            raise ValueError(f"Network error: {e}")
        except Exception as e:
            print(f"Error crawling Rotten Tomatoes: {e}")
            raise ValueError(f"Error crawling Rotten Tomatoes: {e}")

    def search_movies_by_name(
        self, search_name: str, page: int, res_per_page: int
    ) -> Dict[str, any]:
        try:
            print(f"Searching for movies with name containing: {search_name}")
            all_movies = self.crawl_movies()

            # Filter movies by name (case-insensitive)
            filtered_movies = [
                movie for movie in all_movies
                if search_name.lower() in movie.title.lower()
            ]

            # Paginate the results
            total = len(filtered_movies)
            start_index = (page - 1) * res_per_page
            paginated_movies = filtered_movies[start_index : start_index + res_per_page]

            return {
                "length": len(paginated_movies),
                "movies": paginated_movies,
                "total": total,
            }

        except Exception as e:
            print(f"Error searching movies by name: {e}")
            raise ValueError(f"Failed to search movies: {e}")