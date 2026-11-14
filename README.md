# TMDB Movie Data ETL Pipeline

A beginner Python-based Extract, Transform, Load (ETL) pipeline that fetches top-rated movie records from The Movie Database (TMDB) REST API across three pages, cleans and standardizes them using pandas, and saves them to a CSV file.

## Project Overview

This is part of my data engineering roadmap where I am building practical, end-to-end Python pipeline skills:
- **Extract:** Fetch movie records from TMDB's top-rated endpoint across pages 1 to 3 with timeout retries and error logging.
- **Transform:** Select core fields, rename IDs, parse ISO dates, drop rows with missing IDs, and remove duplicate movies using pandas.
- **Validate:** Run sanity checks before writing any data to ensure the DataFrame is not empty and no movie title is missing or blank.
- **Load:** Save the cleaned DataFrame to `data/movies_cleaned.csv` using `pathlib` for safe directory creation.

## Pipeline Architecture

```text
TMDB REST API (Pages 1–3)
         ↓
  extract.py (Requests + Timeout Retries)
         ↓
  transform.py (Pandas Cleaning & Deduplication)
         ↓
  Validation in pipeline.py (Empty Check & Title Validation)
         ↓
  load.py (Save to data/movies_cleaned.csv)
```

## File Structure

```text
tmdb-etl-project/
├── extract.py         # Fetches movie data from TMDB API with timeout retries
├── transform.py       # Cleans records, parses release dates, and deduplicates
├── load.py            # Writes cleaned DataFrame to CSV using pathlib
├── pipeline.py        # Entry point: runs extraction, validation, and loading
├── requirements.txt   # Dependencies (requests, pandas, python-dotenv)
├── .env.example       # Template for environment variables
└── README.md          # Project documentation and notes
```

## Setup & Running the Pipeline

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nirajbasnet009/tmdb-etl-project.git
   cd tmdb-etl-project
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your TMDB API Key:**
   Copy `.env.example` to `.env` and paste your TMDB API key:
   ```bash
   cp .env.example .env
   ```
   Edit `.env`:
   ```text
   TMDB_API_KEY=your_actual_api_key_here
   ```
   *(If `TMDB_API_KEY` is not found in `.env`, the pipeline will securely prompt you using `getpass()` in the terminal).*

5. **Run the pipeline:**
   ```bash
   python pipeline.py
   ```

### Output Location

The pipeline writes the cleaned records to:
```text
data/movies_cleaned.csv
```

## What I Personally Verified

During testing, I verified the following behaviors locally:
- **3-Page Batch Execution:** Extracted 20 movies per page (60 raw records total across pages 1 to 3) and saved 60 clean rows to CSV.
- **Idempotency:** Running the pipeline a second time produced the exact same 60 rows without creating duplicates.
- **Failed Run Protection:** An invalid API key triggered an HTTP `401 Unauthorized` and failed immediately, leaving the existing CSV completely untouched with an identical SHA-256 checksum.
- **Empty-Data Check:** When simulating an empty DataFrame before the loading step, the pipeline raised a `ValueError` and stopped before touching disk.

## Next Steps

- Bounded exponential backoff retries for HTTP 429 rate limits and 5xx server errors.
- Atomic file writes to prevent partial file corruption.
- Automated unit and integration tests.
- Loading into a relational database (MySQL / PostgreSQL).
