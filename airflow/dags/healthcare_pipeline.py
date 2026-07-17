from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}
with DAG(
    dag_id="healthcare_pipeline",
    start_date=datetime(2026, 7, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
) as dag:

    extract_api = BashOperator(
        task_id="extract_api",
        bash_command="""
        python /opt/airflow/src/extract/extract_api.py
        """
    )

    extract_csv = BashOperator(
        task_id="extract_csv",
        bash_command="""
        python /opt/airflow/src/extract/extract_csv.py
        """
    )

    extract_postgres = BashOperator(
        task_id="extract_postgres",
        bash_command="""
        python /opt/airflow/src/extract/extract_postgres.py
        """
    )

    load_raw_to_warehouse = BashOperator(
        task_id="load_raw_to_warehouse",
        bash_command="""
        python /opt/airflow/src/extract/load_raw_to_warehouse.py
        """
    )

    task_validate_all = BashOperator(
        task_id="validate_data",
        bash_command="""
        python /opt/airflow/src/quality/validate_all.py
        """
    )
    task_dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/dbt_project && dbt run",
    )

    [extract_api, extract_csv, extract_postgres] >> task_validate_all >> load_raw_to_warehouse >> task_dbt_run