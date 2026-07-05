# Healthcare Data Warehouse — Project Roadmap

## 0. Concept

A synthetic hospital network ("Northwind Health System") runs 3–5 facilities. Patients have
encounters (ER visits, inpatient stays, outpatient appointments), generate diagnoses, procedures,
lab results, and insurance claims. Your job: build a warehouse that lets analysts answer questions
like "what's our 30-day readmission rate by facility?" or "which departments have the highest
claim denial rate this quarter?"

**Critical compliance note:** Use only synthetic data. [Synthea](https://synthetichealth.github.io/synthea/)
generates realistic, statistically valid, fully synthetic patient records (demographics,
encounters, conditions, medications, labs) in CSV/FHIR format — free, open-source, and built
exactly for projects like this. Never use real patient data, even anonymized. This keeps the
project HIPAA-safe and freely shareable in your portfolio/GitHub.

---

## 1. Data Sources (simulating a real hospital's messy landscape)

| Source | Format | What it represents | How to get it |
|---|---|---|---|
| Legacy patient export | CSV | Nightly dump from an old registration system | Synthea `patients.csv`, `payers.csv` |
| EHR operational DB | PostgreSQL | Live encounters, providers, facilities | Load Synthea `encounters`, `providers`, `organizations` into a Postgres OLTP schema |
| Lab / claims feed | REST API | Real-time lab results and insurance claims | Build a small FastAPI/Flask mock API serving Synthea `observations.csv` and `claims.csv` as paginated JSON |

This trio is deliberate — it forces you to build three different extraction patterns (file read,
DB query, HTTP pagination), which is exactly what recruiters want to see.

---

## 2. Data Model — Star Schema (core) + Snowflake extension

**Fact tables** (grain defines everything — get this right first):

- `fact_encounter` — one row per patient visit (admit/discharge dates, length of stay, cost)
- `fact_claim_line` — one row per billed claim line item (amount, denial status)
- `fact_lab_result` — one row per lab test result (value, unit, abnormal flag)

**Dimensions:**

- `dim_patient` — SCD Type 2 (track address/insurance changes over time — a classic warehousing
  concept recruiters look for)
- `dim_provider`
- `dim_facility`
- `dim_diagnosis` — ICD-10 codes
- `dim_procedure` — CPT codes
- `dim_date`
- `dim_insurance_plan`

**Snowflake extension** (to demonstrate you know when/why to normalize further):
- Split `dim_diagnosis` → `dim_diagnosis` + `dim_diagnosis_category` (ICD-10 chapter)
- Split `dim_provider` → `dim_provider` + `dim_specialty`

Document both designs side by side in your README with an ER diagram — this comparison is a
strong portfolio talking point ("here's when I'd choose star vs snowflake and why").

---

## 3. Tech Stack → Project Phase Mapping

| Layer | Tech | Used in phase |
|---|---|---|
| Sources | CSV, PostgreSQL, REST API | Phase 2 |
| Extraction | Python + Pandas | Phase 3 |
| Data quality | Great Expectations | Phase 4 |
| Transformation | dbt | Phase 5 |
| Scale-up | PySpark | Phase 7 |
| Orchestration | Apache Airflow | Phase 6 |
| Analytics | SQL views / materialized views | Phase 8 |
| Cloud | AWS (S3, RDS, MWAA/EC2) | Phase 9 |
| Visualization | Power BI / Tableau | Phase 10 |
| Containerization | Docker | Phase 1, ongoing |
| Version control | Git + GitHub | Ongoing |

---

## 4. Phase-by-Phase Roadmap (suggested: 8–10 weeks, part-time)

**Phase 1 — Environment setup (Week 1)**
- Initialize Git repo, `.gitignore`, README skeleton
- `docker-compose.yml` with a PostgreSQL container
- Project folder structure (see §6)
- Generate a Synthea dataset (a few thousand patients is plenty)

**Phase 2 — Simulate the three sources (Week 1–2)**
- Load a slice of Synthea data into Postgres as your "OLTP" source (`patients`, `encounters`, `providers`)
- Export another slice as raw CSVs (legacy system dump)
- Build a small FastAPI service serving lab results/claims as a paginated JSON API

**Phase 3 — Extraction with Pandas (Week 2–3)**
- Write one extractor per source (`extract_csv.py`, `extract_postgres.py`, `extract_api.py`)
- Land raw extracts into a `raw/` landing zone (local disk or S3 later)
- Log row counts, timestamps — this is your audit trail

**Phase 4 — Data quality gate (Week 3)**
- Great Expectations suites: schema checks, null checks, referential checks
  (e.g., every `encounter` references a valid `patient_id`), value-range checks (lab values,
  dates not in the future)
- Fail the pipeline loudly on critical checks; warn-and-continue on soft ones

**Phase 5 — Transformation with dbt (Week 4–5)**
- `staging/` models: 1:1 cleaned views over raw sources
- `intermediate/` models: joins, dedup, SCD2 logic for `dim_patient`
- `marts/` models: the actual star schema fact and dimension tables
- dbt tests (`unique`, `not_null`, `relationships`) as a second layer of data quality

**Phase 6 — Orchestration with Airflow (Week 5–6)**
- One DAG: `extract → quality_check → dbt_run → dbt_test → refresh_views`
- Sensors/retries for the REST API extractor
- Slack/email alert on failure (optional but impressive)

**Phase 7 — Scale demonstration with PySpark (Week 6–7)**
- Take the largest fact table (e.g., lab results at high volume) and rewrite that one
  transformation in PySpark
- Write a short README section comparing Pandas vs Spark runtime — this "I know when to reach
  for Spark" narrative is exactly what interviewers probe for

**Phase 8 — Analytics layer (Week 7)**
- SQL views: `vw_readmission_rate`, `vw_avg_length_of_stay`, `vw_claim_denial_rate`
- Materialized views for the expensive aggregations, with a refresh step in the Airflow DAG
- `EXPLAIN ANALYZE` a couple of queries and add indexes — shows optimization skill

**Phase 9 — Cloud deployment on AWS (Week 8)**
- S3 as the raw/landing data lake
- RDS for PostgreSQL (swap your local container for this)
- Airflow via MWAA (managed) or a small EC2 instance if MWAA cost is a concern
- IAM roles scoped tightly (least privilege) — mention this explicitly in your README, it signals
  security awareness

**Phase 10 — Visualization (Week 8–9)**
- Connect Power BI or Tableau to Postgres/RDS
- Build 4–6 dashboard visuals: patient volume trend, readmission rate by facility, claim denial
  rate by payer, average length of stay by department, lab turnaround time

**Phase 11 — Documentation & polish (Week 9–10)**
- Architecture diagram in the README
- Star vs snowflake schema diagrams
- Setup instructions (`docker-compose up`, `airflow dags trigger ...`)
- A "design decisions" section explaining tradeoffs (why Postgres not a real data lake, why dbt
  over raw SQL, why Pandas → Spark)

---

## 5. Suggested Folder Structure

```
healthcare-dw/
├── docker-compose.yml
├── README.md
├── data/
│   └── synthea_raw/
├── src/
│   ├── extract/
│   │   ├── extract_csv.py
│   │   ├── extract_postgres.py
│   │   └── extract_api.py
│   ├── quality/
│   │   └── ge_suites/
│   └── mock_api/
│       └── main.py            # FastAPI serving labs/claims
├── dbt_project/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   └── tests/
├── airflow/
│   └── dags/
│       └── healthcare_dw_dag.py
├── sql/
│   └── analytics_views.sql
└── docs/
    ├── architecture.png
    └── er_diagram.png
```

---

## 6. Sample KPIs for Your Dashboards

- Patient volume trend by month / facility
- Average length of stay by department
- 30-day readmission rate
- Claim denial rate by payer
- Revenue by department
- Lab turnaround time (order → result)

---

## 7. Why This Project Reads Well to Recruiters

- **Multi-source ingestion** (CSV + DB + API) — proves you can handle real-world messiness
- **SCD Type 2** — a genuine warehousing concept, not just "load a table"
- **Star vs snowflake side-by-side** — shows modeling judgment, not memorized rules
- **Pandas → PySpark** — shows you understand *when* to scale, not just that Spark exists
- **Data quality as a first-class step** — governance-mindedness
- **Airflow DAG with retries/alerts** — production-orchestration thinking
- **AWS deployment with least-privilege IAM** — cloud + security awareness
- **Synthetic data + explicit compliance note** — shows you understand healthcare data
  sensitivity even in a portfolio project

---

## 8. Next Steps

Pick one to start with:
1. Generate the Synthea dataset and stand up the three source systems (Phase 1–2)
2. Design the full star + snowflake schema in detail (table-by-table column lists)
3. Scaffold the repo structure and Docker Compose file
