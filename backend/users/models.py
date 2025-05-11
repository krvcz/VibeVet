from django.db import models
from common.models import BaseAuditModel
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email jest wymagany')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # Wyłączamy pole username
    email = models.EmailField(_('email address'), unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class UserSearchHistory(BaseAuditModel):
    """
    Model to store user search history across different modules.
    """
    module = models.CharField(
        max_length=20,
        db_index=True,
        help_text="Module identifier (e.g., 'drug-interaction', 'dosage-calc', 'treatment-guide')"
    )
    query = models.TextField(
        help_text="The search query or interaction content"
    )

    class Meta:
        db_table = 'user_search_history'
        verbose_name = 'User Search History'
        verbose_name_plural = 'User Search Histories'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['created_by', '-created_at']),
            models.Index(fields=['created_by', 'module', '-created_at'])
        ]

    def __str__(self) -> str:
        return f"{self.module} search by {self.created_by} at {self.created_at}"
