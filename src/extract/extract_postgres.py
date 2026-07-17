import os
import pandas as pd
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"

DB_CONFIG = {
    "host": os.getenv("OLTP_DB_HOST", "healthcare-oltp"),
    "port": int(os.getenv("OLTP_DB_PORT", "5432")),
    "dbname": os.getenv("OLTP_DB_NAME", "healthcare"),
    "user": os.getenv("OLTP_DB_USER", "healthcare"),
    "password": os.getenv("OLTP_DB_PASSWORD", "healthcare")
}

table_to_csv = {
    "encounters": "raw_encounters.csv",
    "providers": "raw_providers.csv",
    "organizations": "raw_organizations.csv"
}

def extract_postgres():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        for table_name, file_name in table_to_csv.items():
            output_file_path = OUTPUT_DIR / file_name

            print(f"Loading {table_name} -> file '{file_name}' ...")
            df = pd.read_sql(f"select * from {table_name}", conn)

            df.to_csv(output_file_path, index=False)
            print(f"Loaded {len(df)} rows into '{file_name}'")
    finally:
        conn.close()

    print("Done. All three tables loaded into data/raw.")

if __name__ == "__main__":
    extract_postgres()