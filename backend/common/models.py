from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

class BaseAuditModel(models.Model):
    """
    Abstract base model to provide audit fields for all models.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'species'
        verbose_name = 'Species'
        verbose_name_plural = 'species'
        ordering = ['name']

    def __str__(self) -> str:
        return str(self.name)


class Unit(BaseAuditModel):
    """
    Model to store measurement units.
    """
    name = models.CharField(max_length=20, unique=True)
    short_name = models.CharField(max_length=5, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'unit'
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'
        ordering = ['name']

    def __str__(self) -> str:
        return f"{self.name} ({self.short_name})"


class Rating(BaseAuditModel):
    """
    Generic model for storing user ratings for different types of content (drug interactions, diagnoses, etc.).
    Uses Django's ContentTypes framework to create generic relations.
    """
    RATING_CHOICES = [
        ('up', 'Positive'),
        ('down', 'Negative')
    ]

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    rating = models.CharField(max_length=4, choices=RATING_CHOICES)

    class Meta:
        db_table = 'rating'
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['created_by'])
        ]
        unique_together = [['created_by', 'content_type', 'object_id']]

    def __str__(self) -> str:
        return f"{self.created_by}'s {self.rating} rating for {self.content_type.model} {self.object_id}"


class SystemLog(models.Model):
    """
    Model to store system logs.
    """
    timestamp = models.DateTimeField(default=timezone.now)
    log_level = models.CharField(max_length=10)
    message = models.TextField()
    source = models.CharField(max_length=20)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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