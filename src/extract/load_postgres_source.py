"""
Loads the 'PostgreSQL OLTP source' CSVs (encounters, providers, organizations)
into the healthcare-oltp Postgres container.

hospital live oparational database.

"""
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

DB_URL = "postgresql+psycopg2://healthcare:healthcare@localhost:5433/healthcare"
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