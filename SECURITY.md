# Security Policy

The AutoRentGo community and maintainers take the security of our open-source codebase and the deployments built upon it very seriously.

---

## Supported Versions

Only the latest active development branch and release versions receive security patches and updates:

| Version | Supported          | Security Fixes |
| ------- | ------------------ | -------------- |
| 0.1.x   | :white_check_mark: | Active         |
| < 0.1.0 | :x:                | Unsupported    |
| main    | :white_check_mark: | Continuous     |

---

## Reporting a Vulnerability

**Please DO NOT report security vulnerabilities through public GitHub issues, discussions, or pull requests.**

If you discover or suspect a security vulnerability in AutoRentGo:

1. **Email our Security Team:** Send a report directly to **security@autorentgo.org**.
2. **Information to Include:**
   - Detailed description of the vulnerability.
   - Component(s) affected (`back`, `front`, Docker configuration, authentication, or API endpoints).
   - Step-by-step instructions or Proof of Concept (PoC) to reproduce the vulnerability.
   - Any potential impact, attack vectors, or mitigation strategies you have identified.
   - Your preferred name/handle if you wish to be credited in the security advisory.

---

## Response Timeline & SLA

- **Initial Acknowledgement:** Within **48 hours** of receiving your report.
- **Vulnerability Assessment:** Within **5 business days**, detailing severity and reproduction confirmation.
- **Remediation & Patching:** High-severity issues are prioritized with a target patch release within **14 business days**.
- **Coordinated Public Disclosure:** Once a fix is verified and released, a coordinated public security advisory will be published with credit to the reporter.

---

## Production Security Best Practices

When deploying AutoRentGo to production environments, always ensure:

1. **Secret Key Randomization:** Generate a cryptographically strong `SECRET_KEY` (minimum 32 bytes) for JWT signing and never use default placeholders.
2. **HTTPS & TLS:** Always enforce HTTPS for both the frontend and backend API using a reverse proxy (e.g. Nginx, Traefik, or Caddy).
3. **CORS Restrictions:** Restrict `CORS_ORIGINS` to trusted domains rather than using `*`.
4. **Database Isolation:** Run PostgreSQL in a dedicated internal network without exposing database ports to the public internet.
5. **Least Privilege Principles:** Limit container capabilities and avoid running Docker workloads as root.
