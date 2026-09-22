import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.core.security import get_password_hash, create_access_token
from app.db.session import Base, get_db
from app.main import create_app
from app.models import (
    User,
    CarOwner,
    Car,
    Dictionary,
    DictionaryTranslation,
    AppSetting,
    Application,
)

# In-memory SQLite database configured with StaticPool for thread-safe test execution
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create all tables once for the test session."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    """Provide a transactional database session for each test function."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI TestClient with overridden get_db dependency."""
    app = create_app()

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def seed_dictionaries(db_session):
    """Seed essential dictionary data (cities, marks, models, categories) for testing."""
    # City
    city = Dictionary(code="ALA", name="Алматы", type="CITY", is_active=True, display_order=1)
    db_session.add(city)
    db_session.flush()
    db_session.add(DictionaryTranslation(dictionary_id=city.id, lang="en", name="Almaty"))
    db_session.add(DictionaryTranslation(dictionary_id=city.id, lang="ru", name="Алматы"))
    db_session.add(DictionaryTranslation(dictionary_id=city.id, lang="kk", name="Алматы"))

    # Category
    category = Dictionary(code="PASSENGER", name="Легковые", type="CATEGORY", is_active=True, display_order=1)
    db_session.add(category)
    db_session.flush()
    db_session.add(DictionaryTranslation(dictionary_id=category.id, lang="en", name="Passenger Cars"))
    db_session.add(DictionaryTranslation(dictionary_id=category.id, lang="ru", name="Легковые"))

    # Mark
    mark = Dictionary(code="TOYOTA", name="Toyota", type="MARKA", is_active=True, display_order=1)
    db_session.add(mark)
    db_session.flush()

    # Model
    model = Dictionary(code="CAMRY", name="Camry", type="MODEL", parent_id=mark.id, is_active=True, display_order=1)
    db_session.add(model)

    # App Settings
    db_session.add(AppSetting(key="subscriptions_enabled", value="false"))

    db_session.commit()
    return {
        "city": city,
        "category": category,
        "mark": mark,
        "model": model,
    }


@pytest.fixture(scope="function")
def test_client_user(db_session):
    """Create a verified regular user."""
    user = User(
        name="Test Client",
        email="client@example.com",
        phone_number="+77011112233",
        password_hash=get_password_hash("TestPass123!"),
        role="client",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_owner_user(db_session):
    """Create a verified vehicle owner user with CarOwner record."""
    user = User(
        name="Test Owner",
        email="owner@example.com",
        phone_number="+77022223344",
        password_hash=get_password_hash("OwnerPass123!"),
        role="client",
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()

    owner_rec = CarOwner(user_id=user.id)
    db_session.add(owner_rec)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_admin_user(db_session):
    """Create an administrator user."""
    admin = User(
        name="Admin User",
        email="admin@autorentgo.test",
        phone_number="+77777777777",
        password_hash=get_password_hash("AdminPass123!"),
        role="admin",
        is_active=True,
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture(scope="function")
def client_auth_headers(test_client_user):
    """Bearer token headers for test_client_user."""
    token = create_access_token(subject=test_client_user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def owner_auth_headers(test_owner_user):
    """Bearer token headers for test_owner_user."""
    token = create_access_token(subject=test_owner_user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def admin_auth_headers(test_admin_user):
    """Bearer token headers for test_admin_user."""
    token = create_access_token(subject=test_admin_user.id)
    return {"Authorization": f"Bearer {token}"}
