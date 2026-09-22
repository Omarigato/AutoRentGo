# Changelog

All notable changes to the **AutoRentGo** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-09-22

### Added
- **Open Source Foundation & Architecture**:
  - Open source release under the MIT License.
  - Multi-tier architecture blueprint with Next.js 14 frontend, FastAPI backend, and PostgreSQL/SQLite persistence.
  - Comprehensive contributing guidelines (`CONTRIBUTING.md`), Code of Conduct (`CODE_OF_CONDUCT.md`), and Security Policy (`SECURITY.md`).
- **Backend Core Services (FastAPI)**:
  - Multi-asset catalog management (passenger vehicles, commercial trucks, heavy machinery, equipment, water transport).
  - Dynamic multilingual taxonomy engine with real-time translation support (Russian, English, Kazakh) and hierarchical relationships (Brand -> Model).
  - Customer rental application (request) system with automated matching against active fleet listings.
  - Authentication engine with JWT access/refresh tokens, Bcrypt password encryption, and phone/email OTP verification.
  - Fleet owner subscription tiers and payment transaction tracking.
  - Cloudinary media CDN integration for vehicle photos and user avatars.
  - Async multi-channel notification engine (Telegram admin bot, WhatsApp Gateway API, and SMTP email templating).
- **Frontend Application (Next.js 14)**:
  - App Router architecture with client and server components.
  - Responsive catalog with multi-facet filters (brand, model, price, transmission, fuel type, condition, city).
  - Client portal for rental application tracking and favorites.
  - Fleet management admin portal for vehicle moderation, taxonomy editing, and analytics.
  - Dark and light theme support via Tailwind CSS and `next-themes`.
- **Developer Experience & Tooling**:
  - Full-stack Docker Compose orchestration with PostgreSQL 16, backend healthchecks, and frontend dependency ordering.
  - Automated test suite powered by `pytest` with 21 unit and integration tests passing out of the box with zero external dependencies.
  - Automatic fallback to SQLite (`sqlite:///./autorentgo.db`) for rapid local setup without PostgreSQL.
  - GitHub Actions CI workflow (`.github/workflows/test.yml`) running linting and test suites on every pull request and push.
  - Structured GitHub Issue and Pull Request templates.

---

## [Planned Roadmap]

### [1.0.0] - Production Hardening & Ecosystem
- **Payment Providers**: Native Stripe, PayPal, and regional payment gateway integrations with webhook handlers.
- **Real-time WebSockets**: Live status updates for booking requests and owner proposals.
- **Contract & Escrow Generation**: Automated PDF rental agreement generator with digital signing.
- **Advanced Fleet Telematics**: Support for GPS tracking and vehicle availability calendars.

### [1.1.0] - AI & Autonomous Operations
- **AI Assistant**: Conversational AI assistant for natural language vehicle search and booking.
- **Smart Vehicle Valuation**: Machine learning-based pricing recommendations for fleet owners based on seasonal demand.
- **Automated Vehicle Condition Inspection**: Computer vision analysis of uploaded vehicle damage photos.
