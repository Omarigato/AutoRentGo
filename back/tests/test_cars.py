from app.models import Car


def test_list_cars_empty(client):
    """Verify car listing returns empty results when no active listings exist."""
    response = client.get("/api/v1/cars")
    assert response.status_code == 200
    res = response.json()
    assert res["code"] == 200
    assert res["data"]["items"] == []
    assert res["data"]["total"] == 0


def test_list_and_get_car(client, db_session, test_owner_user, seed_dictionaries):
    """Verify creating an active car and querying it via public endpoints."""
    city = seed_dictionaries["city"]
    category = seed_dictionaries["category"]
    mark = seed_dictionaries["mark"]
    model = seed_dictionaries["model"]

    # Seed an active vehicle
    car = Car(
        name="Toyota Camry 70 Luxe",
        description="Excellent business sedan for daily or long-term rental.",
        price_per_day=35000,
        release_year=2022,
        vehicle_mark_id=mark.id,
        vehicle_model_id=model.id,
        category_id=category.id,
        city_id=city.id,
        author_id=test_owner_user.id,
        status="ACTIVE",
    )
    db_session.add(car)
    db_session.commit()
    db_session.refresh(car)

    # 1. Test listing
    response = client.get("/api/v1/cars")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total"] == 1
    assert data["items"][0]["name"] == "Toyota Camry 70 Luxe"
    assert data["items"][0]["price_per_day"] == 35000

    # 2. Test get by ID
    detail_res = client.get(f"/api/v1/cars/{car.id}")
    assert detail_res.status_code == 200
    detail = detail_res.json()["data"]
    assert detail["id"] == car.id
    assert detail["name"] == "Toyota Camry 70 Luxe"
    assert detail["status"] == "ACTIVE"


def test_get_car_not_found(client):
    """Verify requesting non-existent car returns 404."""
    response = client.get("/api/v1/cars/999999")
    assert response.status_code == 404


def test_filter_cars_by_mark(client, db_session, test_owner_user, seed_dictionaries):
    """Verify car list filtering by marka_id."""
    city = seed_dictionaries["city"]
    mark = seed_dictionaries["mark"]

    car = Car(
        name="Toyota Land Cruiser",
        price_per_day=75000,
        release_year=2023,
        vehicle_mark_id=mark.id,
        city_id=city.id,
        author_id=test_owner_user.id,
        status="ACTIVE",
    )
    db_session.add(car)
    db_session.commit()

    # Filter with matching mark
    res_match = client.get(f"/api/v1/cars?marka_id={mark.id}")
    assert res_match.status_code == 200
    assert res_match.json()["data"]["total"] == 1

    # Filter with non-matching mark
    res_no_match = client.get("/api/v1/cars?marka_id=9999")
    assert res_no_match.status_code == 200
    assert res_no_match.json()["data"]["total"] == 0
