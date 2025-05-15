from django.db import models
from django.conf import settings
from common.models import BaseAuditModel, Species, Unit
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal


class BaseDrugModel(BaseAuditModel):
    """
    Abstract base model to provide audit fields for all models.
    """
    name = models.CharField(max_length=20)
    active_ingredient = models.CharField(max_length=20)
    species = models.ForeignKey(Species, on_delete=models.PROTECT)
    contraindications = models.CharField(max_length=100, null=True, blank=True)
    measurement_value = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        validators=[MinValueValidator(Decimal('0.00001'))]
    )
    measurement_unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name='%(class)s_measurement_unit'
    )
    per_weight_value = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        validators=[MinValueValidator(Decimal('0.00001'))]
    )
    per_weight_unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name='%(class)s_per_weight_unit'
    )

    class Meta:
        abstract = True

    def clean(self):
        """Validate the model instance."""
        super().clean()
        if self.measurement_value <= 0:
            raise ValidationError({'measurement_value': 'Measurement value must be positive'})
        if self.per_weight_value <= 0:
            raise ValidationError({'per_weight_value': 'Per weight value must be positive'})
        if len(self.name) > 20:
            raise ValidationError({'name': 'Name cannot exceed 20 characters'})

    def save(self, *args, **kwargs):
        """Override save to ensure validation is always run."""
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(f"BaseDrugModel {self.pk}")


class Drug(BaseDrugModel):
    """
    Model for standard drugs.
    """

    class Meta:
        db_table = 'drug'
        verbose_name = 'Drug'
        verbose_name_plural = 'Drugs'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['active_ingredient'])
        ]

    def __str__(self) -> str:
        return str(f"{self.name} ({self.active_ingredient})")


class CustomDrug(BaseDrugModel):
    """
    Model for user-specific custom drugs.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='custom_drugs'
    )

    class Meta:
        db_table = 'custom_drug'
        verbose_name = 'Custom Drug'
        verbose_name_plural = 'Custom Drugs'
        indexes = [
            models.Index(fields=['user'])
        ]

    def __str__(self) -> str:
        return str(f"Custom Drug: {self.name} (by {self.user})")
