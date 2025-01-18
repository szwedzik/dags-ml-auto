# FastAPI Model Deployment

## 📌 Wstęp
Ten projekt implementuje serwis REST API do przewidywania wyników modelu uczenia maszynowego. API jest konteneryzowane za pomocą Dockera i może być uruchomione zarówno lokalnie, jak i w kontenerze.

---

## 📂 Struktura katalogów
```
project-root/
│── app/
│   ├── main.py          # Serwis FastAPI
│   ├── model.pkl        # Wytrenowany model
│   ├── requirements.txt # Lista zależności
│── screenshots/         # Zrzuty ekranu
│   ├── docker-compose.png
│── docker-compose.yml   # Konfiguracja Docker Compose
│── Dockerfile           # Konfiguracja obrazu Docker
│── README.md            # Dokumentacja projektu
│── test_input.json      # Przykładowe dane wejściowe
```

---

## 🚀 Uruchomienie lokalne
### 1️⃣ Instalacja zależności
Najpierw zainstaluj wymagane biblioteki:
```sh
pip install -r app/requirements.txt
```

### 2️⃣ Uruchomienie API
```sh
uvicorn app.main:app --host 0.0.0.0 --port 5000
```

API będzie dostępne pod adresem: `http://127.0.0.1:5000`

---

## 🐳 Konteneryzacja (Docker)
### 1️⃣ Budowanie obrazu Docker
```sh
docker build -t fastapi-model .
```

### 2️⃣ Uruchomienie kontenera
```sh
docker run -p 5000:5000 fastapi-model
```

---

## 🔄 Uruchomienie z `docker-compose`
Aby uruchomić całość w kontenerze, użyj:
```sh
docker-compose up --build
```

---

## ☁️ Wdrożenie na Google Cloud Run
### 1️⃣ Zaloguj się do Google Cloud
```sh
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 2️⃣ Zbuduj i wypchnij obraz do Google Container Registry
```sh
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/fastapi-model
```

### 3️⃣ Wdrożenie na Google Cloud Run
```sh
gcloud run deploy fastapi-model \
    --image gcr.io/YOUR_PROJECT_ID/fastapi-model \
    --platform managed \
    --allow-unauthenticated \
    --region europe-west1
```

Po zakończeniu zobaczysz **URL**, np.:
```
https://fastapi-model-abcdefg-ue.a.run.app
```

Teraz możesz przetestować API:
```sh
curl -X POST "https://fastapi-model-abcdefg-ue.a.run.app/predict" \
     -H "Content-Type: application/json" \
     -d '{"feature1": 1.5, "feature2": 2.3, "feature3": 3.1}'
```

---

## 🔬 Testowanie API
Możesz przetestować API za pomocą `curl` lub Postman:
```sh
curl -X POST "http://127.0.0.1:5000/predict" \
     -H "Content-Type: application/json" \
     -d '{"feature1": 1.5, "feature2": 2.3, "feature3": 3.1}'
```

Przykładowa odpowiedź:
```json
{
    "prediction": [1]
}
```