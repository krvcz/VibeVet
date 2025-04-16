import logging
from typing import List, Literal
from django.contrib.auth.models import User
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from core.models import Drug, DrugInteraction
from core.services import rating_service

logger = logging.getLogger(__name__)

class DrugInteractionValidationError(Exception):
    """Custom exception for drug interaction validation errors."""

def create_interaction(*, drug_ids: List[int], user: User, context: str = None) -> DrugInteraction:
    """
    Create a new drug interaction record.
    
    Args:
        drug_ids: List of drug IDs to check for interaction
        user: User creating the interaction request
        context: Optional context for the AI query
        
    Returns:
        DrugInteraction instance
        
    Raises:
        DrugInteractionValidationError: If validation fails
        Drug.DoesNotExist: If any drug ID is invalid
    """
    # Validate and get all drugs
    try:
        drugs = list(Drug.objects.filter(id__in=drug_ids))
        if len(drugs) != len(drug_ids):
            found_ids = {drug.id for drug in drugs}
            missing_ids = [str(id) for id in drug_ids if id not in found_ids]
            raise DrugInteractionValidationError(
                f"Invalid drug IDs: {', '.join(missing_ids)}"
            )
    except Drug.DoesNotExist as e:
        logger.error("Invalid drug IDs provided: %s", str(e))
        raise DrugInteractionValidationError("One or more drug IDs are invalid") from e

    # Build query string from drug names
    drug_names = [drug.name for drug in drugs]
    query = ", ".join(drug_names)

    # For MVP, mock the AI response
    mock_result = f"Mock interaction analysis for: {query}"
    if context:
        mock_result += f"\nContext: {context}"

    # Create interaction record
    with transaction.atomic():
        interaction = DrugInteraction.objects.create(
            query=query,
            result=mock_result,
            context=context,
            created_by=user
        )
        interaction.drugs.set(drugs)
        
    return interaction

def rate_interaction(*, interaction_id: int, rating: Literal['up', 'down'], user: User) -> None:
    """
    Rate a drug interaction record.
    
    Args:
        interaction_id: ID of the interaction to rate
        rating: Either 'up' or 'down'
        user: User performing the rating
        
    Raises:
        DrugInteractionValidationError: If validation fails or user already rated
        ObjectDoesNotExist: If interaction with given ID doesn't exist
    """
    try:
        interaction = DrugInteraction.objects.get(id=interaction_id)
    except DrugInteraction.DoesNotExist as exc:
        logger.error("Drug interaction with ID %d not found", interaction_id)
        raise ObjectDoesNotExist(f"Drug interaction with ID {interaction_id} not found") from exc

    try:
        # Use the generic rating service
        rating_service.rate_content(
            content_object=interaction,
            rating=rating,
            user=user
        )
    except rating_service.RatingValidationError as e:
        raise DrugInteractionValidationError(str(e)) from e