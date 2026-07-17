# Helthcare Data Warehouse Analytics Pipeline

## Overview

An end-to-end Healthcare Data Warehouse project that integrates data from multiple sources, validates data quality using Great Expectations, transforms data with dbt, orchestrates workflows with Apache Airflow, and visualizes business insights using Metabase.


## Features
- Extract from multiple sources
    - REST API
    - CSV files
    - PostgresSQL oparatinal data base

- Data validation using Great Expectation
- ELT orchestration using Apache Airflow
- Star schema data warehouse design
- Analytical SQL views
- Intaractive dashbord using Matabase
- Dockerized environment


## Architecture
<image>


## Technology Stack
- Python
- PostgreSQL
- dbt
- Pandas
- SQLAlchemy
- Psycopg2
- Apache Airflow
- Great Expectations
- SQL
- Metabase
- Docker
- Git & GitHub


## Data Warehouse Design

### Fact Tables
- fact_encounter - One row per patient visit
- fact_claim_line - One row per claim × responsibility (primary/secondary/patient)
- fact_lab_result - One row per lab observation

### Dimension Tables
- dim_patient - Demographics, computed age (as of today or death date)
- dim_provider - Providers, joined with facility name
- dim_facility - Hospitals, clinics, and other care facilities
- dim_date - Generated calendar dimension (2010–2030)
- dim_payer - Payers

## Analytics Views
- Revenue by Facility
- Provider Performance
- Length of Stay by Facility
- Readmission Rate
- Patient Trend by Gender and Age
- Claim Analytics

## Airflow Orchestration
The workflow is orchestrated using Apache Airflow.
Main Tasks:
 - extract_api
 - extract_csv
 - extract_postgres
 - validate_data
 - load_raw_to_warehouse
 - dbt_run

## What This Project Demonstrates
- Ingesting from three genuinely different source types — flat files, a relational
OLTP database, and a paginated REST API — the way a real hospital's fragmented systems
actually look
- A config-driven data quality framework (Great Expectations) covering not-null,
uniqueness, valid-value, range, and cross-table referential integrity checks
- A proper star schema (5 dimensions, 3 facts) built with dbt, including a
computed age dimension, an unpivoted claims fact table, and surrogate keys where no
natural key existed
- Apache Airflow orchestrating the full pipeline (parallel extraction → validation →
load → transformation) inside Docker
- A PySpark rewrite of one transformation, benchmarked against the dbt/SQL version,
with an honest writeup of when Spark actually pays off
-Real, documented infrastructure troubleshooting across two cloud providers
(Oracle Cloud, Railway) — capacity limits, memory constraints, SSH connectivity, and
safe cleanup of a mis-provisioned paid resource

## Data Model
### Source 
 - Synthea — synthetic patient
data generator. No real patient data is used anywhere in this project


## Pipeline Orchestration
```
extract_csv         -|
extract_postgres     | -> validate_data -> load_raw_to_warehouse -> dbt_run
extract_api         _|

```
The three extractors run in parallel since they have no interdependency. Data quality
validation runs once all three complete, gating the load step — a failure here should
stop the pipeline before bad data ever reaches the warehouse.

Runs inside Docker Compose with dedicated containers for the OLTP source, the data
warehouse, the mock API, and Airflow's own services — all on a shared Docker network.


## Cloud Deployment — What Actually Happened
The original plan was AWS (RDS + MWAA). In practice, this phase surfaced real
infrastructure constraints, documented honestly rather than hidden:
- AWS Free Tier:  as of July 2025, RDS's old "750 hrs/month for 12 months" offer no
longer applies to new accounts — new signups get a depleting credit balance instead
- Oracle Cloud (Always Free): epeated capacity errors on the free ARM shape; a
fallback to the free 1GB AMD Micro instance provisioned successfully but crashed under
memory pressure before any project software was even installed
- Railway: the healthcare_dw Postgres database was successfully deployed and
verified running in the cloud.A live public Metabase
dashboard was attempted on the same platform but hit a JVM memory ceiling. 


## Visualization
- Power BI Desktop has no Mac version 
- Tableau Public's free tier doesn't support live database
connections
- Metabase: was used instead — genuinely free, connects
directly to Postgres, and fits the project's existing containerized architecture.

<image>

## Data Quality
A single, reusable, config-driven validator (not one script per file) runs Great
Expectations checks across all 7 raw sousource files:
- Not-null and uniqueness checks on primary keys
- Valid-value-set checks
- Range checks on financial fields
- Cross-table referential integrity


## Business Insights
- Healthcare revenue trends
- Provider performance
- Facility performance
- Average patient length of stay
- Patient demographics
- Encounter trends
- Readmission rates
- Patient distribution by gender and age


## Project Structure

<image>

## Running This Project

```bash
    git clone https://github.com/<your-username>/healthcare-dw.git
    cd airflow
    docker compose up -d
```
Once containers are healthy, open the Airflow UI at``` http://localhost:8080``` and trigger
the healthcare_pipeline DAG. 

## Author's Note

This project was built iteratively, phase by phase, with a focus on documenting the 
real challenges, decisions, and improvements made throughout the development process.

Instead of presenting only a polished final pipeline, this README captures the actual 
engineering journey — including problems encountered, design changes, and trade-offs.

During development:

- Some KPIs were reduced or removed after evaluating whether the available synthetic 
  healthcare data could realistically support meaningful analysis.
- Several infrastructure approaches were tested, including Oracle Cloud, Railway, 
  and Tableau Public, but were adjusted due to practical limitations.
- Challenges related to data quality, orchestration, deployment, and tooling were 
  documented and resolved as part of the learning process.

The final architecture represents not only the completed data pipeline, but also the 
engineering decisions, problem-solving, and lessons learned throughout the project.

The process of building, testing, failing, improving, and making informed trade-offs 
is an essential part of this project.

## Future Improvements
- Cloud deployment (AWS)
- CI/CD pipeline
- Automated monitoring and alerting
- Data lineage documentation