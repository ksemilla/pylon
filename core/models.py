from django.db import models
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from django.conf import settings
from core.middlewares import get_current_user


# Create your models here.
class StampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="created_%(class)s",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="updated_%(class)s",
    )

    def save(self, *args, **kwargs):
        current_user = get_current_user()
        if not self.pk:  # Object is being created
            # if not self.created_by:
            #     raise ValueError("User must be set for new objects")
            self.created_by = current_user
        else:  # Object is being updated
            self.updated_by = current_user
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


def generate_datetime_indexes(model_name):
    return [
        models.Index(
            ExtractYear("created_at"), fields=[], name=f"{model_name}_year_idx"
        ),
        models.Index(
            ExtractMonth("created_at"),
            fields=[],
            name=f"{model_name}_month_idx",
        ),
        models.Index(
            ExtractDay("created_at"), fields=[], name=f"{model_name}_day_idx"
        ),
    ]
