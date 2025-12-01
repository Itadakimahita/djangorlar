from typing import Any

from django.db import models
from django.utils import timezone as django_timezone


class AbstractBaseModel(models.Model):
    """Abstract base model with common fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
    
    def delete(self, *args: tuple[Any, ...], **kwargs: dict[Any, Any]) -> None:
        """Soft delete the object by setting deleted_at timestamp."""

        self.deleted_at = django_timezone.now()
        self.save(update_fields=['deleted_at'])