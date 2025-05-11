from django.forms import ValidationError
from django.utils import timezone
from rest_framework import serializers
from decimal import ROUND_HALF_UP, Decimal

from common.models import Unit, Species
from drugs.services.dosage_calculator_service import DosageCalculatorService
from .models import Drug, CustomDrug
from common.serializers import SpeciesSerializer, UnitSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


# ==========================
# 1. DRUG SERIALIZERS
# ==========================

class DrugSerializer(serializers.ModelSerializer):
    # Format the measurement_value as a string with fixed precision
    measurement_value = serializers.DecimalField(max_digits=10, decimal_places=5, coerce_to_string=True)
    # Add nested serializers for related fields
    species = SpeciesSerializer(read_only=True)
    measurement_unit = UnitSerializer(read_only=True)
    per_weight_value = serializers.DecimalField(max_digits=10, decimal_places=5, coerce_to_string=True)
    per_weight_unit = UnitSerializer(read_only=True)

    class Meta:
        model = Drug
        fields = [
            'id',
            'name',
            'active_ingredient',
            'species',
            'contraindications',
            'measurement_value',
            'measurement_unit',
            'per_weight_value',
            'per_weight_unit',
        ]


# ==========================
# 2. CUSTOM DRUG SERIALIZERS
# ==========================
class CustomDrugSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    measurement_value = serializers.DecimalField(max_digits=10, decimal_places=5, coerce_to_string=True)
    species = SpeciesSerializer(read_only=True)
    measurement_unit = UnitSerializer(read_only=True)
    per_weight_value = serializers.DecimalField(max_digits=10, decimal_places=5, coerce_to_string=True)
    per_weight_unit = UnitSerializer(read_only=True)

    class Meta:
        model = CustomDrug
        fields = [
            'id',
            'name',
            'active_ingredient',
            'species',
            'contraindications',
            'measurement_value',
            'measurement_unit',
            'per_weight_value',
            'per_weight_unit'
        ]

class UpdateCustomDrugSerializer(serializers.ModelSerializer):
    """
    Serializer for updating custom drugs. All fields are optional.
    """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        max_length=20,
        required=False,
        help_text="Name of the custom drug"
    )
    active_ingredient = serializers.CharField(
        max_length=20,
        required=False,
        help_text="Active ingredient in the drug"
    )
    species= serializers.PrimaryKeyRelatedField(
        queryset=Species.objects.all(),
        required=False,
        help_text="ID of the species this drug is for"
    )
    contraindications = serializers.CharField(
        max_length=100,
        allow_null=True,
        required=False,
        help_text="Optional contraindications for the drug"
    )
    measurement_value = serializers.DecimalField(
        max_digits=10,
        decimal_places=5,
        coerce_to_string=True,
        required=False,
        help_text="Measurement value with 5 decimal precision"
    )
    measurement_unit = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(),
        required=False,
        help_text="ID of the measurement unit"
    )
    per_weight_value = serializers.DecimalField(
        max_digits=10,
        decimal_places=5,
        coerce_to_string=True,
        required=False,
        help_text="Per weight value with 5 decimal precision"
    )
    per_weight_unit = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(),
        required=False,
        help_text="ID of the per weight unit"
    )

    class Meta:
        model = CustomDrug
        fields = [
            'id',
            'name',
            'active_ingredient',
            'species',
            'contraindications',
            'measurement_value',
            'measurement_unit',
            'per_weight_value',
            'per_weight_unit'
        ]

class CreateCustomDrugSerializer(UpdateCustomDrugSerializer):
    name = serializers.CharField(
        max_length=20,
        help_text="Name of the custom drug"
    )
    active_ingredient = serializers.CharField(
        max_length=20,
        help_text="Active ingredient in the drug"
    )
    species= serializers.PrimaryKeyRelatedField(
        queryset=Species.objects.all(),
        help_text="ID of the species this drug is for"
    )
    contraindications = serializers.CharField(
        max_length=100,
        allow_null=True,
        allow_blank=True,
        required=False,
        help_text="Optional contraindications for the drug"
    )
    measurement_value = serializers.DecimalField(
        max_digits=10,
        decimal_places=5,
        coerce_to_string=True,
        help_text="Measurement value with 5 decimal precision"
    )
    measurement_unit = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(),
        help_text="ID of the measurement unit"
    )

    per_weight_value = serializers.DecimalField(
        max_digits=10,
        decimal_places=5,
        coerce_to_string=True,
        required=False,
        help_text="Per weight value with 5 decimal precision"
    )
    per_weight_unit = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(),
        required=False,
        help_text="ID of the per weight unit"
    )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['created_by'] = user
        validated_data['created_at'] = timezone.now()
        validated_data['updated_at'] = timezone.now()
        
        return super().create(validated_data)
    
# ==========================
# 3. DOSAGE CALCULATOR SERIALIZERS
# ==========================

class DosageCalcInputSerializer(serializers.Serializer):
    drug_id = serializers.IntegerField(
        help_text="ID of the drug or custom drug"
    )
    weight = serializers.DecimalField(max_digits=5, decimal_places=2, rounding=ROUND_HALF_UP)  # Allow up to 999.99
    species= serializers.PrimaryKeyRelatedField(
        queryset=Species.objects.all(),
        help_text="ID of the species this drug is for"
    )
    target_unit = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(),
        help_text="ID of the target unit for dosage calculation"
    )

    drug_type = serializers.ChoiceField(
        choices=[('standard', 'Standard'), ('custom', 'Custom')],
        default='standard',
        help_text="Type of drug: standard or custom"
    )

    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Weight must be greater than 0")
        if value >= 1000:
            raise serializers.ValidationError("Weight must be less than 1000")
        return value

    def validate(self, attrs):
        drug_id = attrs['drug_id']
        drug_type = attrs['drug_type']
        
        # Get the appropriate drug model based on type
        try:
            if drug_type == 'standard':
                drug = Drug.objects.get(pk=drug_id)
            else:  # custom
                drug = CustomDrug.objects.get(pk=drug_id)
                
                # Check if user has access to this custom drug if needed
                request = self.context.get('request')
                if request and request.user and not isinstance(request.user, AnonymousUser):
                    if drug.user != request.user:
                        raise serializers.ValidationError(
                            {"drug_id": "You don't have access to this custom drug"}
                        )
                
        except (Drug.DoesNotExist, CustomDrug.DoesNotExist):
            raise serializers.ValidationError(
                {"drug_id": f"{drug_type.capitalize()} drug with ID {drug_id} does not exist"}
            )
        if drug.per_weight_value and drug.per_weight_value <= 0:
            raise ValidationError(
                {"drug_id": "Drug has invalid per_weight_value"}
            )
        attrs['drug'] = drug

        # Verify target unit exists and is compatible
        target_unit = attrs['target_unit']
        source_unit = drug.measurement_unit
            
        from common.services.unit_conversion_service import UnitConversionService
        if not UnitConversionService.is_compatible(source_unit.short_name, target_unit.short_name):
            raise ValidationError(
                {"target_unit": f"Unit {target_unit.short_name} is not compatible with drug unit {source_unit.short_name}"}
            )
        attrs['target_unit_obj'] = target_unit

        return attrs

    def create(self, validated_data):
        # Extract validated data
        drug = validated_data['drug']
        weight = validated_data['weight']
        target_unit = validated_data['target_unit_obj']
            
        # Calculate dosage
        result = DosageCalculatorService.calculate_dosage(
            drug_base_value=drug.measurement_value,
            per_weight_value=drug.per_weight_value or Decimal('1'),
            weight=weight,
            source_unit=drug.measurement_unit.short_name,
            target_unit=target_unit.short_name,
        )

        response_data = {
            'drug_id': drug.id,
            'calculated_dose': result['calculated_dose'],
            'unit': result['unit']
        }

        return response_data


class DosageCalcResultSerializer(serializers.Serializer):
    drug_id = serializers.IntegerField()
    calculated_dose = serializers.DecimalField(
        max_digits=20,  # Ensure total digits do not exceed 10
        decimal_places=5,
        coerce_to_string=True,
    )
    unit = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError("Create not supported")

    def update(self, instance, validated_data):
        raise NotImplementedError("Update not supported")