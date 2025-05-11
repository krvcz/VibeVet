from decimal import Decimal, ROUND_HALF_UP
import logging
from django.core.exceptions import ValidationError
from django.db import transaction
from ..models import Drug, Unit
from common.models import Species
from typing import Dict
from common.services.unit_conversion_service import UnitConversionService

logger = logging.getLogger('drugs')

class DosageCalculationError(Exception):
    """Custom exception for dosage calculation errors."""

class DosageCalculatorService:
    @staticmethod
    def calculate_dosage(
        drug_base_value: Decimal,
        per_weight_value: Decimal,
        weight: Decimal,
        source_unit: str,
        target_unit: str,
    ) -> Dict[str, Decimal]:
        """
        Calculate drug dosage based on animal weight and perform unit conversion if needed.
        
        Args:
            drug_base_value: Base value of the drug
            per_weight_value: Value of weight unit for the base value (e.g., 10 for "per 10 kg")
            weight: Animal weight
            source_unit: Original unit of the drug measurement
            target_unit: Desired unit for the result
            
        Returns:
            Dict containing calculated dose and unit
        """
        # Calculate the weight factor (e.g., if drug is 100mg per 10kg and weight is 25kg, factor is 2.5)
        weight_factor = weight / per_weight_value if per_weight_value else weight
        
        # Calculate the basic dosage
        calculated_dose = drug_base_value * weight_factor
        
        # If target unit is different from source unit, convert it
        if source_unit != target_unit:
            calculated_dose = UnitConversionService.convert(
                calculated_dose,
                source_unit,
                target_unit
            )
        else:
            # Even if no conversion is needed, ensure consistent rounding
            calculated_dose = calculated_dose.quantize(
                Decimal('0.00001'),
                rounding=ROUND_HALF_UP
            )

        return {
            'calculated_dose': calculated_dose,
            'unit': target_unit
        }

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
            target_unit_obj = Unit.objects.get(id=target_unit)
        except Unit.DoesNotExist as exc:
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
        
        # Calculate dose using the DosageCalculatorService
        dosage_result = DosageCalculatorService.calculate_dosage(
            base_value,
            weight_factor,
            drug.measurement_target.short_name,
            target_unit_obj.short_name
        )
        
        logger.info(
            "Calculated dose %s %s for drug %s and weight %s",
            dosage_result['calculated_dose'],
            dosage_result['unit'],
            drug.name,
            weight
        )
        
        # Format the result with high precision
        return {
            "drug_id": drug_id,
            "calculated_dose": f"{dosage_result['calculated_dose']:.5f}",
            "unit": dosage_result['unit']
        }
        
    except Exception as e:
        logger.error("Error calculating dosage: %s", str(e), exc_info=True)
        raise DosageCalculationError(f"Error calculating dosage: {str(e)}") from e