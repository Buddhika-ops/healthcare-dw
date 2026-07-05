import pandas as pd
from pathlib import Path

INPIT_DIR = Path(__file__).resolve().parents[2] /"data" / "legacy_export"
OUTPUT_DIR = Path(__file__).resolve().parents[2] /"data" / "raw"

legacy_to_raw = {
    "patients.csv":"raw_patients.csv",
    "payers.csv":"raw_payers.csv"
}

def extract_csv():
    for file_name , raw_file_name in legacy_to_raw.items():

        input_file_path = INPIT_DIR / file_name
        output_file_path = OUTPUT_DIR / raw_file_name

        print(f"Loading {file_name} -> file '{input_file_path}' ...")
        df = pd.read_csv(input_file_path)
        df.to_csv(output_file_path,index=False)
        print(f"  Loaded {len(df)} rows into '{raw_file_name}'")

    print("Done. All two file loaded into data/raw.")
    
if __name__ == "__main__":
    extract_csv()