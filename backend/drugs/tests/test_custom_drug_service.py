import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from drugs.services.custom_drug_service import (
    create_custom_drug,
    update_custom_drug,
    delete_custom_drug,
    CustomDrugValidationError,
    validate_custom_drug_data
)
from drugs.models import CustomDrug

pytestmark = pytest.mark.unit

@pytest.fixture
def valid_drug_data(species, measurement_unit, weight_unit):
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

@pytest.mark.django_db
class TestCustomDrugService:
    def test_validate_custom_drug_data_valid(self, valid_drug_data):
        """Test validation of valid custom drug data."""
        # Should not raise any exception
        validate_custom_drug_data(valid_drug_data)

    def test_validate_custom_drug_data_empty_name(self, valid_drug_data):
        """Test validation with empty name."""
        valid_drug_data['name'] = ''
        with pytest.raises(CustomDrugValidationError, match='Name cannot be empty'):
            validate_custom_drug_data(valid_drug_data)

    def test_validate_custom_drug_data_empty_active_ingredient(self, valid_drug_data):
        """Test validation with empty active ingredient."""
        valid_drug_data['active_ingredient'] = ''
        with pytest.raises(CustomDrugValidationError, match='Active ingredient cannot be empty'):
            validate_custom_drug_data(valid_drug_data)

    def test_validate_custom_drug_data_invalid_measurement_value(self, valid_drug_data):
        """Test validation with invalid measurement value."""
        valid_drug_data['measurement_value'] = Decimal('0.00')
        with pytest.raises(CustomDrugValidationError, match='Measurement value must be positive'):
            validate_custom_drug_data(valid_drug_data)

    def test_create_custom_drug_success(self, valid_drug_data, user):
        """Test successful creation of custom drug."""
        custom_drug = create_custom_drug(valid_drug_data, user)
        
        assert isinstance(custom_drug, CustomDrug)
        assert custom_drug.name == valid_drug_data['name']
        assert custom_drug.active_ingredient == valid_drug_data['active_ingredient']
        assert custom_drug.measurement_value == valid_drug_data['measurement_value']
        assert custom_drug.user == user

    def test_create_custom_drug_invalid_species(self, valid_drug_data, user):
        """Test creation with invalid species ID."""
        valid_drug_data['species'] = 99999  # Non-existent species ID
        with pytest.raises(CustomDrugValidationError, match='Invalid species selected'):
            create_custom_drug(valid_drug_data, user)

    def test_update_custom_drug_success(self, valid_drug_data, user):
        """Test successful update of custom drug."""
        # First create a custom drug
        custom_drug = create_custom_drug(valid_drug_data, user)
        
        # Update data
        update_data = {
            'name': 'Updated Drug Name',
            'active_ingredient': 'Updated Ingredient'
        }
        
        updated_drug = update_custom_drug(custom_drug, update_data, user, partial=True)
        
        assert updated_drug.name == 'Updated Drug Name'
        assert updated_drug.active_ingredient == 'Updated Ingredient'
        # Original values should remain unchanged
        assert updated_drug.measurement_value == valid_drug_data['measurement_value']

    def test_update_custom_drug_wrong_user(self, valid_drug_data, user):
        """Test update with wrong user."""
        custom_drug = create_custom_drug(valid_drug_data, user)
        
        other_user = get_user_model().objects.create_user(
            email='other@example.com',
            password='testpass123'
        )
        
        update_data = {'name': 'Updated Drug Name'}
        with pytest.raises(CustomDrugValidationError, match="You don't have permission to modify this custom drug"):
            update_custom_drug(custom_drug, update_data, other_user)

    def test_delete_custom_drug_success(self, valid_drug_data, user):
        """Test successful deletion of custom drug."""
        custom_drug = create_custom_drug(valid_drug_data, user)
        delete_custom_drug(custom_drug, user)
        
        # Verify the drug was deleted
        with pytest.raises(CustomDrug.DoesNotExist):
            CustomDrug.objects.get(id=custom_drug.id)

    def test_delete_custom_drug_wrong_user(self, valid_drug_data, user):
        """Test deletion with wrong user."""
        custom_drug = create_custom_drug(valid_drug_data, user)
        
        other_user = get_user_model().objects.create_user(
            email='other@example.com',
            password='testpass123'
        )
        
        with pytest.raises(CustomDrugValidationError, match="You don't have permission to delete this custom drug"):
            delete_custom_drug(custom_drug, other_user) 