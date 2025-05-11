from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from common.models import BaseAuditModel, Rating
from drugs.models import Drug

class DrugInteraction(BaseAuditModel):
    """
    Model to store drug interaction queries and AI-generated results.
    """
    query = models.TextField()
    result = models.TextField()
    context = models.CharField(max_length=50, null=True, blank=True)
    drugs = models.ManyToManyField(Drug, related_name='interactions')
    ratings = GenericRelation(Rating)

    class Meta:
        db_table = 'drug_interaction'
        verbose_name = 'Drug Interaction'
        verbose_name_plural = 'Drug Interactions'
        indexes = [
            models.Index(fields=['created_by'])
        ]

    def __str__(self) -> str:
        return str(f"Drug Interaction {self.pk} - {self.query[:50]}...")
