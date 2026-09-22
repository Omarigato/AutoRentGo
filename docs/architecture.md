# AutoRentGo System Architecture & Design

Welcome to the technical architecture document for **AutoRentGo** — an open-source, modular platform and developer framework designed for building scalable vehicle, equipment, and asset rental marketplaces.

---

## 1. High-Level System Architecture

AutoRentGo employs a decoupled, multi-tier architecture designed for containerized deployment, high developer velocity, and horizontal scalability.

```mermaid
flowchart TD
    subgraph ClientLayer["Clients & Integrations"]
        WebClient["Desktop / Mobile Browser"]
        AdminClient["Operations & Fleet Admin Portal"]
        ThirdParty["External Systems / Webhooks"]
    end

    subgraph IngressLayer["Edge & Ingress Layer"]
        NextGateway["Next.js 14 App Router (Reverse Proxy & SSR)"]
    end

    subgraph ServiceLayer["Core Backend Services (FastAPI)"]
        API["FastAPI Application Core"]
        AuthModule["Authentication & RBAC"]
        CarCatalog["Asset Catalog & Filtering Engine"]
        AppMatcher["Rental Application Matching Service"]
        TaxonomyEngine["Multilingual Taxonomy & Dictionaries"]
        BillingModule["Subscriptions & Payments (TipTopPay)"]
        NotificationEngine["Async Notification Dispatcher"]
    end

    subgraph DataLayer["Persistence Layer"]
        PostgresDB[("PostgreSQL 16 / SQLite Engine")]
        MediaCDN["Cloudinary Media CDN"]
    end

    subgraph ExternalChannels["External Notification Channels"]
        TelegramBot["Telegram Admin Bot"]
        WhatsAppAPI["WhatsApp Cloud / Gateway"]
        SMTPGateway["SMTP Mail Server"]
    end

    WebClient --> NextGateway
    AdminClient --> NextGateway
    ThirdParty --> API

    NextGateway -->|/api/v1/*| API

    API --> AuthModule
    API --> CarCatalog
    API --> AppMatcher
    API --> TaxonomyEngine
    API --> BillingModule
    API --> NotificationEngine

    AuthModule --> PostgresDB
    CarCatalog --> PostgresDB
    AppMatcher --> PostgresDB
    TaxonomyEngine --> PostgresDB
    BillingModule --> PostgresDB

    CarCatalog -.-> MediaCDN
    NotificationEngine --> TelegramBot
    NotificationEngine --> WhatsAppAPI
    NotificationEngine --> SMTPGateway
```

---

## 2. Backend Architecture & Clean Modularity

The backend is built with **FastAPI** on Python 3.11+, leveraging modern asynchronous ASGI paradigms, strict Pydantic v2 schemas, and dependency injection.

### 2.1 Layered Responsibilities
- **`app/main.py`**: Application factory (`create_app`), global CORS middleware, language negotiation middleware (`Accept-Language` / `?lang=`), and OpenAPI schema orchestration.
- **`app/api/v1/`**: Modular API endpoints grouped by domain:
  - `auth`: JWT registration, OTP verification, credential login, user profile `/me`.
  - `cars`: Vehicle listings, multi-parameter filtering, media upload, lifecycle status (`ACTIVE`, `AWAIT`, `DRAFT`, `REJECT`).
  - `applications`: Customer rental requests and matching logic.
  - `dictionaries`: Hierarchical taxonomy (vehicle brands, models, categories, cities, transmissions, fuel types).
  - `subscriptions` & `admin`: Subscription tier management, fleet owner billing, and platform moderation.
- **`app/core/`**: Cross-cutting concerns including security (Bcrypt, JWT tokens), structured logging, i18n translation maps, standard response factories (`create_response`), and Pydantic configuration.
- **`app/services/`**: Isolated integration layers (Cloudinary media manager, WhatsApp gateway client, Telegram bot webhook, SMTP mail delivery, TipTopPay billing).

---

## 3. Database Layer & Domain Model

The persistence layer uses **SQLAlchemy 2.0** with strict type annotations (`Mapped[...]` and `mapped_column`) and supports both **PostgreSQL** in production and **SQLite** for rapid local development and automated testing.

### 3.1 Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    USERS ||--o| CLIENT_CARS : "owns fleet as"
    USERS ||--o{ CARS : "authors"
    USERS ||--o{ APPLICATIONS : "submits"
    USERS ||--o{ USER_LIKES : "favorites"
    USERS ||--o{ USER_EVENTS : "triggers"

    CLIENT_CARS ||--o{ OWNER_SUBSCRIPTIONS : "subscribes"
    SUBSCRIPTION_PLANS ||--o{ OWNER_SUBSCRIPTIONS : "defines"
    OWNER_SUBSCRIPTIONS ||--o{ PAYMENT_TRANSACTIONS : "bills"

    CARS ||--o{ IMAGES : "has photos"
    CARS ||--o{ USER_LIKES : "liked by"
    CARS ||--o{ REVIEWS : "receives"

    DICTIONARIES ||--o{ DICTIONARIES : "parent brand of model"
    DICTIONARIES ||--o{ DICTIONARY_TRANSLATIONS : "localized into"
    DICTIONARIES ||--o{ CARS : "categorizes (mark, model, city)"
    DICTIONARIES ||--o{ APPLICATIONS : "filters (city, category, mark)"

    APPLICATIONS ||--o{ APPLICATION_CARS : "matched to"
    CARS ||--o{ APPLICATION_CARS : "candidate for"

    USERS {
        int id PK
        string email UK
        string phone_number UK
        string password_hash
        string role "client | admin"
        int balance
        boolean is_active
    }

    CARS {
        int id PK
        string name
        int price_per_day
        int release_year
        int city_id FK
        int vehicle_mark_id FK
        int vehicle_model_id FK
        int author_id FK
        string status "ACTIVE | AWAIT | DRAFT | REJECT"
    }

    APPLICATIONS {
        int id PK
        int user_id FK
        int city_id FK
        int category_id FK
        int vehicle_mark_id FK
        string status "ACTIVE | COMPLETED | REJECTED"
        datetime requested_at
    }

    DICTIONARIES {
        int id PK
        string code
        string type "CITY | MARKA | MODEL | CATEGORY"
        int parent_id FK
        boolean is_active
    }
```

---

## 4. API Request & Data Flow

Every inbound HTTP request flows through a unified request pipeline ensuring internationalization, authentication, and standard JSON response envelopes.

```mermaid
sequenceDiagram
    autonumber
    actor Client as Client / Web App
    participant GW as Next.js Gateway
    participant MW as Lang & CORS Middleware
    participant Auth as Security Dependency (get_current_user)
    participant Route as Route Handler (e.g. /cars)
    participant DB as SQLAlchemy Session (get_db)
    participant Out as create_response Envelope

    Client->>GW: GET /api/v1/cars?city_id=1 [Accept-Language: en]
    GW->>MW: Forward to FastAPI ASGI App
    MW->>MW: Parse lang header -> request.state.lang = "en"
    MW->>Route: Execute handler list_cars(...)
    Route->>DB: Query cars with filters & pagination
    DB-->>Route: Return ORM models
    Route->>Out: create_response(data, lang="en")
    Out-->>Client: 200 OK {"code": 200, "data": {...}, "message": {...}}
```

---

## 5. Rental Application & Matching Workflow

The platform's standout functional core is its **automated matching engine**: when a customer requires equipment or a vehicle, owners with compatible listings are automatically matched and alerted.

```mermaid
flowchart TD
    A[Customer Submits Rental Request] --> B[Validate City, Category & Dates]
    B --> C[(Save Application with Status ACTIVE)]
    C --> D[Query Matching Active Listings in Same City & Category]
    D --> E[(Link Application to Candidates in application_cars)]
    E --> F{Notify Fleet Owners}
    F -->|WhatsApp Gateway| G[Send WhatsApp Alert to Owner]
    F -->|SMTP Service| H[Send Email Notification to Owner]
    F -->|Telegram Bot| I[Send Push Alert to Admin Channel]
    E --> J[Owner Views Matching Request in Dashboard]
    J --> K[Owner Proposes Vehicle or Accepts Request]
    K --> L[Customer Completes Booking]
```

---

## 6. Authentication & Security Model

- **Stateless Tokens**: Signed using HMAC SHA-256 (`HS256`) with a configurable expiration window.
- **Credential Storage**: Bcrypt cryptographic hashing via Passlib with automatic salt generation.
- **Two-Factor / Passwordless OTP Verification**: Time-bounded one-time passwords (`otp_verifications`) expiring in 10 minutes for phone and email identity validation.
- **Role-Based Access Control (RBAC)**: Distinct authorization scopes (`client`, `owner`, `admin`) enforced using FastAPI dependencies (`get_current_user`, `get_current_owner`).

---

## 7. Future Scalability & Extensibility Roadmap

AutoRentGo is architected as an extensible foundation ready for high concurrency:

1. **Read/Write Persistence Splitting**:
   - Primary PostgreSQL instance for ACID transaction writes.
   - Read replicas for catalog searches and dictionary queries.
2. **Caching Tier (Redis)**:
   - Redis caching for frequently queried dictionary taxonomies and top vehicle listings.
3. **Asynchronous Worker Queues**:
   - Transitioning from FastAPI in-process `BackgroundTasks` to Celery / ARQ with Redis / RabbitMQ brokers for high-volume notification bursts.
4. **Storage Abstraction (S3 / MinIO / Cloudflare R2)**:
   - Pluggable storage backend interface allowing self-hosted S3-compatible object stores alongside Cloudinary.
5. **AI Assistant Integration (Roadmap v1.1)**:
   - Natural language vehicle search, automated condition analysis from photos, and smart pricing recommendations.
