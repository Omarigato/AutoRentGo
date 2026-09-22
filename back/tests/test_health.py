def test_openapi_docs_available(client):
    """Verify Swagger UI documentation is accessible at /docs."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower() or "html" in response.headers.get("content-type", "")


def test_redoc_available(client):
    """Verify ReDoc documentation is accessible at /redoc."""
    response = client.get("/redoc")
    assert response.status_code == 200
    assert "redoc" in response.text.lower() or "html" in response.headers.get("content-type", "")


def test_openapi_schema(client):
    """Verify OpenAPI JSON schema specification is generated correctly."""
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert "paths" in schema
    assert schema["info"]["title"] == "AutoRentGo"
