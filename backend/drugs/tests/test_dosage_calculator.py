import pytest
from decimal import Decimal, ROUND_HALF_UP
from drugs.services.dosage_calculator_service import DosageCalculatorService, DosageCalculationError

pytestmark = pytest.mark.unit

class TestDosageCalculatorService:
    def test_basic_dosage_calculation(self):
        """Test basic dosage calculation without unit conversion."""
        result = DosageCalculatorService.calculate_dosage(
            drug_base_value=Decimal("100.00"),
            per_weight_value=Decimal("10.00"),
            weight=Decimal("25.00"),
            source_unit="mg",
            target_unit="mg"
        )
        
        # For 100mg/10kg and weight 25kg, expect 250mg
        assert result["calculated_dose"] == Decimal("250.00000")
        assert result["unit"] == "mg"

    def test_dosage_calculation_with_unit_conversion(self):
        """Test dosage calculation with unit conversion."""
        result = DosageCalculatorService.calculate_dosage(
            drug_base_value=Decimal("1000.00"),  # 1000mg
            per_weight_value=Decimal("10.00"),
            weight=Decimal("20.00"),
            source_unit="mg",
            target_unit="g"
        )
        
        # For 1000mg/10kg and weight 20kg, expect 2g (2000mg -> 2g)
        assert result["calculated_dose"] == Decimal("2.00000")
        assert result["unit"] == "g"

    def test_dosage_calculation_with_small_values(self):
        """Test dosage calculation with very small values."""
        result = DosageCalculatorService.calculate_dosage(
            drug_base_value=Decimal("0.00001"),
            per_weight_value=Decimal("1.00"),
            weight=Decimal("1.00"),
            source_unit="mg",
            target_unit="mg"
        )
        
        assert result["calculated_dose"] == Decimal("0.00001")
        assert result["unit"] == "mg"

    def test_dosage_calculation_with_zero_weight(self):
        """Test that calculation with zero weight raises error."""
        with pytest.raises(DosageCalculationError):
            DosageCalculatorService.calculate_dosage(
                drug_base_value=Decimal("100.00"),
                per_weight_value=Decimal("10.00"),
                weight=Decimal("0.00"),
                source_unit="mg",
                target_unit="mg"
            )

    def test_dosage_calculation_with_negative_values(self):
        """Test that calculation with negative values raises error."""
        with pytest.raises(DosageCalculationError):
            DosageCalculatorService.calculate_dosage(
                drug_base_value=Decimal("-100.00"),
                per_weight_value=Decimal("10.00"),
                weight=Decimal("25.00"),
                source_unit="mg",
                target_unit="mg"
            )

    def test_dosage_calculation_with_incompatible_units(self):
        """Test that calculation with incompatible units raises error."""
        with pytest.raises(DosageCalculationError):
            DosageCalculatorService.calculate_dosage(
                drug_base_value=Decimal("100.00"),
                per_weight_value=Decimal("10.00"),
                weight=Decimal("25.00"),
                source_unit="mg",
                target_unit="ml"  # Incompatible unit conversion
            )

    def test_rounding_precision(self):
        """Test that results are rounded to 5 decimal places."""
        result = DosageCalculatorService.calculate_dosage(
            drug_base_value=Decimal("100.00"),
            per_weight_value=Decimal("3.00"),
            weight=Decimal("10.00"),
            source_unit="mg",
            target_unit="mg"
        )
        
        # Result should have exactly 5 decimal places
        decimal_places = abs(result["calculated_dose"].as_tuple().exponent)
        assert decimal_places == 5

    def test_edge_case_large_numbers(self):
        """Test calculation with large numbers."""
        result = DosageCalculatorService.calculate_dosage(
            drug_base_value=Decimal("9999.99999"),
            per_weight_value=Decimal("10.00"),
            weight=Decimal("999.99"),
            source_unit="mg",
            target_unit="mg"
        )
        
        assert result["calculated_dose"] > 0
        assert isinstance(result["calculated_dose"], Decimal) 