import pytest
from decimal import Decimal
from rest_framework.test import APIClient
from users.tests.factories import UserFactory
from common.models import Species, Unit
from drugs.models import CustomDrug


@pytest.fixture
def api_client():
    """Return an authenticated APIClient instance."""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    """Return an authenticated APIClient instance."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def user():
    """Create and return a regular user."""
    return UserFactory(
        email='testuser@example.com',
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def admin_user():
    """Create and return an admin user."""
    return UserFactory(
        email='admin@example.com',
        is_staff=True,
        is_superuser=True
    )


@pytest.fixture
def species(user):
    """Create and return a test species."""
    return Species.objects.create(
        name="Dog",
        description="Domestic dog",
        created_by=user
    )


@pytest.fixture
def measurement_unit(user):
    """Create and return a measurement unit (mass)."""
    return Unit.objects.create(
        name="Milligram",
        short_name="mg",
        description="Mass measurement unit",
        created_by=user
    )


@pytest.fixture
def weight_unit(user):
    """Create and return a weight unit (mass)."""
    return Unit.objects.create(
        name="Kilogram",
        short_name="kg",
        description="Weight measurement unit",
        created_by=user
    )


@pytest.fixture
def valid_drug_data(species, measurement_unit, weight_unit):
    """Return valid drug data for testing."""
    return {
        'name': 'Test Drug',
        'active_ingredient': 'Test Ingredient',
        'species': species.id,
        'measurement_value': Decimal('100.00'),
        'measurement_unit': measurement_unit.id,
        'per_weight_value': Decimal('10.00'),
        'per_weight_unit': weight_unit.id,
        'contraindications': 'Test contraindications'
    } 