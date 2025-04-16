from decimal import Decimal
import logging
from django.core.exceptions import ValidationError
from django.db import transaction
from core.models import Drug, Species, MeasurementUnit

logger = logging.getLogger('core')

class DosageCalculationError(Exception):
    """Custom exception for dosage calculation errors."""

@transaction.atomic
def calculate_dosage(drug_id: int, weight: int, species: int, target_unit: int) -> dict:
    """
    Calculate drug dosage based on provided parameters.
    
    Args:
        drug_id: ID of the drug
        weight: Animal weight (1-999)
        species: ID of the species
        target_unit: ID of the target measurement unit
    
    Returns:
        dict with calculated_dose and unit
        
    Raises:
        ValidationError: If input validation fails
        DosageCalculationError: If calculation fails
    """
    try:
        # Input validation
        if not isinstance(weight, int) or weight < 1 or weight > 999:
            logger.warning("Invalid weight value: %s", weight)
            raise ValidationError("Weight must be an integer between 1 and 999")

        # Validate drug exists and fetch it with related data
        try:
            drug = Drug.objects.select_related('measurement_target').get(id=drug_id)
        except Drug.DoesNotExist as exc:
            logger.warning("Drug with id %s does not exist", drug_id)
            raise ValidationError(f"Drug with id {drug_id} does not exist") from exc
        
        # Validate species exists
        try:
            species_obj = Species.objects.get(id=species)
        except Species.DoesNotExist as exc:
            logger.warning("Species with id %s does not exist", species)
            raise ValidationError(f"Species with id {species} does not exist") from exc
        
        # Validate measurement unit exists
        try:
            target_unit_obj = MeasurementUnit.objects.get(id=target_unit)
        except MeasurementUnit.DoesNotExist as exc:
            logger.warning("Measurement unit with id %s does not exist", target_unit)
            raise ValidationError(f"Measurement unit with id {target_unit} does not exist") from exc
        
        # Validate species compatibility
        if drug.species_id != species:
            logger.warning(
                "Drug %s is not compatible with species %s",
                drug.name,
                species_obj.name
            )
            raise ValidationError(f"Drug {drug.name} is not compatible with species {species_obj.name}")

        # Convert measurement value to Decimal for precise calculation
        base_value = Decimal(str(drug.measurement_value))
        weight_factor = Decimal(str(weight)) / Decimal('100')  # Weight-based scaling
        
        # Calculate dose with proper precision
        calculated_dose = base_value * weight_factor
        logger.info(
            "Calculated dose %s %s for drug %s and weight %s",
            calculated_dose,
            target_unit_obj.short_name,
            drug.name,
            weight
        )
        
        # Format the result with high precision
        return {
            "drug_id": drug_id,
            "calculated_dose": f"{calculated_dose:.5f}",
            "unit": target_unit_obj.short_name
        }
        
    except Exception as e:
        logger.error("Error calculating dosage: %s", str(e), exc_info=True)
        raise DosageCalculationError(f"Error calculating dosage: {str(e)}") from e