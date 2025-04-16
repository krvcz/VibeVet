import logging
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from core.models import TreatmentGuide

logger = logging.getLogger('core')

class TreatmentGuideValidationError(Exception):
    """Custom exception for treatment guide validation errors."""

class TreatmentGuideProcessingError(Exception):
    """Custom exception for AI processing errors."""

@transaction.atomic
def create_treatment_guide(*, factors: dict, user: User) -> dict:
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
        
        # Basic validation - just check if factors is not empty
        if not factors:
            logger.warning("No diagnostic factors provided")
            raise TreatmentGuideValidationError("No diagnostic factors provided")

        # TODO: In future implementation, add AI service integration here
        # For now, return a mock response analyzing the provided factors
        mock_result = analyze_factors_mock(factors)
        
        # Create and save the treatment guide
        treatment_guide = TreatmentGuide.objects.create(
            result=mock_result,
            factors=factors,
            positive_rating=0,
            negative_rating=0,
            created_by=user
        )
        
        logger.info("Created treatment guide with ID: %s", treatment_guide.id)
        
        # Return the result in expected format
        return {
            "id": treatment_guide.id,
            "result": treatment_guide.result,
            "factors": treatment_guide.factors,
            "positive_rating": treatment_guide.positive_rating,
            "negative_rating": treatment_guide.negative_rating
        }
        
    except Exception as e:
        logger.error("Error creating treatment guide: %s", str(e), exc_info=True)
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

@transaction.atomic
def rate_treatment_guide(*, guide_id: int, rating: str, user: User) -> None:
    """
    Rate a treatment guide with thumbs up or down.
    
    Args:
        guide_id: ID of the treatment guide to rate
        rating: Either 'up' or 'down'
        user: User performing the rating
        
    Raises:
        ObjectDoesNotExist: If treatment guide doesn't exist
        TreatmentGuideValidationError: If rating is invalid
    """
    try:
        # Get the treatment guide
        guide = TreatmentGuide.objects.get(id=guide_id)
        
        # Update the appropriate rating counter
        if rating == 'up':
            guide.positive_rating = guide.positive_rating + 1
            field_name = 'positive_rating'
        elif rating == 'down':
            guide.negative_rating = guide.negative_rating + 1
            field_name = 'negative_rating'
        else:
            logger.warning(f"Invalid rating value: {rating}")
            raise TreatmentGuideValidationError("Rating must be either 'up' or 'down'")
        
        # Save only the modified rating field
        guide.save(update_fields=[field_name])
        
        logger.info(
            "Updated %s for treatment guide %d by user %s",
            field_name,
            guide_id,
            user.username
        )
        
    except ObjectDoesNotExist as exc:
        logger.warning("Treatment guide with id %d not found", guide_id)
        raise exc