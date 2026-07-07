SELECT
    "Id" as claim_id,
    "PATIENTID" as patient_id,
    "PROVIDERID" as provider_id,
    "PRIMARYPATIENTINSURANCEID" as primary_insurance_id,
    cast("CURRENTILLNESSDATE" as timestamp) as current_illness_date,
    cast("SERVICEDATE" as timestamp) as service_date,
    "STATUS1" as status_1,
    "STATUS2" as status_2,
    "STATUSP" as status_p,
    "OUTSTANDING1" as outstanding_1,
    "OUTSTANDING2" as outstanding_2,
    "OUTSTANDINGP" as outstanding_p
FROM{{ source("raw","raw_claims") }}