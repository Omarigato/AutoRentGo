# AutoRentGo Developer Demo & Quick Start Guide

This guide walks you through launching the **AutoRentGo** platform and interacting with the core REST API endpoints using `curl` or HTTP clients like Postman / Insomnia.

---

## 1. How to Launch the Project

### Option A: Using Docker Compose (Single Command)

```bash
# 1. Clone repository
git clone https://github.com/Omarigato/AutoRentGo.git
cd AutoRentGo

# 2. Copy environment variables
cp .env.example .env

# 3. Start PostgreSQL, Backend, and Frontend containers
docker compose up --build
```

The services will become available at:
- **Frontend App**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000/api/v1](http://localhost:8000/api/v1)
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Technical Docs**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### Option B: Local Native Launch (Lightweight SQLite Mode)

```bash
# Backend
cd back
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python -m app.init_db
uvicorn app.main:app --reload --port 8000

# Frontend (in another terminal)
cd front
npm install
npm run dev
```

---

## 2. Interactive API Demo Scenarios

### Scenario 1: Authentication & JWT Token Issuance

#### Request:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "login": "admin@autorentgo.kz",
    "password": "adminautorentgo2026@@!"
  }'
```

#### Response (`200 OK`):
```json
{
  "code": 200,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user_id": 1
  },
  "message": {
    "en": "Success",
    "ru": "Успешно",
    "kk": "Сәтті"
  }
}
```

---

### Scenario 2: Querying the Multilingual Taxonomy & Dictionaries

AutoRentGo features a dynamic hierarchical dictionary system. Querying with language negotiation returns translated labels.

#### Request:
```bash
curl -X GET "http://localhost:8000/api/v1/dictionaries?type=CITY" \
  -H "Accept-Language: en"
```

#### Response (`200 OK`):
```json
{
  "code": 200,
  "data": [
    {
      "id": 1,
      "name": "Almaty",
      "code": "ALA",
      "icon": "map-pin",
      "color": "blue",
      "parent_id": null,
      "display_order": 1
    },
    {
      "id": 2,
      "name": "Astana",
      "code": "AST",
      "icon": "map-pin",
      "color": "blue",
      "parent_id": null,
      "display_order": 2
    }
  ],
  "message": {
    "en": "Success",
    "ru": "Успешно",
    "kk": "Сәтті"
  }
}
```

---

### Scenario 3: Querying the Vehicle & Equipment Catalog

Filter vehicles by category, brand, model, city, and sort order (`cheap`, `new`).

#### Request:
```bash
curl -X GET "http://localhost:8000/api/v1/cars?city_id=1&sort=new&limit=2" \
  -H "Accept-Language: en"
```

#### Response (`200 OK`):
```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "id": 1,
        "name": "Toyota Camry 70 Luxe",
        "release_year": 2022,
        "price_per_day": 35000,
        "views_count": 142,
        "is_top": true,
        "mark": "Toyota",
        "model": "Camry",
        "category_name": "Passenger Cars",
        "car_class": "Business",
        "color": "White",
        "transmission": "Automatic",
        "city": "Almaty",
        "images": [
          {
            "url": "https://res.cloudinary.com/demo/image/upload/v1/cars/camry.jpg"
          }
        ],
        "author": {
          "name": "Premier Fleet Ltd",
          "address": "Dostyk Ave 105, Almaty"
        }
      }
    ],
    "total": 1
  },
  "message": {
    "en": "Success",
    "ru": "Успешно",
    "kk": "Сәтті"
  }
}
```

---

### Scenario 4: Submitting a Rental Booking Request (Application)

Customers can post requests when they require equipment, commercial vehicles, or passenger fleets for specified dates.

#### Request:
```bash
curl -X POST "http://localhost:8000/api/v1/applications" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -F "city_id=1" \
  -F "category_id=1" \
  -F "vehicle_mark_id=3" \
  -F "message=Need a comfortable executive sedan for airport transfer from Oct 1 to Oct 4."
```

#### Response (`200 OK`):
```json
{
  "code": 200,
  "data": {
    "id": 12,
    "user_id": 4,
    "city_id": 1,
    "category_id": 1,
    "vehicle_mark_id": 3,
    "vehicle_model_id": null,
    "message": "Need a comfortable executive sedan for airport transfer from Oct 1 to Oct 4.",
    "status": "ACTIVE",
    "views_count": 0,
    "create_date": "2026-09-22T12:30:00",
    "city_name": "Almaty",
    "matching_cars_count": 3
  },
  "message": "Заявка создана"
}
```

---

## 3. Running Automated Tests

AutoRentGo ships with an automated test suite verifying auth, permissions, API documentation, and catalog filtering:

```bash
# From repository root or back/
pytest -v
```

Expected output:
```text
============================= test session starts =============================
collected 21 items

back/tests/test_applications.py ...                                      [ 14%]
back/tests/test_auth.py ......                                           [ 42%]
back/tests/test_cars.py ....                                             [ 61%]
back/tests/test_dictionaries.py .....                                    [ 85%]
back/tests/test_health.py ...                                            [100%]

============================= 21 passed in 5.44s ==============================
```
