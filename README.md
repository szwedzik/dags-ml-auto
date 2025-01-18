# 📌 Automatyzacja Budowy Modelu ML w Airflow

## 📌 Opis projektu

Ten projekt implementuje zautomatyzowany pipeline w **Apache Airflow**, który przetwarza dane i buduje model ML. Składa się z dwóch **DAG-ów**:

1. **data_processing_dag** – Pobiera i przetwarza dane wejściowe.
2. **model_training_dag** – Trenuje model ML i zapisuje wyniki ewaluacji.

Każdy z DAG-ów działa niezależnie i może być uruchamiany osobno. Model wykorzystuje **TPOT** do automatycznego wyboru najlepszej architektury ML.

---

## 📂 Struktura katalogów

```
project/
├── dags/
│   ├── data_processing_dag.py
│   ├── model_training_dag.py
├── processed_data/
│   ├── processed_data.csv
├── models/
│   ├── model.pkl
├── reports/
│   ├── evaluation_report.txt
├── screenshots/
│   ├── pairplot.png
│   ├── dags.png
```

---

## 🚀 **DAG 1: Przetwarzanie danych** (data_processing_dag)

**Opis:**
- Pobiera dane wejściowe z zewnętrznego źródła.
- Przeprowadza czyszczenie, usuwanie duplikatów i skalowanie danych.
- Generuje wykresy eksploracyjne.
- Zapisuje przetworzone dane w `processed_data/processed_data.csv`.

📌 **Podgląd wykresu korelacji:**  
![Pairplot](visualizations/pairplot.png)

🔗 **Kod DAG-a:** [data_processing_dag.py](dags/data_processing_dag.py)

---

## 🎯 **DAG 2: Trenowanie Modelu ML** (model_training_dag)

**Opis:**
- Wczytuje dane przetworzone z `processed_data/processed_data.csv`.
- Podzielone dane na zbiór **treningowy (70%)** i **testowy (30%)**.
- Automatyczny wybór modelu ML przy użyciu **TPOT**.
- Trening modelu i zapis w `models/model.pkl`.
- Ewaluacja modelu (MAE) i zapis raportu w `reports/evaluation_report.txt`.

📌 **Wynik ewaluacji modelu:**  
```
Mean Absolute Error (MAE): 0.7091
```
🔗 **Kod DAG-a:** [model_training_dag.py](dags/model_training_dag.py)
🔗 **Raport ewaluacji:** [evaluation_report.txt](reports/evaluation_report.txt)

---

## 🔄 **Jak uruchomić DAG-i?**

1️⃣ **Uruchom Airflow**:
```bash
airflow standalone
```

2️⃣ **Sprawdź dostępne DAG-i**:
```bash
airflow dags list
```

3️⃣ **Ręczne uruchomienie DAG-a**:
```bash
airflow dags trigger data_processing_dag
airflow dags trigger model_training_dag
```

4️⃣ **Monitorowanie DAG-ów** (interfejs UI):
- Otwórz przeglądarkę i przejdź do [http://localhost:8080](http://localhost:8080)
- Zaloguj się (**admin/admin**)
- Uruchom DAG-i z interfejsu użytkownika

📌 **Podgląd interfejsu Airflow:**  
![DAGs](dags.png)

---

## ✅ **Testowanie i Walidacja**
- Oba DAG-i zostały **przetestowane lokalnie** i działają poprawnie.
- Wyniki modelu i przetworzone dane zapisano w odpowiednich katalogach.
- Raport ewaluacyjny wskazuje **MAE: 0.7091**.

🔗 **Główne pliki projektu:**
- [data_processing_dag.py](dags/data_processing_dag.py)
- [model_training_dag.py](dags/model_training_dag.py)
- [evaluation_report.txt](reports/evaluation_report.txt)
- [pairplot.png](screenshots/pairplot.png)
- [dags.png](screenshots/dags.png)

