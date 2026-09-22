# Contributing to AutoRentGo

First off, thank you for considering contributing to **AutoRentGo**! 🎉

AutoRentGo is an open-source platform and extensible foundation for building rental marketplaces and asset-sharing systems (vehicles, heavy machinery, equipment, and marine transport). We welcome contributions from developers, designers, technical writers, and testers of all experience levels.

Please take a moment to review this document before submitting your contribution.

---

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please report any unacceptable behavior to [opensource@autorentgo.org](mailto:opensource@autorentgo.org).

---

## How to Set Up the Project Locally

### Prerequisites
- **Git** (v2.30+)
- **Python** (v3.11+)
- **Node.js** (v18+ or v20+) & **npm**
- **Docker** & **Docker Compose** (recommended for full-stack orchestration)

---

### Option A: Running with Docker (Recommended)

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/AutoRentGo.git
   cd AutoRentGo
   ```

2. **Copy the environment configuration:**
   ```bash
   cp .env.example .env
   ```

3. **Start the containers:**
   ```bash
   docker compose up --build
   ```

4. **Access the services:**
   - Frontend Application: [http://localhost:3000](http://localhost:3000)
   - Backend REST API: [http://localhost:8000/api/v1](http://localhost:8000/api/v1)
   - Interactive Swagger API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc Documentation: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### Option B: Local Native Development

#### 1. Backend Setup (FastAPI)
```bash
cd back

# Create and activate a virtual environment
python -m venv venv
# On Linux/macOS:
source venv/bin/activate
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Install runtime and development dependencies
pip install -r requirements-dev.txt

# Copy environment variables
cp ../.env.example .env

# Initialize database schema and seed default dictionaries (SQLite by default)
python -m app.init_db

# Run the development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Frontend Setup (Next.js)
```bash
cd ../front

# Install dependencies
npm install

# Run the Next.js development server
npm run dev
```

---

## How to Report an Issue

We use GitHub Issues to track bugs, improvements, and feature requests.

1. **Check existing issues:** Search our [Issue Tracker](https://github.com/Omarigato/AutoRentGo/issues) to ensure your issue or feature has not already been reported.
2. **Use our issue templates:**
   - For bugs: Select the **Bug Report** template and fill in reproduction steps, environment details, expected vs actual behavior.
   - For enhancements: Select the **Feature Request** template and describe the use case, architectural proposal, and developer benefit.
3. **Provide minimal, reproducible examples:** When reporting a backend error, please include request payloads, status codes, and relevant stack traces.

---

## How to Make a Pull Request (PR)

### 1. Branch Naming Strategy
Branch off from the `main` branch using descriptive branch prefixes:
- `feat/<feature-name>`: A new feature or capability.
- `fix/<bug-description>`: A bug fix.
- `docs/<doc-name>`: Documentation improvements.
- `refactor/<refactor-name>`: Code refactoring without changing functionality.
- `test/<test-name>`: Adding or improving automated tests.

Example:
```bash
git checkout -b feat/stripe-payment-provider
```

### 2. Commit Message Guidelines
We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
```
<type>(<scope>): <short summary>

[optional body]

[optional footer(s)]
```
- `feat(auth)`: Add OAuth2 GitHub login provider
- `fix(cars)`: Fix price-per-day filtering logic
- `docs(readme)`: Update Docker quickstart instructions
- `test(api)`: Add test coverage for rental booking lifecycle

### 3. Verification Before Submitting
Before opening a PR, ensure all checks pass locally:
```bash
# 1. Run backend unit and integration tests
pytest -v

# 2. Run Python linting checks
flake8 back/app back/tests

# 3. Run frontend linting
cd front && npm run lint
```

### 4. Submitting the PR
1. Push your branch to your fork:
   ```bash
   git push origin feat/your-feature-name
   ```
2. Open a Pull Request against `Omarigato/AutoRentGo`'s `main` branch.
3. Fill out the [Pull Request Template](.github/pull_request_template.md).
4. Link any related issues (e.g., `Closes #42`).
5. Ensure all GitHub Actions CI checks turn green. Maintainers will review your PR and provide constructive feedback.

---

## Development & Architecture Rules

1. **Preserve Backward Compatibility:** Do not break existing API contracts or schema migrations unless explicitly planned for a major version release.
2. **Type Hints & Schemas:**
   - All backend endpoints must define explicit Pydantic request and response schemas.
   - All SQLAlchemy models must use modern SQLAlchemy 2.0 `Mapped[...]` annotations.
   - All frontend components must use strict TypeScript types.
3. **Database Portability:** Code should run smoothly with PostgreSQL in production and SQLite in local/test environments. Avoid engine-specific raw SQL.
4. **Test-Driven Delivery:** Any new endpoint or significant bug fix must be accompanied by tests in `back/tests/`.
5. **No Secrets in Source:** Never commit private API keys, production tokens, or credentials. Use `.env` variables and verify `.gitignore`.

Thank you for helping make AutoRentGo the standard open-source platform for rental marketplaces!
