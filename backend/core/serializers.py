from rest_framework import serializers
from .models import (
    Drug,
    CustomDrug,
    DrugInteraction,
    TreatmentGuide,
    UserSearchHistory,
    Species,
    MeasurementUnit,
)

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ['id', 'name']

class MeasurementUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementUnit
        fields = ['id', 'name', 'short_name']

# ==========================
# 1. DRUG SERIALIZERS
# ==========================

class DrugSerializer(serializers.ModelSerializer):
    # Format the measurement_value as a string with fixed precision
    measurement_value = serializers.DecimalField(max_digits=10, decimal_places=5, coerce_to_string=True)
    # Add nested serializers for related fields
    species = SpeciesSerializer(read_only=True)
    measurement_target = MeasurementUnitSerializer(read_only=True)

    class Meta:
        model = Drug
        fields = [
            'id',
            'name',
            'active_ingredient',
            'species',
            'measurement_value',
            'measurement_target'
        ]


# ==========================
# 2. CUSTOM DRUG SERIALIZERS
# ==========================

class CreateCustomDrugSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=20,
        help_text="Name of the custom drug"
    )
    active_ingredient = serializers.CharField(
        max_length=20,
        help_text="Active ingredient in the drug"
    )
    species = serializers.IntegerField(
        min_value=1,
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
        help_text="Measurement value with 5 decimal precision"
    )
    measurement_target = serializers.IntegerField(
        min_value=1,
        help_text="ID of the measurement unit"
    )

    def create(self, validated_data):
        raise NotImplementedError("Use custom_drug_service instead")

    def update(self, instance, validated_data):
        raise NotImplementedError("Use custom_drug_service instead")

class CustomDrugSerializer(serializers.ModelSerializer):
    measurement_value = serializers.DecimalField(max_digits=10, decimal_places=5, coerce_to_string=True)

    class Meta:
        model = CustomDrug
        fields = [
            'id',
            'name',
            'active_ingredient',
            'species',
            'contraindications',
            'measurement_value',
            'measurement_target'
        ]

class UpdateCustomDrugSerializer(serializers.ModelSerializer):
    """
    Serializer for updating custom drugs. All fields are optional.
    """
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
    species = serializers.IntegerField(
        min_value=1,
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
    measurement_target = serializers.IntegerField(
        min_value=1,
        required=False,
        help_text="ID of the measurement unit"
    )

    class Meta:
        model = CustomDrug
        fields = [
            'name',
            'active_ingredient',
            'species',
            'contraindications',
            'measurement_value',
            'measurement_target'
        ]


# ==========================
# 3. DRUG INTERACTION SERIALIZERS
# ==========================

class DrugInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugInteraction
        fields = [
            'id',
            'query',
            'result',
            'positive_rating',
            'negative_rating',
            'created_at'
        ]


class CreateDrugInteractionSerializer(serializers.Serializer):
    drug_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        help_text="List of drug IDs to check for interaction."
    )
    context = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=50,
        help_text="Optional context for the AI query."
    )

    def create(self, validated_data):
        raise NotImplementedError("Use drug_interaction_service instead")

    def update(self, instance, validated_data):
        raise NotImplementedError("Use drug_interaction_service instead")

class RateDrugInteractionSerializer(serializers.Serializer):
    rating = serializers.ChoiceField(
        choices=[('up', 'up'), ('down', 'down')],
        help_text="Choose 'up' for positive rating or 'down' for negative."
    )

    def create(self, validated_data):
        raise NotImplementedError("Use drug_interaction_service instead")

    def update(self, instance, validated_data):
        raise NotImplementedError("Use drug_interaction_service instead")


# ==========================
# 4. DOSAGE CALCULATOR SERIALIZERS
# ==========================

class DosageCalcInputSerializer(serializers.Serializer):
    drug_id = serializers.IntegerField(min_value=1)
    weight = serializers.IntegerField(min_value=1, max_value=999)
    species = serializers.IntegerField(min_value=1)
    target_unit = serializers.IntegerField(min_value=1)

    def create(self, validated_data):
        raise NotImplementedError("Use dosage_calculator_service instead")

    def update(self, instance, validated_data):
        raise NotImplementedError("Use dosage_calculator_service instead")

class DosageCalcResultSerializer(serializers.Serializer):
    drug_id = serializers.IntegerField()
    calculated_dose = serializers.CharField(
        help_text="Calculated dose formatted with high precision, e.g., '15.00000'."
    )
    unit = serializers.CharField(
        help_text="Measurement unit string, e.g., 'mg'."
    )

    def create(self, validated_data):
        raise NotImplementedError("Use dosage_calculator_service instead")

    def update(self, instance, validated_data):
        raise NotImplementedError("Use dosage_calculator_service instead")


# ==========================
# 5. TREATMENT GUIDE SERIALIZERS
# ==========================

# For creating a treatment guide query, factors are submitted as a JSON object.
class CreateTreatmentGuideSerializer(serializers.Serializer):
    factors = serializers.DictField(
        child=serializers.JSONField(),
        help_text="Diagnostic factors for treatment guide query."
    )

    def create(self, validated_data):
        raise NotImplementedError("Use treatment_guide_service instead")

    def update(self, instance, validated_data):
        raise NotImplementedError("Use treatment_guide_service instead")

class TreatmentGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentGuide
        fields = [
            'id',
            'result',
            'factors',
            'positive_rating',
            'negative_rating'
        ]


class RateTreatmentGuideSerializer(serializers.Serializer):
    rating = serializers.ChoiceField(
        choices=[('up', 'up'), ('down', 'down')],
        help_text="Choose 'up' or 'down' to rate the treatment guide."
    )

    def create(self, validated_data):
        raise NotImplementedError("Use treatment_guide_service instead")

    def update(self, instance, validated_data):
        raise NotImplementedError("Use treatment_guide_service instead")


# ==========================
# 6. USER SEARCH HISTORY SERIALIZER
# ==========================

class UserSearchHistorySerializer(serializers.ModelSerializer):
    # Rename 'created_at' to 'timestamp' as expected by the DTO.
    timestamp = serializers.DateTimeField(source='created_at')

    class Meta:
        model = UserSearchHistory
        fields = [
            'id',
            'module',
            'query',
            'timestamp'
        ]