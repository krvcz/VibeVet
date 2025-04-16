import logging
from django.db import transaction
from django.contrib.auth.models import User
from core.models import UserSearchHistory

logger = logging.getLogger('core')

@transaction.atomic
def add_to_history(*, module: str, query: str, user: User | None = None) -> UserSearchHistory:
    """
    Add a search query to user's search history.
    
    Args:
        module: Name of the module (e.g., 'drug-interaction', 'dosage-calc', 'treatment-guide')
        query: Search query or interaction content
        user: User who performed the search, if None will use mock user
    
    Returns:
        Created UserSearchHistory instance
    """
    try:
        
        history_entry = UserSearchHistory.objects.create(
            module=module,
            query=query,
            created_by=user  # Only created_by is needed from BaseAuditModel
        )
        
        logger.info(
            "Added search history entry for user %s in module %s: %s",
            user.username,
            module,
            query
        )
        
        return history_entry
        
    except Exception as e:
        logger.error(
            "Error adding search history entry: %s",
            str(e),
            exc_info=True
        )
        raise