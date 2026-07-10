import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text

DB_URL = "postgresql+psycopg2://warehouse:warehouse@healthcare-dw:5432/healthcare_dw"
engine = create_engine(DB_URL)

FILES_TO_TABLES = {
    "raw_patients.csv": "raw_patients",
    "raw_encounters.csv": "raw_encounters",
    "raw_providers.csv": "raw_providers",
    "raw_payers.csv": "raw_payers",
    "raw_observations.csv": "raw_observations",
    "raw_claims.csv": "raw_claims",
    "raw_organizations.csv": "raw_organizations"
}

DIR_PATH = Path(__file__).resolve().parents[2] / "data" / "raw"

def infer_pg_type(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "BIGINT"
    elif pd.api.types.is_float_dtype(dtype):
        return "DOUBLE PRECISION"
    elif pd.api.types.is_bool_dtype(dtype):
        return "BOOLEAN"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "TIMESTAMP"
    else:
        return "TEXT"

def load_dataframe(df, table_name, conn):
    columns_sql = ", ".join(f'"{col}" {infer_pg_type(dtype)}' for col, dtype in df.dtypes.items())
    conn.execute(text(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns_sql})'))
    conn.execute(text(f'TRUNCATE TABLE "{table_name}"'))

    df = df.where(pd.notnull(df), None)
    records = df.to_dict("records")
    if not records:
        return

    cols = list(df.columns)
    col_list = ", ".join(f'"{c}"' for c in cols)
    placeholders = ", ".join(f":{c}" for c in cols)
    insert_stmt = text(f'INSERT INTO "{table_name}" ({col_list}) VALUES ({placeholders})')
    conn.execute(insert_stmt, records)

def load_raw_to_warehouse():
    with engine.begin() as conn:
        for file_name, table_name in FILES_TO_TABLES.items():
            print(f"Loading {file_name} -> table '{table_name}' (raw, untransformed) ...")
            df = pd.read_csv(DIR_PATH / file_name)
            load_dataframe(df, table_name, conn)
            print(f"  Loaded {len(df)} rows into '{table_name}'")

    print("\nDone. All 7 raw tables loaded into healthcare_dw.")

if __name__ == "__main__":
    load_raw_to_warehouse()