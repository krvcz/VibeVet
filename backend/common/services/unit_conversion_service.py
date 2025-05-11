from decimal import Decimal, ROUND_HALF_UP
from typing import Dict

class UnitConversioError(Exception):
    """Custom exception for dosage calculation errors."""

class UnitConversionService:
    # Conversion factors relative to base units
    MASS_CONVERSIONS = {
        'ng': Decimal('0.000000001'),  # nanogram to gram
        'μg': Decimal('0.000001'),     # microgram to gram
        'mg': Decimal('0.001'),        # milligram to gram
        'g': Decimal('1'),             # gram (base unit)
        'kg': Decimal('1000'),         # kilogram to gram
    }
    
    VOLUME_CONVERSIONS = {
        'μl': Decimal('0.000001'),     # microliter to liter
        'ml': Decimal('0.001'),        # milliliter to liter
        'l': Decimal('1'),             # liter (base unit)
    }

    CONCENTRATION_CONVERSIONS = {
        'ng/ml': Decimal('0.001'),     # ng/mL to μg/mL
        'μg/ml': Decimal('1'),         # μg/mL (base unit)
        'mg/ml': Decimal('1000'),      # mg/mL to μg/mL
        'g/ml': Decimal('1000000'),    # g/mL to μg/mL
    }

    @classmethod
    def get_conversion_map(cls, unit_type: str) -> Dict[str, Decimal]:
        """Get the conversion map for a given unit type"""
        if unit_type == 'mass':
            return cls.MASS_CONVERSIONS
        elif unit_type == 'volume':
            return cls.VOLUME_CONVERSIONS
        elif unit_type == 'concentration':
            return cls.CONCENTRATION_CONVERSIONS
        raise UnitConversioError(f"Unknown unit type: {unit_type}")

    @classmethod
    def convert(cls, value: Decimal, from_unit: str, to_unit: str) -> Decimal:
        """
        Convert a value from one unit to another
        
        Args:
            value: The value to convert
            from_unit: The source unit (e.g., 'mg', 'mL')
            to_unit: The target unit (e.g., 'g', 'L')
            
        Returns:
            Decimal: The converted value
            
        Raises:
            UnitConversioError: If units are incompatible or unknown
        """
        # First, determine the unit type
        unit_type = cls._determine_unit_type(from_unit, to_unit)
        conversion_map = cls.get_conversion_map(unit_type)
        
        if from_unit not in conversion_map or to_unit not in conversion_map:
            raise UnitConversioError(f"Cannot convert from {from_unit} to {to_unit}")
        
        # Convert to base unit first, then to target unit
        base_value = value * conversion_map[from_unit]
        result = base_value / conversion_map[to_unit]
        
        # Round to 5 decimal places using ROUND_HALF_UP
        return result.quantize(Decimal('0.00001'), rounding=ROUND_HALF_UP)

    @classmethod
    def _determine_unit_type(cls, unit1: str, unit2: str) -> str:
        """Determine the type of units (mass, volume, or concentration)"""
        for unit in (unit1, unit2):
            if unit in cls.MASS_CONVERSIONS:
                return 'mass'
            elif unit in cls.VOLUME_CONVERSIONS:
                return 'volume'
            elif unit in cls.CONCENTRATION_CONVERSIONS:
                return 'concentration'
        raise UnitConversioError(f"Cannot determine unit type for {unit1} and {unit2}")

    @classmethod
    def is_compatible(cls, unit1: str, unit2: str) -> bool:
        """Check if two units are compatible for conversion"""
        try:
            cls._determine_unit_type(unit1, unit2)
            return True
        except UnitConversioError:
            return False