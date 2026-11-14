# TMDB Movie Data ETL Pipeline

A Python-based Extract, Transform, Load (ETL) pipeline that fetches top-rated movie records from The Movie Database (TMDB) REST API, cleans and standardizes them using Pandas, and loads the output to a cleaned CSV.

## Project Purpose

This project is part of my data engineering roadmap to build practical experience with:
- REST API data extraction with pagination, query parameters, timeouts, and error handling.
- Vectorized data transformations and deduplication using Pandas.
- Safe, idempotent batch loading.

## File Structure

```text
tmdb-etl-project/
├── extract.py         # Fetches movie records page by page from TMDB API with error handling
├── transform.py       # Cleans records, parses release dates, and deduplicates movie IDs
├── load.py            # Idempotently writes cleaned DataFrame to CSV using pathlib
├── pipeline.py        # Pipeline orchestrator prompting for API key and executing E-T-L
├── requirements.txt   # Minimal dependencies (requests, pandas)
└── README.md          # Project documentation and verified results
```

## Setup & Installation

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

## Running the Pipeline

Run the pipeline entry point:

```bash
python pipeline.py
```

You will be securely prompted to enter your TMDB API Read Access Key or v3 API Key via `getpass()`.

### Output Location

The pipeline outputs cleaned records to:
```text
data/movies_cleaned.csv
```

## Verified Results & Key Takeaways

The following baseline behaviors were verified during local pipeline execution:
- **Page 1 Extraction:** Returned 20 movie records as expected from TMDB top-rated endpoint.
- **3-Page Batch Execution:** Successfully extracted 60 raw movie records across pages 1 to 3 and saved 60 transformed rows.
- **Idempotency:** A second consecutive run still produced exactly 60 rows, rewriting the CSV cleanly without row multiplication or state corruption.
- **Authentication Failure Handling:** An invalid key properly triggered an HTTP `401 Unauthorized` exception.
- **Integrity Under Failure:** The SHA-256 checksum of `data/movies_cleaned.csv` was identical before and after a failed run, verifying that existing destination data is never corrupted or cleared when an API error occurs.

## Planned Improvements

- **Validation Before Loading:** Enforce pre-load sanity checks (`empty` DataFrame checks, required columns `movie_id` and `title`, duplicate checks).
- **Bounded Retries:** Exponential backoff and retry logic for transient network timeouts and HTTP 429/5xx status codes.
- **Environment Configuration:** Support for `TMDB_API_KEY` from environment variables / `.env` with `.env.example` template.
