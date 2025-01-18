from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.expanduser("~/PycharmProjects/ASI/project")
DATA_PATH = f"{BASE_DIR}/processed_data/processed_data.csv"
VISUALIZATION_PATH = f"{BASE_DIR}/visualizations/pairplot.png"

os.makedirs(f"{BASE_DIR}/processed_data", exist_ok=True)
os.makedirs(f"{BASE_DIR}/visualizations", exist_ok=True)


def process_data():
    df = pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/AER/CollegeDistance.csv")

    df.drop_duplicates(inplace=True)
    df.fillna(df.median(numeric_only=True), inplace=True)

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()

    df.to_csv(DATA_PATH, index=False)

    sns.pairplot(df[numeric_cols])
    plt.savefig(VISUALIZATION_PATH)


with DAG(
        dag_id="data_processing_dag",
        start_date=datetime(2024, 1, 1),
        schedule_interval=None,
        catchup=False
) as dag:
    process_data_task = PythonOperator(
        task_id="process_data",
        python_callable=process_data
    )

    process_data_task
