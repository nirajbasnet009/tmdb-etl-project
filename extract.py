# ETL: Import libraries for API extraction

import requests
import logging


# ETL: Extract movie data from TMDB

logger = logging.getLogger(__name__)
def extract_movies(api_key, page=1):
    url = "https://api.themoviedb.org/3/movie/top_rated"

    params = {
        "api_key": api_key,
        "page": page
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        movies = response.json()['results']


    except requests.exceptions.HTTPError as error:
        logger.error("TMDB page %s failed with HTTP status %s.",page, error.response.status_code)
        raise

    except requests.exceptions.Timeout:
        logger.error("TMDB request timed out on page %s.",page)
        raise

    except requests.exceptions.ConnectionError:
        logger.error('Could not connect to the TMDB while fetching page %s.',page)
        raise
    
    return movies


if __name__ == "__main__":
    from getpass import getpass

    api_key = getpass("Enter your TMDB API key: ")
    movies = extract_movies(api_key)

    print("Returned type:", type(movies).__name__)
    print("Movie count:", len(movies))

    if movies:
        print("First movie title:", movies[0]['title'])

    from transform import transform_movies

    clean_movies = transform_movies(movies)

    print("Cleaned shape:", clean_movies.shape)
    print(clean_movies[["movie_id", "title", "release_date"]].head())

    from load import load_movies

    saved_file = load_movies(clean_movies)
    print("CSV saved to:", saved_file)