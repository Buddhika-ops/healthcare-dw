import pandas as pd
import great_expectations as gx
from great_expectations import expectations as gxe
from pathlib import Path

DIR_PATH = Path(__file__).resolve().parents[2] / "data" / "raw"

FILE_CHECKS = {
    "raw_patients.csv": {
        "not_null": ["Id", "BIRTHDATE"],
        "unique": ["Id"],
        "in_set": {"GENDER": ["M", "F"]},
        "between": ["HEALTHCARE_COVERAGE", "HEALTHCARE_EXPENSES", "INCOME"]
    },
    "raw_encounters.csv": {
        "not_null": ["Id", "PATIENT", "PROVIDER", "ORGANIZATION", "START"],
        "unique": ["Id"],
        "between": ["TOTAL_CLAIM_COST"]
    },
    "raw_providers.csv": {
        "not_null": ["Id", "ORGANIZATION"],
        "unique": ["Id"],
    },
    "raw_payers.csv": {
        "not_null": ["Id"],
        "unique": ["Id"],
    },
    "raw_observations.csv": {
        "not_null": ["PATIENT", "ENCOUNTER", "VALUE", "CODE", "DATE"]
    },
    "raw_claims.csv": {
        "not_null": ["Id", "PATIENTID", "PROVIDERID"],
        "unique": ["Id"]
    },
    "raw_organizations.csv": {
        "not_null": ["Id"],
        "unique": ["Id"],
    }
}

context = gx.get_context()
data_source = context.data_sources.add_pandas("pandas_source")


def validate_file(file_name, checks):
    df = pd.read_csv(DIR_PATH / file_name)

    asset_name = file_name.replace(".csv", "")
    data_asset = data_source.add_dataframe_asset(name=asset_name)
    batch_definition = data_asset.add_batch_definition_whole_dataframe(f"{asset_name}_batch")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

    suite = gx.ExpectationSuite(name=f"{asset_name}_suite")

    for column in checks.get("not_null", []):
        suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column=column))

    for column in checks.get("unique", []):
        suite.add_expectation(gxe.ExpectColumnValuesToBeUnique(column=column))

    for column, allowed_values in checks.get("in_set", {}).items():
        suite.add_expectation(gxe.ExpectColumnValuesToBeInSet(column=column, value_set=allowed_values))

    for column in checks.get("between", []):
        suite.add_expectation(gxe.ExpectColumnValuesToBeBetween(column=column, min_value=0))

    return batch.validate(suite)


def validate_all():
    for file_name, checks in FILE_CHECKS.items():
        print(f"\nValidating {file_name}...")

        results = validate_file(file_name, checks)

        for result in results["results"]:
            expectation_type = result["expectation_config"]["type"]
            column = result["expectation_config"]["kwargs"].get("column", "")
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
    payers_id = list(payers_df['Id'])
    encounters_id = list(encounters_df['Id'])

    CHECKS = [
        ("raw_encounters.csv", encounters_df, "PATIENT", patients_id),
        ("raw_encounters.csv", encounters_df, "ORGANIZATION", organizations_id),
        ("raw_encounters.csv", encounters_df, "PROVIDER", providers_id),
        ("raw_encounters.csv", encounters_df, "PAYER", payers_id),
        ("raw_providers.csv", providers_df, "ORGANIZATION", organizations_id),
        ("raw_claims.csv", claims_df, "PROVIDERID", providers_id),
        ("raw_claims.csv", claims_df, "PATIENTID", patients_id),
        ("raw_observations.csv", observations_df, "ENCOUNTER", encounters_id),
        ("raw_observations.csv", observations_df, "PATIENT", patients_id)
    ]

    for i, (file_name, df, column, valid_id) in enumerate(CHECKS):
        asset_name = f"rel_{i}_{file_name.replace('.csv', '')}_{column}"
        data_asset = data_source.add_dataframe_asset(name=asset_name)
        batch_definition = data_asset.add_batch_definition_whole_dataframe(f"{asset_name}_batch")
        batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

        result = batch.validate(gxe.ExpectColumnValuesToBeInSet(column=column, value_set=valid_id))

        status = "PASS" if result["success"] else "FAIL"
        print(f"  [{status}] {file_name}: '{column}' references valid IDs")
        if not result["success"]:
            print(f"       -> {result['result']['unexpected_count']} orphaned references found")


if __name__ == "__main__":
    validate_all()
    validate_relationships()