from getpass import getpass
import os

from extract import extract_movies
from load import load_movies
from transform import transform_movies

from dotenv import load_dotenv


def run_pipeline(api_key):
    raw_movies = []

    for page in range(1,4):
        page_movies = extract_movies(api_key, page=page)
        raw_movies.extend(page_movies)
        print(f"Page {page}: fetched {len(page_movies)} movies.")

    clean_movies = transform_movies(raw_movies)

    if clean_movies.empty:
        raise ValueError("No usable movies to save.")

    titles = clean_movies['title'].astype('string')
    if titles.fillna("").str.strip().eq("").any():
        raise ValueError("Movie title cannot be missing or blank")

    output_path = load_movies(clean_movies)

    print(f"Fetched {len(raw_movies)} movies. Saved {len(clean_movies)} rows.")
    return output_path


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("TMDB_API_KEY", "").strip()
    
    if not api_key:
        api_key = getpass("Enter your TMDB API key: ").strip()
    saved_file = run_pipeline(api_key)
    print(f"CSV saved to {saved_file}")
