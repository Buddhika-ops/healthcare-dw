"""
Mock REST API simulating a hospital lab/claims vendor feed.

Serves observations.csv and claims.csv as paginated JSON, the way a real
vendor API (e.g. a lab system or clearinghouse) would.

Run with:
    uvicorn src.mock_api.main:app --reload
"""

import math
from fastapi import FastAPI, HTTPException, Query
import pandas as pd
from pathlib import Path

app = FastAPI(title="Healthcare Mock API", version="0.1.0")

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "api_source"

# Load once at startup. In Phase 2, swap these CSVs for the real
# Synthea observations.csv / claims.csv files.
observations = pd.read_csv(DATA_DIR / "observations.csv")
claims = pd.read_csv(DATA_DIR / "claims.csv")


def clean_nan(records):
    """Replace any NaN float values with None so they serialize as valid JSON null."""
    for record in records:
        for key, value in record.items():
            if isinstance(value, float) and math.isnan(value):
                record[key] = None
    return records


def paginate(df: pd.DataFrame, page: int, page_size: int):
    if page < 1 or page_size < 1:
        raise HTTPException(status_code=400, detail="page and page_size must be >= 1")

    start = (page - 1) * page_size
    end = start + page_size
    total = len(df)
    records = df.iloc[start:end].to_dict(orient="records")
    records = clean_nan(records)

    return {
        "page": page,
        "page_size": page_size,
        "total_records": total,
        "total_pages": (total + page_size - 1) // page_size,
        "data": records,
    }

@app.get("/")
def root():
    return {
        "service": "Healthcare Mock API",
        "endpoints": ["/observations", "/claims"],
    }


@app.get("/observations")
def get_observations(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000),
):
    return paginate(observations, page, page_size)


@app.get("/claims")
def get_claims(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000),
):
    return paginate(claims, page, page_size)