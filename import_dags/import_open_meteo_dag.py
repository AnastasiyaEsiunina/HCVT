from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from import_open_meteo.etl_tasks import run

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 2, 10),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "weather_etl",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
)

load_task = PythonOperator(
    task_id="load_task",
    python_callable=run,
    op_kwargs={"task": "load", "date_from": "{{ ts }}"},
    dag=dag,
)

transform_task = PythonOperator(
    task_id="transform_task",
    python_callable=run,
    op_kwargs={"task": "transform", "date_from": "{{ ts }}"},
    dag=dag,
)

extract_task = PythonOperator(
    task_id="extract_task",
    python_callable=run,
    op_kwargs={"task": "extract", "date_from": "{{ ts }}"},
    dag=dag,
)

extract_task >> transform_task >> load_task
