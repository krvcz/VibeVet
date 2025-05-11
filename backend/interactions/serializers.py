from rest_framework import serializers
from django.db import transaction
import logging
import json
from common.serializers import RatingSerializer
from drugs.models import Drug
from interactions.services import drug_interaction_service
from interactions.services.drug_interaction_service import DrugInteractionValidationError
from users.services import search_history_service
from .models import DrugInteraction

# ==========================
# DRUG INTERACTION SERIALIZERS
# ==========================

logger = logging.getLogger(__name__)

class OpenRouterInteractionResponseSerializer(serializers.Serializer):
    severity = serializers.CharField(
        help_text="Interaction severity level (low, moderate, high, contraindicated)"
    )
    summary = serializers.CharField(
        help_text="Brief overview of the interaction"
    )
    mechanism = serializers.CharField(
        help_text="Detailed explanation of the interaction mechanism"
    )
    recommendations = serializers.CharField(
        help_text="Clinical recommendations for managing the interaction"
    )

class DrugInteractionSerializer(serializers.ModelSerializer):

    class Meta:
        model = DrugInteraction
        fields = [
            'id',
            'query',
            'result',
        ]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get('result'):
            try:
                # If result is a string, try to parse it as JSON
                if isinstance(data['result'], str):
                    parsed_result = json.loads(data['result'])
                else:
                    parsed_result = data['result']
                
                # Validate the parsed result against OpenRouterResponseSerializer
                result_serializer = OpenRouterInteractionResponseSerializer(data=parsed_result)
                if result_serializer.is_valid():
                    data['result'] = result_serializer.data
                else:
                    logger.error("Invalid result format for interaction %s: %s", 
                               instance.id, result_serializer.errors)
                    data['result'] = None
            except json.JSONDecodeError:
                logger.error("Failed to parse result JSON for interaction %s", 
                           instance.id)
                data['result'] = None
            except ValueError as e:
                logger.error("Error processing result for interaction %s: %s", 
                           instance.id, str(e))
                data['result'] = None
        return data

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_existing = False
        self._context = kwargs.get('context', {})

    @transaction.atomic
    def create(self, validated_data):
        drug_ids = [drug.id for drug in validated_data['drugs']]
        request = self._context.get('request')
        
        # Check for existing interaction
        existing = drug_interaction_service.find_interaction_with_same_drugs(drug_ids)
        if existing:
            self.is_existing = True
            if request:
                search_history_service.add_to_history(
                    module='drug-interaction',
                    query=f"Drug interaction query with drugs: {', '.join(map(str, drug_ids))}",
                    user=request.user
                )
            return existing       

        instance = drug_interaction_service.create_interaction(
            drugs=validated_data['drugs'],
            context=validated_data.get('context'),
            user=request.user if request else None
        )
        
        # Add to search history
        if request:
            search_history_service.add_to_history(
                module='drug-interaction',
                query=f"Drug interaction query with drugs: {', '.join(map(str, drug_ids))}",
                user=request.user
            )

        return instance

    def update(self, instance, validated_data):
        return instance

    def validate_drug_ids(self, value) -> dict:
        try:
            # Type checker doesn't recognize Django's dynamic model manager
            drugs = list(Drug.objects.filter(id__in=value))  # type: ignore
            if not drugs:
                raise DrugInteractionValidationError("No valid drug IDs provided")
            if len(drugs) != len(value):
                found_ids = {drug.id for drug in drugs}
                missing_ids = [str(id) for id in value if id not in found_ids]
                raise DrugInteractionValidationError(
                    f"Invalid drug IDs: {', '.join(missing_ids)}"
                )
        except Exception as e:
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
    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance