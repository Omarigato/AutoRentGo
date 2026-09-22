def test_list_my_applications_empty(client, client_auth_headers):
    """Verify empty list when authenticated user has no rental applications."""
    response = client.get("/api/v1/applications", headers=client_auth_headers)
    assert response.status_code == 200
    res = response.json()
    assert res["code"] == 200
    assert res["data"] == []


def test_create_application_and_list(client, client_auth_headers, seed_dictionaries):
    """Verify creating a rental application and querying it via /applications."""
    city = seed_dictionaries["city"]
    category = seed_dictionaries["category"]
    mark = seed_dictionaries["mark"]

    form_data = {
        "city_id": str(city.id),
        "category_id": str(category.id),
        "vehicle_mark_id": str(mark.id),
        "message": "Looking for a business sedan for 3 days.",
    }

    # Create application (sent as multipart/form-data)
    create_res = client.post("/api/v1/applications", data=form_data, headers=client_auth_headers)
    assert create_res.status_code == 200
    res_data = create_res.json()
    assert res_data["code"] == 200
    assert res_data["data"]["city_id"] == city.id
    assert res_data["data"]["status"] == "ACTIVE"

    # Query applications
    list_res = client.get("/api/v1/applications", headers=client_auth_headers)
    assert list_res.status_code == 200
    apps = list_res.json()["data"]
    assert len(apps) == 1
    assert apps[0]["message"] == "Looking for a business sedan for 3 days."


def test_create_duplicate_application_fails(client, client_auth_headers, seed_dictionaries):
    """Verify duplicate active application creation is rejected with 400."""
    city = seed_dictionaries["city"]

    form_data = {
        "city_id": str(city.id),
        "message": "Duplicate test message.",
    }

    # First creation
    res1 = client.post("/api/v1/applications", data=form_data, headers=client_auth_headers)
    assert res1.status_code == 200

    # Second creation with identical parameters
    res2 = client.post("/api/v1/applications", data=form_data, headers=client_auth_headers)
    assert res2.status_code == 400
    assert res2.json()["code"] == 400
