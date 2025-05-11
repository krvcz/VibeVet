import logging
from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from ..models import TreatmentGuide

logger = logging.getLogger('treatments')

class TreatmentGuideValidationError(Exception):
    """Custom exception for treatment guide validation errors."""

class TreatmentGuideProcessingError(Exception):
    """Custom exception for AI processing errors."""


def find_existing_treatment_guide(factors: dict) -> TreatmentGuide | None:
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
    Create a treatment guide based on diagnostic factors.
    
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

        # TODO: In future implementation, add AI service integration here
        # For now, return a mock response analyzing the provided factors
        mock_result = analyze_factors_mock(factors)
        
        # Create and save the treatment guide
        treatment_guide = TreatmentGuide.objects.create(
            result=mock_result,
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

def analyze_factors_mock(factors: dict) -> str:
    """
    Mock function to analyze diagnostic factors and return a preliminary assessment.
    This will be replaced by actual AI integration in the future.
    """
    # Create a simple summary of provided factors
    factor_summary = "\n".join(f"- {key}: {value}" for key, value in factors.items())
    
    return (
        f"Preliminary assessment based on provided factors:\n\n"
        f"{factor_summary}\n\n"
        f"Note: This is a mock response. In the future, this will be replaced "
        f"with actual AI-powered analysis."
    )
