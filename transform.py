import pandas as pd

MOVIE_COLUMNS = [
    'id',
    'title',
    'overview',
    'popularity',
    'release_date',
    'vote_average',
    'vote_count'
]


def transform_movies(movies):
    movies_df = pd.DataFrame(movies, columns=MOVIE_COLUMNS)
    movies_df = movies_df.rename(columns={'id':'movie_id'})

    movies_df['release_date'] = pd.to_datetime(movies_df['release_date'], format="%Y-%m-%d", errors='coerce')

    return (
    movies_df
    .dropna(subset=['movie_id'])
    .drop_duplicates(subset=['movie_id'])
    .reset_index(drop=True)
    ) 