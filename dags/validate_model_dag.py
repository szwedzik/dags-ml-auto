from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from utils.data_utils import validate_model

with DAG(
    dag_id="validate_model_dag",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False
) as dag:

    validate_task = PythonOperator(
        task_id="validate_model",
        python_callable=validate_model
    )

    validate_task
