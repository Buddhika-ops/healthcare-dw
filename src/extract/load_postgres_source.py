"""
Loads the 'PostgreSQL OLTP source' CSVs (encounters, providers, organizations)
into the healthcare-oltp Postgres container.

hospital live oparational database.

"""
import os
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

DB_URL = (
    f"postgresql+psycopg2://{os.getenv('OLTP_DB_USER', 'healthcare')}:{os.getenv('OLTP_DB_PASSWORD', 'healthcare')}"
    f"@{os.getenv('OLTP_DB_HOST', 'localhost')}:{os.getenv('OLTP_DB_PORT', '5433')}/{os.getenv('OLTP_DB_NAME', 'healthcare')}"
)
DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "postgres_source"



engine = create_engine(DB_URL)

file_to_tables = {
    "encounters.csv":"encounters",
    "providers.csv":"providers",
    "organizations.csv":"organizations"
}

for file_name,table_name in file_to_tables.items():
    file_path = DATA_DIR / file_name
    print(f"Loading {file_name} -> table '{file_name}' ...")
    df = pd.read_csv(file_path)

    df.to_sql(table_name,engine,if_exists="replace",index=False)
    print(f"  Loaded {len(df)} rows into '{table_name}'")

print("Done. All three tables loaded into Postgres.")