import logging
from typing import Dict, Any
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.exceptions import ValidationError
from ..models import CustomDrug, Unit
from common.models import Species

logger = logging.getLogger(__name__)

class CustomDrugValidationError(ValidationError):
    """Custom exception for drug validation errors"""

def validate_custom_drug_data(data: Dict[str, Any], partial: bool = False) -> None:
    """
    Validate custom drug data before creation or update.
    
    Args:
        data: Data to validate
        partial: If True, skips validation for missing fields (for PATCH requests)
    
    Raises:
        CustomDrugValidationError if validation fails
    """
    if not partial or 'name' in data:
        if len(str(data['name']).strip()) == 0:
            raise CustomDrugValidationError('Name cannot be empty')
        
    if not partial or 'active_ingredient' in data:
        if len(str(data['active_ingredient']).strip()) == 0:
            raise CustomDrugValidationError('Active ingredient cannot be empty')
        
    if not partial or 'measurement_value' in data:
        if Decimal(str(data['measurement_value'])) <= 0:
            raise CustomDrugValidationError('Measurement value must be positive')

def create_custom_drug(data: Dict[str, Any], user: 'AbstractUser') -> CustomDrug:
    """
    Create a new custom drug for a specific user.
    
    Args:
        data: Validated data from CreateCustomDrugSerializer
        user: The authenticated user creating the drug
    
    Returns:
        CustomDrug: The created custom drug instance
        
    Raises:
        CustomDrugValidationError: If validation fails
        Species.DoesNotExist: If species_id is invalid
        Unit.DoesNotExist: If measurement_unit_id is invalid
    """
    try:
        # Additional validation
        validate_custom_drug_data(data)
        
        # Get related objects
        species: Species = Species.objects.get(id=data['species'])
        measurement_unit: Unit = Unit.objects.get(id=data['measurement_unit'])
        per_weight_unit: Unit = Unit.objects.get(id=data['per_weight_unit'])
        
        # Create custom drug in transaction
        with transaction.atomic():
            custom_drug: CustomDrug = CustomDrug.objects.create(
                name=str(data['name']).strip(),
                active_ingredient=str(data['active_ingredient']).strip(),
                species=species,
                contraindications=data.get('contraindications'),
                measurement_value=Decimal(str(data['measurement_value'])),
                measurement_unit=measurement_unit,
                per_weight_value=Decimal(str(data['per_weight_value'])),
                per_weight_unit=per_weight_unit,
                user=user,
                created_by=user
            )
            
        logger.info(
            "Custom drug created: %s (ID: %d) by user %s",
            custom_drug.name,
            custom_drug.id,
            user.username
        )
        return custom_drug
        
    except Species.DoesNotExist as exc:
        logger.error("Invalid species ID: %d", data['species'])
        raise CustomDrugValidationError('Invalid species selected') from exc
        
    except Unit.DoesNotExist as exc:
        logger.error("Invalid measurement unit ID: %d", data.get('measurement_unit') or data.get('per_weight_unit'))
        raise CustomDrugValidationError('Invalid measurement unit selected') from exc
        
    except Exception as exc:
        logger.error("Error creating custom drug: %s", str(exc))
        raise

def update_custom_drug(
    custom_drug: CustomDrug,
    data: Dict[str, Any],
    user: 'AbstractUser',
    partial: bool = False
) -> CustomDrug:
    """
    Update an existing custom drug.
    
    Args:
        custom_drug: The CustomDrug instance to update
        data: Update data from UpdateCustomDrugSerializer
        user: The authenticated user updating the drug
        partial: If True, allows partial updates (PATCH)
    
    Returns:
        CustomDrug: The updated custom drug instance
        
    Raises:
        CustomDrugValidationError: If validation fails
        Species.DoesNotExist: If species_id is invalid
        Unit.DoesNotExist: If measurement_unit_id is invalid
    """
    if custom_drug.user != user:
        raise CustomDrugValidationError("You don't have permission to modify this custom drug")
    
    try:
        # Validate the update data
        validate_custom_drug_data(data, partial=partial)
        
        with transaction.atomic():
            # Update species if provided
            if 'species' in data:
                species = Species.objects.get(id=data['species'])
                custom_drug.species = species
                
            # Update measurement unit if provided
            if 'measurement_unit' in data:
                measurement_unit = Unit.objects.get(id=data['measurement_unit'])
                custom_drug.measurement_unit = measurement_unit

            # Update per weight unit if provided
            if 'per_weight_unit' in data:
                per_weight_unit = Unit.objects.get(id=data['per_weight_unit'])
                custom_drug.per_weight_unit = per_weight_unit
            
            # Update scalar fields
            if 'name' in data:
                custom_drug.name = str(data['name']).strip()
            if 'active_ingredient' in data:
                custom_drug.active_ingredient = str(data['active_ingredient']).strip()
            if 'contraindications' in data:
                custom_drug.contraindications = data['contraindications']
            if 'measurement_value' in data:
                custom_drug.measurement_value = Decimal(str(data['measurement_value']))
            if 'per_weight_value' in data:
                custom_drug.per_weight_value = Decimal(str(data['per_weight_value']))
            
            custom_drug.save()
            
        logger.info(
            "Custom drug updated: %s (ID: %d) by user %s",
            custom_drug.name,
            custom_drug.id,
            user.username
        )
        return custom_drug
        
    except Species.DoesNotExist as exc:
        logger.error("Invalid species ID: %d", data['species'])
        raise CustomDrugValidationError('Invalid species selected') from exc
        
    except Unit.DoesNotExist as exc:
        logger.error("Invalid measurement unit ID")
        raise CustomDrugValidationError('Invalid measurement unit selected') from exc
        
    except Exception as exc:
        logger.error("Error updating custom drug: %s", str(exc))
        raise

def delete_custom_drug(custom_drug: CustomDrug, user: 'AbstractUser') -> None:
    """
    Delete a custom drug.
    
    Args:
        custom_drug: The CustomDrug instance to delete
        user: The authenticated user deleting the drug
    
    Raises:
        CustomDrugValidationError: If user is not the owner
    """
    if custom_drug.user != user:
        raise CustomDrugValidationError("You don't have permission to delete this custom drug")
        
    try:
        drug_id = custom_drug.id
        drug_name = custom_drug.name
        
        with transaction.atomic():
            custom_drug.delete()
            
        logger.info(
            "Custom drug deleted: %s (ID: %d) by user %s",
            drug_name,
            drug_id,
            user.username
        )
        
    except Exception as exc:
        logger.error("Error deleting custom drug: %s", str(exc))
        raise