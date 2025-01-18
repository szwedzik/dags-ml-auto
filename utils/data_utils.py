import pandas as pd
import joblib
import subprocess
from sklearn.metrics import accuracy_score
from utils.email_utils import send_alert_email

MODEL_PATH = "models/model.pkl"
DATA_PATH = "data/new_data.csv"
THRESHOLD = 0.80
TEST_PATH = "tests"

def validate_model():
    """Walidacja modelu ML"""
    model = joblib.load(MODEL_PATH)
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["target"])
    y = df["target"]

    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)

    test_results = run_tests()

    if accuracy < THRESHOLD or test_results is False:
        send_alert_email(accuracy, test_results)

    with open("reports/validation_report.txt", "w") as f:
        f.write(f"Model Accuracy: {accuracy:.2%}\n")

def run_tests():
    """Uruchamianie testów"""
    result = subprocess.run(["pytest", TEST_PATH], capture_output=True, text=True)
    return result.returncode == 0
