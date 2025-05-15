import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from drugs.models import Drug, CustomDrug

pytestmark = pytest.mark.unit

@pytest.mark.django_db
class TestDrugModel:
    def test_create_valid_drug(self, species, measurement_unit, weight_unit, user):
        """Test creating a valid drug instance."""
        drug = Drug.objects.create(
            name="Amoxicillin",
            active_ingredient="Amox trihydrate",
            species=species,
            measurement_value=Decimal("100.00"),
            measurement_unit=measurement_unit,
            per_weight_value=Decimal("10.00"),
            per_weight_unit=weight_unit,
            created_by=user
        )
        
        assert drug.name == "Amoxicillin"
        assert drug.active_ingredient == "Amox trihydrate"
        assert drug.species == species
        assert drug.measurement_value == Decimal("100.00")
        assert drug.measurement_unit == measurement_unit
        assert drug.per_weight_value == Decimal("10.00")
        assert drug.per_weight_unit == weight_unit

    def test_drug_str_representation(self, species, measurement_unit, weight_unit, user):
        """Test the string representation of a drug."""
        drug = Drug.objects.create(
            name="Amoxicillin",
            active_ingredient="Amox trihydrate",
            species=species,
            measurement_value=Decimal("100.00"),
            measurement_unit=measurement_unit,
            per_weight_value=Decimal("10.00"),
            per_weight_unit=weight_unit,
            created_by=user
        )
        
        assert str(drug) == "Amoxicillin (Amox trihydrate)"

    def test_drug_with_invalid_measurement_value(self, species, measurement_unit, weight_unit, user):
        """Test that creating a drug with invalid measurement value raises error."""
        with pytest.raises(ValidationError):
            Drug.objects.create(
                name="Amoxicillin",
                active_ingredient="Amox trihydrate",
                species=species,
                measurement_value=Decimal("0.00"),  # Invalid - should be > 0
                measurement_unit=measurement_unit,
                per_weight_value=Decimal("10.00"),
                per_weight_unit=weight_unit,
                created_by=user
            )

    def test_drug_with_invalid_per_weight_value(self, species, measurement_unit, weight_unit, user):
        """Test that creating a drug with invalid per_weight_value raises error."""
        with pytest.raises(ValidationError):
            Drug.objects.create(
                name="Amoxicillin",
                active_ingredient="Amox trihydrate",
                species=species,
                measurement_value=Decimal("100.00"),
                measurement_unit=measurement_unit,
                per_weight_value=Decimal("-1.00"),  # Invalid - should be > 0
                per_weight_unit=weight_unit,
                created_by=user
            )

    def test_drug_name_max_length(self, species, measurement_unit, weight_unit, user):
        """Test that drug name cannot exceed max length."""
        with pytest.raises(ValidationError):
            Drug.objects.create(
                name="A" * 21,  # Exceeds max_length=20
                active_ingredient="Amox trihydrate",
                species=species,
                measurement_value=Decimal("100.00"),
                measurement_unit=measurement_unit,
                per_weight_value=Decimal("10.00"),
                per_weight_unit=weight_unit,
                created_by=user
            )

@pytest.mark.django_db
class TestCustomDrugModel:
    def test_create_valid_custom_drug(self, species, measurement_unit, weight_unit, user):
        """Test creating a valid custom drug instance."""
        custom_drug = CustomDrug.objects.create(
            name="Custom Amox",
            active_ingredient="Amox trihydrate",
            species=species,
            measurement_value=Decimal("100.00"),
            measurement_unit=measurement_unit,
            per_weight_value=Decimal("10.00"),
            per_weight_unit=weight_unit,
            user=user,
            created_by=user
        )
        
        assert custom_drug.name == "Custom Amox"
        assert custom_drug.active_ingredient == "Amox trihydrate"
        assert custom_drug.species == species
        assert custom_drug.measurement_value == Decimal("100.00")
        assert custom_drug.measurement_unit == measurement_unit
        assert custom_drug.per_weight_value == Decimal("10.00")
        assert custom_drug.per_weight_unit == weight_unit
        assert custom_drug.user == user

    def test_custom_drug_str_representation(self, species, measurement_unit, weight_unit, user):
        """Test the string representation of a custom drug."""
        custom_drug = CustomDrug.objects.create(
            name="Custom Amox",
            active_ingredient="Amox trihydrate",
            species=species,
            measurement_value=Decimal("100.00"),
            measurement_unit=measurement_unit,
            per_weight_value=Decimal("10.00"),
            per_weight_unit=weight_unit,
            user=user,
            created_by=user
        )
        
        assert str(custom_drug) == f"Custom Drug: Custom Amox (by {user})"

    def test_custom_drug_user_required(self, species, measurement_unit, weight_unit, user):
        """Test that custom drug requires a user."""
        with pytest.raises(ValidationError):
            CustomDrug.objects.create(
                name="Custom Amox",
                active_ingredient="Amox trihydrate",
                species=species,
                measurement_value=Decimal("100.00"),
                measurement_unit=measurement_unit,
                per_weight_value=Decimal("10.00"),
                per_weight_unit=weight_unit,
                created_by=user
                # user field missing
            ) 