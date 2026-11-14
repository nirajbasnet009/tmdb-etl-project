from getpass import getpass

from extract import extract_movies
from load import load_movies
from transform import transform_movies


def run_pipeline(api_key):
    raw_movies = []

    for page in range(1,4):
        page_movies = extract_movies(api_key, page=page)
        raw_movies.extend(page_movies)
        print(f"Page {page}: fetched {len(page_movies)} movies.")

    clean_movies = transform_movies(raw_movies)
    output_path = load_movies(clean_movies)

    print(f"Fetched {len(raw_movies)} movies. Saved {len(clean_movies)} rows.")
    return output_path


if __name__ == "__main__":
    api_key = getpass("Enter your TMDB API key: ").strip()
    saved_file = run_pipeline(api_key)
    print(f"CSV saved to {saved_file}")