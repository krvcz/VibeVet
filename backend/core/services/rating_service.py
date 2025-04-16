from typing import Any, Literal
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Model

from ..models import Rating

class RatingValidationError(Exception):
    """Custom exception for rating validation errors."""
    pass

def rate_content(*, content_object: Model, rating: Literal['up', 'down'], user: User) -> None:
    """
    Rate any content object that should support ratings.
    
    Args:
        content_object: The object being rated (DrugInteraction, TreatmentGuide etc.)
        rating: Either 'up' or 'down'
        user: User performing the rating
        
    Raises:
        RatingValidationError: If validation fails or user already rated
        ObjectDoesNotExist: If content object doesn't exist
    """
    content_type = ContentType.objects.get_for_model(content_object)

    # Check if user already rated this content
    if Rating.objects.filter(
        content_type=content_type,
        object_id=content_object.id,
        created_by=user
    ).exists():
        raise RatingValidationError("You have already rated this content")

    # Update the appropriate rating field and create rating record
    with transaction.atomic():
        # Increment the appropriate counter on the content object
        if rating == 'up':
            content_object.positive_rating = content_object.positive_rating + 1
        else:  # rating == 'down'
            content_object.negative_rating = content_object.negative_rating + 1
        content_object.save(update_fields=['positive_rating', 'negative_rating'])
        
        # Create rating record
        Rating.objects.create(
            content_type=content_type,
            object_id=content_object.id,
            rating=rating,
            created_by=user
        )