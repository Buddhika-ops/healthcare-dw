import pandas as pd
import great_expectations as gx
from pathlib import Path

DIR_PATH = Path(__file__).resolve().parents[2] /"data"/"raw"

FILE_CHECKS = {
        
        "raw_patients.csv":{
            "not_null":["Id","BIRTHDATE"],
            "unique" : ["Id"],
            "in_set" : {"GENDER":["M","F"]},
            "between": ["HEALTHCARE_COVERAGE","HEALTHCARE_EXPENSES","INCOME"]
        },
        "raw_encounters.csv":{
            "not_null":["Id","PATIENT","PROVIDER","ORGANIZATION","START"],
            "unique" : ["Id"],
            "between": ["TOTAL_CLAIM_COST"]
        },
        "raw_providers.csv":{
            "not_null":["Id","ORGANIZATION"],
            "unique" : ["Id"],
        },
        "raw_payers.csv":{
            "not_null":["Id"],
            "unique" : ["Id"],
        },
        "raw_observations.csv" :{
            "not_null":["PATIENT","ENCOUNTER","VALUE","CODE","DATE"]
        },
        "raw_claims.csv":{
            "not_null":["Id","PATIENTID","PROVIDERID"],
            "unique" : ["Id"]
        },
        "raw_organizations.csv":{
        "not_null": ["Id"],
        "unique": ["Id"],
        }
    }


def validate_file(file_path,checks):
        df = pd.read_csv(file_path)

        context = gx.get_context()
        validator = context.sources.pandas_default.read_dataframe(df)

        for column in checks.get("not_null",[]):
            validator.expect_column_values_to_not_be_null(column)

        for column in checks.get("unique",[]):
            validator.expect_column_values_to_be_unique(column)

        for column,allowed_values in checks.get("in_set",{}).items():
            validator.expect_column_values_to_be_in_set(column, allowed_values)
        
        for column in checks.get("between",[]):
            validator.expect_column_values_to_be_between(column, min_value = 0)

        return validator.validate()

def validate_all():
    for  file_name, checks in FILE_CHECKS.items():
        file_path = DIR_PATH/ file_name

        print(f"\nValidating {file_name}...")

        results = validate_file(file_path,checks)

        for result in results["results"]:
            expectation_type = result["expectation_config"]["expectation_type"]
            column = result["expectation_config"]["kwargs"].get("column","")
            status = "PASS" if result["success"] else "FAIL"
            print(f"  [{status}] {expectation_type} on '{column}'")

        overall = "ALL CHECKS PASSED" if results["success"] else "SOME CHECKS FAILED"
        print(f"  -> {overall}")



def validate_relationships():
    patients_df = pd.read_csv(DIR_PATH / "raw_patients.csv")
    encounters_df = pd.read_csv(DIR_PATH / "raw_encounters.csv")
    providers_df = pd.read_csv(DIR_PATH / "raw_providers.csv")
    payers_df = pd.read_csv(DIR_PATH / "raw_payers.csv")
    observations_df = pd.read_csv(DIR_PATH / "raw_observations.csv")
    claims_df = pd.read_csv(DIR_PATH / "raw_claims.csv")
    organizations_df = pd.read_csv(DIR_PATH / "raw_organizations.csv")

    patients_id = list(patients_df['Id'])
    providers_id = list(providers_df['Id'])
    organizations_id = list(organizations_df['Id'])
    encounters_id = list(encounters_df['Id'])
    payers_id = list(payers_df['Id'])

    CHECKS = [
         ("raw_encounters.csv",encounters_df,"PATIENT",patients_id),
         ("raw_encounters.csv",encounters_df,"ORGANIZATION",organizations_id),
         ("raw_encounters.csv",encounters_df,"PROVIDER",providers_id),
         ("raw_encounters.csv",encounters_df,"PAYER",payers_id),

         ("raw_providers.csv",providers_df,"ORGANIZATION",organizations_id),

         ("raw_claims.csv",claims_df,"PROVIDERID",providers_id),
         ("raw_claims.csv",claims_df,"PATIENTID",patients_id),

         ("raw_observations.csv",observations_df,"ENCOUNTER",encounters_id),
         ("raw_observations.csv",observations_df,"PATIENT",patients_id)
    ]

    for file_name, df, column, valid_id in CHECKS:
         context = gx.get_context()
         validator = context.sources.pandas_default.read_dataframe(df)
         result = validator.expect_column_values_to_be_in_set(column,valid_id)
         status = "PASS" if result["success"] else "FAIL"
         print(f"  [{status}] {file_name}: '{column}' references valid IDs")
         if not result["success"]:
            print(f"       -> {result['result']['unexpected_count']} orphaned references found")
         
if __name__ == "__main__":
     validate_all()
     validate_relationships() 