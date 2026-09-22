def test_list_dictionaries(client, seed_dictionaries):
    """Verify listing all active dictionary elements."""
    response = client.get("/api/v1/dictionaries")
    assert response.status_code == 200
    res = response.json()
    assert res["code"] == 200
    assert len(res["data"]) >= 4


def test_filter_dictionaries_by_type(client, seed_dictionaries):
    """Verify filtering dictionary elements by type (e.g. CITY)."""
    response = client.get("/api/v1/dictionaries?type=CITY")
    assert response.status_code == 200
    items = response.json()["data"]
    assert len(items) == 1
    assert items[0]["code"] == "ALA"


def test_dictionary_translations_en(client, seed_dictionaries):
    """Verify dictionary translation in English via Accept-Language header."""
    headers = {"Accept-Language": "en"}
    response = client.get("/api/v1/dictionaries?type=CITY", headers=headers)
    assert response.status_code == 200
    items = response.json()["data"]
    assert items[0]["name"] == "Almaty"


def test_dictionary_translations_ru(client, seed_dictionaries):
    """Verify dictionary translation in Russian via Accept-Language header."""
    headers = {"Accept-Language": "ru"}
    response = client.get("/api/v1/dictionaries?type=CITY", headers=headers)
    assert response.status_code == 200
    items = response.json()["data"]
    assert items[0]["name"] == "Алматы"


def test_hierarchical_models_by_mark(client, seed_dictionaries):
    """Verify nested dictionary lookup (models linked to parent brand)."""
    mark_id = seed_dictionaries["mark"].id
    response = client.get(f"/api/v1/dictionaries?type=MODEL&parent_id={mark_id}")
    assert response.status_code == 200
    items = response.json()["data"]
    assert len(items) == 1
    assert items[0]["code"] == "CAMRY"
