import pandas as pd
import great_expectations as gx
from pathlib import Path

DIR_PATH = Path(__file__).resolve().parents[2]/"data" / "raw" / "raw_patients.csv"

def validate_patients():
    
    df = pd.read_csv(DIR_PATH)

    context = gx.get_context()

    validator = context.sources.pandas_default.read_dataframe(df)

    validator.expect_column_values_to_not_be_null("Id")
    validator.expect_column_values_to_be_unique("Id")
    validator.expect_column_values_to_not_be_null("BIRTHDATE")
    validator.expect_column_values_to_not_be_null("DEATHDATE")
    validator.expect_column_values_to_be_in_set("GENDER", ["M", "F"])

    results = validator.validate()

    print(f"Checked {len(df)} rows in raw_patients.csv\n")

    for result in results["results"]:
            expectation_type = result["expectation_config"]["expectation_type"]
            column = result["expectation_config"]["kwargs"].get("column", "")
            success = result["success"]
            status = "PASS" if success else "FAIL"
            print(f"[{status}] {expectation_type} on '{column}'")
    
            if not success:
                unexpected_count = result["result"].get("unexpected_count", "?")
                print(f"       -> {unexpected_count} unexpected values found")
    
    print(f"\nOverall result: {'ALL CHECKS PASSED' if results['success'] else 'SOME CHECKS FAILED'}")
    
 
if __name__ == "__main__":
    validate_patients()
 
