from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from train_model import train_model

with DAG(
    dag_id="train_model_dag",
    schedule_interval="@weekly",
    start_date=days_ago(1),
    catchup=False
) as dag:

    train_task = PythonOperator(
        task_id="train_model",
        python_callable=train_model
    )

    train_task
