from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.indexes import GinIndex
from common.models import BaseAuditModel, Rating

class TreatmentGuide(BaseAuditModel):
    """
    Model to store treatment guide queries and AI-generated results.
    """
    query = models.TextField()
    result = models.TextField()
    factors = models.JSONField()
    ratings = GenericRelation(Rating)

    class Meta:
        db_table = 'treatment_guide'
        verbose_name = 'Treatment Guide'
        verbose_name_plural = 'Treatment Guides'
        indexes = [
            models.Index(fields=['created_by']),
            GinIndex(fields=['factors'], name='factors_gin_idx', opclasses=['jsonb_path_ops'])
        ]

    def __str__(self) -> str:
        return str(f"Treatment Guide {self.pk} - {self.query[:50]}...")
