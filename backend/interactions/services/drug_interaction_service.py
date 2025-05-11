import logging
from typing import List, Literal, Optional
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import json

from common.services.openrouter_service import OpenRouterService
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
    """Create a new drug interaction record.
    
    Args:
        drugs: List of drugs to check interactions for
        user: User creating the interaction
        context: Optional additional context for the interaction
        
    Returns:
        DrugInteraction: The created interaction record
    """
    # Prepare drug names for the query
    drug_names = sorted([drug.name for drug in drugs])
    drug_details = [f"{drug.name} ({drug.active_ingredient}, {drug.contraindications})" for drug in drugs]
    query = ", ".join(drug_names)

    # Prepare the OpenRouter request
    system_message = """Jesteś ekspertem od interakcji leków weterynaryjnych. Analizuj potencjalne interakcje między podanymi lekami, ich składnikami aktywnymi i przeciwwskazaniami.
    Weź pod uwagę:
    1. Bezpośrednie interakcje farmakologiczne
    2. Łączne działanie na układy narządów
    3. Przeciwwskazania i czynniki ryzyka
    4. Implikacje kliniczne i stopień nasilenia
    Przedstaw ustrukturyzowaną analizę z poziomem nasilenia, mechanizmem interakcji i zaleceniami klinicznymi. Używaj tylko i wyłączenie języka polskiego."""

    user_message = f"Przeanalizuj potencjalne interakcje między lekami: {', '.join(drug_details)}"
    if context:
        user_message += f"\nDodatkowy kontekst: {context}"

    response_format = {
      "type": "json_schema",
      "json_schema": {
        "name": "interaction",
        "strict": True,
        "schema": {
          "type": "object",
          "properties": {
            "severity": {
              "type": "string",
              "description": "Poziom nasilenia interakcji leków (niski, umiarkowany, wysoki, przeciwwskazany)",
            },
            "summary": {
              "type": "string",
              "description": "Krótki przegląd interakcji. Maksymalnie 2-3 zdania.",
            },
            "mechanism": {
              "type": "string",
              "description": "Szczegółowe wyjaśnienie mechanizmu interakcji. Maksymalnie 2-3 zdania.",
            },
            "recommendations": {
              "type": "string",
              "description": "Zalecenia kliniczne dotyczące zarządzania interakcją. Maksymalnie 2-3 zdania.",
            },
          },
          "required": ["severity", "summary", "mechanism", "recommendations"],
          "additionalProperties": False,
        },
      },
    }

    # Initialize OpenRouter service and send request
    try:
        open_router = OpenRouterService()
        result = open_router.send_openrouter_request(
            system_message=system_message,
            user_message=user_message,
            response_format=response_format,
            model_name="openai/gpt-4o-mini",  # Updated model name format
            model_params={
                "temperature": 0.3,  # Lower temperature for more focused/consistent responses
                "max_tokens": 1000,
                "top_p": 0.95,
                "frequency_penalty": 0,
                "presence_penalty": 0
            }
        )

        logger.info(
            "Received OpenRouter response for drugs: %s with confidence: %f",
            query,
            result.get("confidence", 0)
        )

        # Create interaction record
        interaction = DrugInteraction.objects.create(
            query=query,
            result=json.dumps(result),  # Store the full structured response
            context=context,
            created_by=user
        )
        interaction.drugs.set(drugs)

        logger.info(f"Created new drug interaction: {interaction.id} for drugs: {query}")
        return interaction

    except Exception as e:
        logger.error("Error creating drug interaction: %s", str(e))
        raise DrugInteractionValidationError(f"Failed to analyze drug interactions: {str(e)}")


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