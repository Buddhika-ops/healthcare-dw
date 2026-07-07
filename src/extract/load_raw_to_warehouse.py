import pandas as pd
from pathlib import Path
from sqlalchemy import text,create_engine

DB_URL = "postgresql+psycopg2://dwuser:devpass@localhost:5432/healthcare_dw"
engine = create_engine(DB_URL)

FILES_TO_TABLES = {
        "raw_patients.csv": "raw_patients",
        "raw_encounters.csv":"raw_encounters",
        "raw_providers.csv":"raw_providers",
        "raw_payers.csv":"raw_payers",
        "raw_observations.csv":"raw_observations",
        "raw_claims.csv":"raw_claims",
        "raw_organizations.csv":"raw_organizations"
}    

DIR_PATH = Path(__file__).resolve().parents[2]/"data"/"raw"

def load_raw_to_warehouse():
    for file_name,table_name in FILES_TO_TABLES.items():
        file_path = DIR_PATH / file_name
        print(f"Loading {file_name} -> table '{table_name}' (raw, untransformed) ...")

        df = pd.read_csv(file_path)
        df.to_sql(table_name,engine, if_exists="replace",index=False)
        print(f"  Loaded {len(df)} rows into '{table_name}'")

    print("\nDone. All 7 raw tables loaded into healthcare_dw.")

if __name__ == "__main__":
    load_raw_to_warehouse()