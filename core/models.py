from django.db import models
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from django.contrib.auth.models import User
from core.middlewares import get_current_user


# Create your models here.
class StampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        current_user = get_current_user()
        if not self.pk:  # Object is being created
            if not self.user:
                raise ValueError("User must be set for new objects")
            self.created_by = current_user
        else:  # Object is being updated
            self.updated_by = current_user
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        indexes = [
            # Index for the year extracted from `created_at`
            models.Index(
                name="idx_created_year",
                fields=[],
                expressions=[ExtractYear("created_at")],
            ),
            # Index for the month extracted from `created_at`
            models.Index(
                name="idx_created_month",
                fields=[],
                expressions=[ExtractMonth("created_at")],
            ),
            # Index for the day extracted from `created_at`
            models.Index(
                name="idx_created_day",
                fields=[],
                expressions=[ExtractDay("created_at")],
            ),
        ]
