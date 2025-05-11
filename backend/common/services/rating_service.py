from typing import Literal
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from ..models import Rating

from django.contrib.auth.models import AbstractUser
from django.db.models import Model



class RatingValidationError(Exception):
    """Custom exception for rating validation errors."""

def rate_content(*, content_object: 'Model', rating: Literal['up', 'down'], user: 'AbstractUser') -> Rating:
    """
    Rate any content object that should support ratings.
    
    Args:
        content_object: The object being rated (DrugInteraction, TreatmentGuide etc.)
        rating: Either 'up' or 'down'
        user: User performing the rating
        
    Returns:
        Rating: The created rating instance
        
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
        rating = Rating.objects.filter(
        content_type=content_type,
        object_id=content_object.id,
        created_by=user).update(rating=rating)

        return rating

    # Create rating record in a transaction
    with transaction.atomic():
        instance = Rating.objects.create(
            content_type=content_type,
            object_id=content_object.id,
            rating=rating,
            created_by=user
        )
    return instance