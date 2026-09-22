from app.core.security import get_password_hash, verify_password, create_access_token


def test_password_hashing_and_verification():
    """Verify bcrypt password hashing and verification function."""
    password = "SecurePassword2026!"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False


def test_login_success(client, test_client_user):
    """Verify successful authentication returns JWT tokens."""
    payload = {
        "login": test_client_user.email,
        "password": "TestPass123!",
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["code"] == 200
    assert "access_token" in res_data["data"]
    assert "refresh_token" in res_data["data"]
    assert res_data["data"]["user_id"] == test_client_user.id


def test_login_wrong_password(client, test_client_user):
    """Verify invalid credentials return 400 error."""
    payload = {
        "login": test_client_user.email,
        "password": "IncorrectPassword123!",
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 400
    res_data = response.json()
    assert res_data["code"] == 400


def test_login_user_not_found(client):
    """Verify non-existent login returns 404 error."""
    payload = {
        "login": "nonexistent_user@example.com",
        "password": "AnyPassword123!",
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 404


def test_get_me_authenticated(client, client_auth_headers, test_client_user):
    """Verify /auth/me returns profile of currently authenticated user."""
    response = client.get("/api/v1/auth/me", headers=client_auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == test_client_user.id
    assert data["email"] == test_client_user.email
    assert data["role"] == "client"


def test_get_me_unauthorized(client):
    """Verify /auth/me requires valid Bearer token."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code in (401, 403)
