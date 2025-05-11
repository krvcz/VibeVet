from rest_framework import serializers
from django.db import transaction
import logging
from common.serializers import RatingSerializer
from common.services import rating_service
from drugs.models import Drug
from interactions.services import drug_interaction_service
from interactions.services.drug_interaction_service import DrugInteractionValidationError
from users.services import search_history_service
from .models import DrugInteraction
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

# ==========================
# DRUG INTERACTION SERIALIZERS
# ==========================

logger = logging.getLogger(__name__)

class DrugInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugInteraction
        fields = [
            'id',
            'query',
            'result',
        ]


class CreateDrugInteractionSerializer(serializers.Serializer):
    drug_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        help_text="List of drug IDs to check for interaction."
    )
    context = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=50,
        help_text="Optional context for the AI query."
    )

    @transaction.atomic
    def create(self, validated_data):
        drug_ids = [drug.id for drug in validated_data['drugs']]
        
        # Check for existing interaction
        existing = drug_interaction_service.find_interaction_with_same_drugs(drug_ids)
        if existing:
            self.is_existing = True
            search_history_service.add_to_history(
            module='drug-interaction',
            query=f"Drug interaction query with drugs: {', '.join(map(str, drug_ids))}",
            user=self.context['request'].user
            )
            return existing       
        self.is_existing = False

        instance = drug_interaction_service.create_interaction(
            drugs=validated_data['drugs'],
            context=validated_data.get('context'),
            user=self.context['request'].user
        )
        # Add to search history
        search_history_service.add_to_history(
            module='drug-interaction',
            query=f"Drug interaction query with drugs: {', '.join(map(str, drug_ids))}",
            user=self.context['request'].user
        )

        # Create new interaction
        return instance
    

    def validate_drug_ids(self, value) -> None:
        try:
            drugs = list(Drug.objects.filter(id__in=value))
            if not drugs:
                raise DrugInteractionValidationError("No valid drug IDs provided")
            if len(drugs) != len(value):
                found_ids = {drug.id for drug in drugs}
                missing_ids = [str(id) for id in value if id not in found_ids]
                raise DrugInteractionValidationError(
                    f"Invalid drug IDs: {', '.join(missing_ids)}"
                )
        except Drug.DoesNotExist as e:
            logger.error("Invalid drug IDs provided: %s", str(e))
            raise DrugInteractionValidationError("One or more drug IDs are invalid") from e

        return {'value': value, 'drugs': drugs}
    
    def validate(self, attrs):
        validated_drug_ids = attrs['drug_ids']
        if isinstance(validated_drug_ids, dict):
            attrs['drugs'] = validated_drug_ids['drugs']
            attrs['drug_ids'] = validated_drug_ids['value']
        return attrs


class RateDrugInteractionSerializer(RatingSerializer):
   ...