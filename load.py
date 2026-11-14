from pathlib import Path

def load_movies(movies_df):
    project_dir = Path(__file__).resolve().parent
    output_path = project_dir/"data"/"movies_cleaned.csv"

    output_path.parent.mkdir(parents=True,exist_ok=True)
    movies_df.to_csv(output_path, index = False)

    return output_path