import logging
from typing import List, Literal, Optional
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from ..models import DrugInteraction
from drugs.models import Drug
from common.services import rating_service
from django.db import models
from django.db.models import Q, Count
from functools import reduce
from operator import and_

logger = logging.getLogger(__name__)

class DrugInteractionValidationError(Exception):
    """Custom exception for drug interaction validation errors."""



def find_interaction_with_same_drugs(drug_ids: list[int]) -> Optional[DrugInteraction]:
    """
    Find interaction with exactly the same drugs using raw SQL.
    """
    
    sql = """
    WITH drug_counts AS (
        SELECT 
            di.id,
            COUNT(*) as drug_count,
            ARRAY_AGG(d.id ORDER BY d.id) as drug_ids
        FROM drug_interaction di
        JOIN drug_interaction_drugs did ON di.id = did.druginteraction_id
        JOIN drug d ON did.drug_id = d.id
        GROUP BY di.id
        HAVING COUNT(*) = %s
    )
    SELECT di.*
    FROM drug_counts dc
    JOIN drug_interaction di ON di.id = dc.id
    WHERE dc.drug_ids = (
        SELECT ARRAY_AGG(id ORDER BY id)
        FROM unnest(%s::bigint[]) AS id
    )
    LIMIT 1;
    """
    
    # Use list() to execute the query and get results
    results = list(DrugInteraction.objects.raw(
        sql, 
        [len(drug_ids), drug_ids]
    ))

    logger.info(f"Found existing interaction for drugs: {drug_ids}")
    
    # Return first result if exists, otherwise None
    return results[0] if results else None


def create_interaction(*, drugs: List[Drug], user: 'AbstractUser', context: str = None) -> DrugInteraction:
    """Create a new drug interaction record or return existing one."""
        
    # Create new interaction if none exists
    drug_names = sorted([drug.name for drug in drugs])
    query = ", ".join(drug_names)
    
    mock_result = "Mock AI-generated result for drugs: " + query

    interaction = DrugInteraction.objects.create(
        query=query,
        result=mock_result,
        context=context,
        created_by=user
    )
    interaction.drugs.set(drugs)

    logger.info(f"Created new drug interaction: {interaction.id} for drugs: {query}")
        
    return interaction

def rate_interaction(*, interaction_id: int, rating: Literal['up', 'down'], user: 'AbstractUser') -> None:
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