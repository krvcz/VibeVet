
from rest_framework import serializers

from common.serializers import RatingSerializer
from treatments.services import treatment_guide_service
from users.services import search_history_service
from django.db import transaction
from .models import TreatmentGuide

# ==========================
# TREATMENT GUIDE SERIALIZERS
# ==========================

# For creating a treatment guide query, factors are submitted as a JSON object.
class CreateTreatmentGuideSerializer(serializers.Serializer):
    factors = serializers.DictField(
        child=serializers.JSONField(),
        help_text="Diagnostic factors for treatment guide query."
    )

    def validate_factors(self, value):
        factors_dict = len(value)
        if factors_dict == 0:
            raise serializers.ValidationError("Factors cannot be empty.")
        if factors_dict > 10:
            raise serializers.ValidationError("Factors cannot exceed 10 items.")

        for key, val in value.items():
            if len(str(key)) > 20:
                raise serializers.ValidationError(f"Factor key '{key}' exceeds maximum length of 10 characters.")
            if len(str(val)) > 20:
                raise serializers.ValidationError(f"Factor value for key '{key}' exceeds maximum length of 10 characters.")
        
        return value

    @transaction.atomic
    def create(self, validated_data):
        existing = treatment_guide_service.find_existing_treatment_guide(validated_data['factors'])
        if existing:
            self.is_existing = True
            # Add to search history
            search_history_service.add_to_history(
            module='treatment-guide',
            query=f"Treatment guide query with factors: {list(validated_data['factors'].keys())}",
            user=self.context['request'].user
            )
            return existing
            
        self.is_existing = False

        instance = treatment_guide_service.create_treatment_guide(
            factors=validated_data['factors'],
            user=self.context['request'].user
        )

        # Add to search history
        search_history_service.add_to_history(
            module='treatment-guide',
            query=f"Treatment guide query with factors: {list(validated_data['factors'].keys())}",
            user=self.context['request'].user
        )

        return instance

class TreatmentGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentGuide
        fields = [
            'id',
            'result',
            'factors'
        ]


class RateTreatmentGuideSerializer(RatingSerializer):
    ...