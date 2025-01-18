from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from tpot import TPOTClassifier
import pickle

# Ustawienie ścieżek
BASE_DIR = os.path.expanduser("~/PycharmProjects/ASI/project")
DATA_PATH = f"{BASE_DIR}/processed_data/processed_data.csv"
MODEL_DIR = f"{BASE_DIR}/models"
MODEL_PATH = f"{MODEL_DIR}/model.pkl"
REPORT_DIR = f"{BASE_DIR}/reports"
REPORT_PATH = f"{REPORT_DIR}/evaluation_report.txt"

# Tworzenie katalogów, jeśli nie istnieją
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


def train_model():
    """Trenuje model ML i zapisuje go do pliku oraz generuje raport ewaluacyjny."""

    try:
        print(f"📂 Sprawdzanie, czy plik istnieje: {DATA_PATH}")
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"❌ Plik {DATA_PATH} nie istnieje! Sprawdź DAG przetwarzania danych.")

        # Wczytanie danych
        df = pd.read_csv(DATA_PATH)
        print("✅ Dane wczytane pomyślnie.")

        # Sprawdzenie czy plik zawiera kolumnę docelową
        target_column = "education"  # Dostosuj do danych
        if target_column not in df.columns:
            raise ValueError(f"❌ Brak kolumny docelowej '{target_column}' w zbiorze danych!")

        X = df.drop(columns=[target_column])
        y = df[target_column]

        # Podział na zbiór treningowy i testowy
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        print(f"📊 Dane podzielone na zbiór treningowy ({len(X_train)}) i testowy ({len(X_test)}).")

        # Automatyczny wybór modelu przy użyciu TPOT
        print("🚀 Rozpoczynam trenowanie modelu...")
        tpot = TPOTClassifier(generations=5, population_size=20, verbosity=2, random_state=42)
        tpot.fit(X_train, y_train)
        print("✅ Model został wytrenowany.")

        # Predykcja i ewaluacja modelu
        y_pred = tpot.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"📈 Wynik modelu (Accuracy): {accuracy:.4f}")

        # Zapisanie modelu do pliku
        print(f"💾 Zapisywanie modelu do {MODEL_PATH}...")
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(tpot.fitted_pipeline_, f)
        print("✅ Model zapisany pomyślnie.")

        # Zapisanie raportu ewaluacyjnego
        print(f"📝 Zapisywanie raportu do {REPORT_PATH}...")
        with open(REPORT_PATH, "w") as f:
            f.write(f"Accuracy: {accuracy:.4f}\n")
        print("✅ Raport zapisany pomyślnie.")

    except Exception as e:
        print(f"❌ Błąd w trakcie trenowania modelu: {e}")
        raise e


# Definicja DAG-a
with DAG(
        dag_id="model_training_dag",
        start_date=datetime(2024, 1, 1),
        schedule=None,
        catchup=False
) as dag:
    train_model_task = PythonOperator(
        task_id="train_model",
        python_callable=train_model
    )

    train_model_task
