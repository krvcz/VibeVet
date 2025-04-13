from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .managers import CustomDrugManager, UserSearchHistoryManager

class BaseAuditModel(models.Model):
    """
    Abstract base model to provide audit fields for all models.
    """
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_created'
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(f"BaseAuditModel {self.pk}")


class Species(BaseAuditModel):
    """
    Model to store animal species information.
    """
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'species'
        verbose_name = 'Species'
        verbose_name_plural = 'Species'

    def __str__(self) -> str:
        return str(self.name)


class MeasurementUnit(BaseAuditModel):
    """
    Model to store measurement units for drug dosages.
    """
    short_name = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'measurement_unit'
        verbose_name = 'Measurement Unit'
        verbose_name_plural = 'Measurement Units'

    def __str__(self) -> str:
        return str(f"{self.name} ({self.short_name})")


class Drug(BaseAuditModel):
    """
    Model to store drug information.
    """
    name = models.CharField(max_length=20)
    active_ingredient = models.CharField(max_length=20)
    species = models.ForeignKey(
        Species,
        on_delete=models.PROTECT,
        related_name='drugs'
    )
    contraindications = models.CharField(max_length=100, null=True, blank=True)
    measurement_value = models.DecimalField(
        max_digits=10,
        decimal_places=5
    )
    measurement_target = models.ForeignKey(
        MeasurementUnit,
        on_delete=models.PROTECT,
        related_name='drugs'
    )

    class Meta:
        db_table = 'drug'
        verbose_name = 'Drug'
        verbose_name_plural = 'Drugs'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['active_ingredient']),
            models.Index(fields=['species'])
        ]

    def __str__(self) -> str:
        return str(f"{self.name} ({self.active_ingredient})")


class CustomDrug(BaseAuditModel):
    """
    Model to store user-specific custom drug information.
    """
    name = models.CharField(max_length=20)
    active_ingredient = models.CharField(max_length=20)
    species = models.ForeignKey(
        Species,
        on_delete=models.PROTECT,
        related_name='custom_drugs'
    )
    contraindications = models.CharField(max_length=100, null=True, blank=True)
    measurement_value = models.DecimalField(
        max_digits=10,
        decimal_places=5
    )
    measurement_target = models.ForeignKey(
        MeasurementUnit,
        on_delete=models.PROTECT,
        related_name='custom_drugs'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='custom_drugs'
    )

    objects = CustomDrugManager()

    class Meta:
        db_table = 'custom_drug'
        verbose_name = 'Custom Drug'
        verbose_name_plural = 'Custom Drugs'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['active_ingredient']),
            models.Index(fields=['user', 'species'])
        ]

    def __str__(self) -> str:
        if hasattr(self, 'user') and self.user:
            return str(f"{self.name} ({self.active_ingredient}) - {str(self.user)}")
        return str(f"{self.name} ({self.active_ingredient}) - Unknown")


class DrugInteraction(BaseAuditModel):
    """
    Model to store drug interaction information and AI-generated results.
    """
    query = models.TextField()
    result = models.TextField()
    context = models.CharField(max_length=50, null=True, blank=True)
    positive_rating = models.PositiveIntegerField(default=0)
    negative_rating = models.PositiveIntegerField(default=0)
    drugs = models.ManyToManyField(
        Drug,
        related_name='interactions'
    )

    class Meta:
        db_table = 'drug_interaction'
        verbose_name = 'Drug Interaction'
        verbose_name_plural = 'Drug Interactions'
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['created_by'])
        ]

    def __str__(self) -> str:
        query_text = str(self.query)
        return str(f"Interaction query: {query_text[:50]}...")


class TreatmentGuide(BaseAuditModel):
    """
    Model to store treatment guides and AI-generated recommendations.
    """
    query = models.TextField()
    result = models.TextField()
    factors = models.JSONField()
    positive_rating = models.PositiveIntegerField(default=0)
    negative_rating = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'treatment_guide'
        verbose_name = 'Treatment Guide'
        verbose_name_plural = 'Treatment Guides'
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['created_by'])
        ]

    def __str__(self) -> str:
        query_text = str(self.query)
        return str(f"Treatment guide: {query_text[:50]}...")


class SystemLog(models.Model):
    """
    Model to store system logs.
    """
    timestamp = models.DateTimeField(default=timezone.now)
    log_level = models.CharField(max_length=10)
    message = models.TextField()
    source = models.CharField(max_length=20)
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='system_logs'
    )

    class Meta:
        db_table = 'system_log'
        verbose_name = 'System Log'
        verbose_name_plural = 'System Logs'
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['source']),
            models.Index(fields=['log_level']),
            models.Index(fields=['user'])
        ]

    def __str__(self) -> str:
        message_text = str(self.message)
        return str(f"{self.timestamp} - {self.log_level}: {message_text[:50]}...")


class UserSearchHistory(BaseAuditModel):
    """
    Model to store user search history across different modules.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='search_history'
    )
    module = models.CharField(max_length=20)
    query = models.TextField()

    objects = UserSearchHistoryManager()

    class Meta:
        db_table = 'user_search_history'
        verbose_name = 'User Search History'
        verbose_name_plural = 'User Search Histories'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['module']),
            models.Index(fields=['user', 'module']),
            models.Index(fields=['created_at'])
        ]

    def __str__(self) -> str:
        if hasattr(self, 'user') and self.user:
            return str(f"{str(self.user)} - {self.module}: {str(self.query)[:50]}...")
        return str(f"Unknown - {self.module}: {str(self.query)[:50]}...")