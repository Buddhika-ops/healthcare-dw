import os
import pandas as pd
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

OUTPUT_DIR = Path(__file__).resolve().parents[2] /"data" / "raw"

BASE_URL = os.getenv("API_BASE_URL", "http://api:8000")
endpoint_to_csv = {
    "observations": "raw_observations.csv",
    "claims": "raw_claims.csv",
}

def fetch_all_pages(endpoint,page_size = 100):
    all_records = []
    page = 1

    while True:
        response = requests.get(f"{BASE_URL}/{endpoint}",
                                params= {"page": page, "page_size": page_size})
        
        response.raise_for_status()
        payload = response.json()

        records = payload["data"]
        all_records.extend(records)

        print(f"  Fetched page {page} of {payload['total_pages']} ({len(records)} records)")

        if page >= payload["total_pages"]:
            break
        page +=1
        return all_records

def extract_api():
    for endpoint, file_name in endpoint_to_csv.items():
        print(f"Fetching '{endpoint}' from API...")
        records = fetch_all_pages(endpoint)

        df = pd.DataFrame(records)
        output_path = OUTPUT_DIR / file_name

        df.to_csv(output_path, index=False)
        print(f"Loaded {len(df)} rows into '{file_name}'\n")
    
    print("Done. Both API sources extracted into data/raw.")

if __name__ == "__main__":
    extract_api()

