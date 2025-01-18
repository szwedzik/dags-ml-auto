import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "TWÓJ_SENDGRID_API_KEY")
FROM_EMAIL = "airflow@example.com"
TO_EMAIL = "admin@example.com"

def send_alert_email(accuracy, test_results):
    """Wysyłanie alertu e-mail przez SendGrid API"""
    test_status = "❌ Niektóre testy nie przeszły!" if not test_results else "✅ Wszystkie testy zaliczone."
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAIL,
        subject="🚨 Airflow: Model Alert!",
        html_content=f"""
        <h2>📌 Ostrzeżenie: Spadek jakości modelu lub błędne testy!</h2>
        <p>🔹 Model: model.pkl</p>
        <p>🔹 Aktualna jakość: <b>{accuracy:.2%}</b></p>
        <p>🔹 Krytyczny próg: <b>80%</b></p>
        <p>🔹 Status testów: {test_status}</p>
        <p>📧 Powiadomienie wysłane automatycznie przez Airflow.</p>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"📧 Wysłano powiadomienie mailowe. Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Błąd podczas wysyłania maila: {e}")
