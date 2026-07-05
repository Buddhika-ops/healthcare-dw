import pandas as pd
from pathlib import Path
from db import get_engine

engine = get_engine()
OUTPUT_DIR = Path(__file__).resolve().parents[2] /"data" / "raw"

table_to_csv ={
    "encounters": "raw_encounters.csv",
    "providers": "raw_providers.csv",
    "organizations": "raw_organizations.csv"
} 

def extract_postgres():
    for table_name,file_name in table_to_csv.items():
        output_file_path = OUTPUT_DIR / file_name

        print(f"Loading {table_name} -> file '{file_name}' ...")
        df = pd.read_sql(f"select * from {table_name}",engine)

        df.to_csv(output_file_path,index=False)
        print(f"Loaded {len(df)} rows into '{file_name}'")

    print("Done. All three tables loaded into data/raw.")

if __name__ == "__main__":
    extract_postgres()

    