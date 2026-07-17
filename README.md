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

---
# Architecture
```
API Source
|
CSV files
|
PostgresSQL oparatinal data base
|
__________________
Extraction
__________________
|
Great Expectation Data validation
|
PostgreSQL Data Warehouse
|
Apache Airflow DAG
|
dbt Models
|
Staging -> Mart -> Analytics
|
Metabase Dashboard

```
---

|Category        Technology


