import logging
from django.contrib.auth.models import AbstractUser
from django.db.models.manager import Manager
from typing import Optional
from ..models import TreatmentGuide
from common.services.openrouter_service import OpenRouterService

logger = logging.getLogger('treatments')

class TreatmentGuideValidationError(Exception):
    """Custom exception for treatment guide validation errors."""

class TreatmentGuideProcessingError(Exception):
    """Custom exception for AI processing errors."""

def find_existing_treatment_guide(factors: dict) -> Optional[TreatmentGuide]:
    """
    Find existing treatment guide with the same factors, regardless of their order.
    
    Args:
        factors: Dictionary containing diagnostic factors
        
    Returns:
        Existing TreatmentGuide if found, None otherwise
    """
    try:
        # Convert factors to a normalized form for comparison
        # Sort keys and convert to string to ensure consistent comparison
        normalized_factors = {k: factors[k] for k in sorted(factors.keys())}
        
        # Query all guides and compare normalized factors
        # Note: This is more expensive than direct DB query but ensures order-independent comparison
        guides = TreatmentGuide.objects.all()
        for guide in guides:
            guide_factors = guide.factors
            if guide_factors:
                normalized_guide_factors = {k: guide_factors[k] for k in sorted(guide_factors.keys())}
                if normalized_factors == normalized_guide_factors:
                    logger.info("Found existing treatment guide with ID: %s", guide.id)
                    return guide
        
        return None
        
    except (KeyError, AttributeError, TypeError) as e:
        logger.warning("Error while searching for existing treatment guide: %s", str(e))
        return None

def create_treatment_guide(*, factors: dict, user: 'AbstractUser') -> dict:
    """
    Create a treatment guide based on diagnostic factors using AI analysis.
    
    Args:
        factors: Dictionary containing diagnostic factors (any key-value pairs)
        user: User creating the guide
    
    Returns:
        dict containing treatment guide data
    
    Raises:
        TreatmentGuideValidationError: If validation fails
        TreatmentGuideProcessingError: If processing fails
    """
    try:
        # Log the incoming request
        logger.info("Processing treatment guide request with factors: %s", factors)

        # Initialize OpenRouter service
        open_router = OpenRouterService()
        
        # Prepare the system message for AI
        system_message = """Jesteś ekspertem od diagnostyki różnicowej zwierząt na podstawie objawów klinicznych.
                    Analizuj podane objawy i przedstaw możliwe diagnozy różnicowe oraz zalecenia diagnostyczne. 
                    Diagnozy mają być przedstawione w maksymalnie 5 punktach z krótkim opisem.
                    Nie używaj znaków markdown. Po prostu plain text.
                    Tylko i wyłączenie w punktach, nie dodawaj dodatkowego tekstu. Jeśli uważasz, że jest za mało danych, po prostu poproś o więcej informacji.
                    Jeśli uważasz, że objawy nie odnoszą się do żadnej choroby, napisz, że nie można postawić diagnozy.
                    Używaj tylko i wyłącznie języka polskiego."""
        
        # Prepare user message with factors
        user_message = """Przeanalizuj podane objawy i przedstaw możliwe diagnozy różnicowe oraz zalecenia diagnostyczne. \n Objawy: \n """
        for key, value in factors.items():
            user_message += f"- {key}: {value}\n"

        # Set model parameters
        model_params = {
            "temperature": 0.3,  # Lower temperature for more focused responses
            "max_tokens": 1000,
            "top_p": 0.95,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }

        # Send request to OpenRouter
        result = open_router.send_openrouter_request(
            system_message=system_message,
            user_message=user_message,
            response_format=None,  # No specific format required
            model_name="openai/gpt-4o-mini",  # Using GPT-4 for medical analysis
            model_params=model_params
        )
        
        # Create and save the treatment guide
        treatment_guide = TreatmentGuide.objects.create(
            result=result,
            factors=factors,
            created_by=user
        )
        
        logger.info("Created treatment guide with ID: %s", treatment_guide.id)
        
        # Return the result in expected format
        return {
            "id": treatment_guide.id,
            "result": treatment_guide.result,
            "factors": treatment_guide.factors
        }
        
    except (KeyError, ValueError, TypeError) as e:
        raise TreatmentGuideValidationError(f"Invalid factors format: {str(e)}") from e
    except Exception as e:
        raise TreatmentGuideProcessingError(f"Error creating treatment guide: {str(e)}") from e
