from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from tpot import TPOTClassifier
import pickle
import os

BASE_DIR = os.path.expanduser("~/PycharmProjects/ASI/project")
DATA_PATH = f"{BASE_DIR}/processed_data/processed_data.csv"
MODEL_PATH = f"{BASE_DIR}/models/model.pkl"
REPORT_PATH = f"{BASE_DIR}/reports/evaluation_report.txt"

os.makedirs(f"{BASE_DIR}/models", exist_ok=True)
os.makedirs(f"{BASE_DIR}/reports", exist_ok=True)


def train_model():
    df = pd.read_csv(DATA_PATH)

    target_column = "education"
    X = df.drop(target_column, axis=1)
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    tpot = TPOTClassifier(generations=5, population_size=20, verbosity=2, random_state=42)
    tpot.fit(X_train, y_train)

    y_pred = tpot.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(tpot.fitted_pipeline_, f)

    with open(REPORT_PATH, "w") as f:
        f.write(f"Accuracy: {accuracy:.4f}")


with DAG(
        dag_id="model_training_dag",
        start_date=datetime(2024, 1, 1),
        schedule_interval=None,
        catchup=False
) as dag:
    train_model_task = PythonOperator(
        task_id="train_model",
        python_callable=train_model
    )

    train_model_task
